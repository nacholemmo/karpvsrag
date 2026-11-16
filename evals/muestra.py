"""Muestra de 15 respuestas juzgadas para revisión manual (fase 2).

9 respuestas reales: Haiku con todo el corpus en contexto (brazo "muestra_contexto").
6 respuestas sintéticas escritas a mano: evals/respuestas_sinteticas.jsonl.

Uso:
    python evals/muestra.py estimar                 # costo estimado, sin llamar a la API
    python evals/muestra.py responder --limite 5    # primero 5
    python evals/muestra.py responder               # el resto (saltea las ya respondidas)
    python evals/juez.py --respuestas evals/muestra_respuestas.jsonl --respuestas evals/respuestas_sinteticas.jsonl \
        --salida evals/juicios_muestra.jsonl
    python evals/muestra.py exportar                # evals/revision_manual.csv (a ciegas, sin veredictos)
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comun import config  # noqa: E402
from brazos.contexto.brazo import sistema_con_corpus  # noqa: E402
from comun.formato import FORMATO_RESPUESTA, normalizar_respuesta, parsear_json  # noqa: E402
from comun.llm import Corrida, llamar  # noqa: E402
from comun.precios import costo_usd  # noqa: E402

EVALS = config.RAIZ / "evals"
PREGUNTAS = EVALS / "preguntas.jsonl"
RESPUESTAS = EVALS / "muestra_respuestas.jsonl"
SINTETICAS = EVALS / "respuestas_sinteticas.jsonl"
JUICIOS = EVALS / "juicios_muestra.jsonl"
REVISION = EVALS / "revision_manual.csv"
MAPA = EVALS / "mapa_revision.json"  # caso opaco -> id de respuesta (no mirar antes de revisar)
SEMILLA = 42
# 9 preguntas reales, estratificadas por tipo (y subtipo en contradiccion_version)
CUPOS = {"dato": 2, "procedimiento": 1, "cruce": 2, "contradiccion": 1, "version": 1, "sin_respuesta": 2}

def cargar_jsonl(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def elegir_preguntas() -> list[dict]:
    preguntas = cargar_jsonl(PREGUNTAS)
    excluidas = {s["pregunta_id"] for s in cargar_jsonl(SINTETICAS)}
    rng = random.Random(SEMILLA)
    elegidas = []
    for clase, n in CUPOS.items():
        candidatas = [p for p in preguntas if p["id"] not in excluidas
                      and (p.get("subtipo") == clase or (p["tipo"] == clase and p.get("subtipo") is None))]
        elegidas += rng.sample(candidatas, n)
    return sorted(elegidas, key=lambda p: p["id"])


def estimar() -> None:
    tokens = json.loads((config.RAIZ / "resultados" / "tokens_corpus.json").read_text())["tokens_prompt_contexto_completo"]
    modelo = config.modelo_respuesta()
    n = len(elegir_preguntas())
    extra_in, salida = 50, 1500  # instrucciones + pregunta; salida con thinking en effort bajo (holgado)
    primera = costo_usd(modelo, extra_in, salida, cache_escritura=tokens)
    resto = costo_usd(modelo, extra_in, salida, cache_lectura=tokens)
    sin_cache = costo_usd(modelo, tokens + extra_in, salida)
    juez = 15 * costo_usd(config.modelo_juez(), 3000, 800)
    print(f"Modelo: {modelo} | corpus: {tokens} tokens | preguntas reales: {n}")
    print(f"Respuestas con caché: USD {primera + (n - 1) * resto:.4f} (peor caso sin caché: USD {n * sin_cache:.4f})")
    print(f"Juez (15 juicios): USD {juez:.4f}")
    print(f"Total estimado: USD {primera + (n - 1) * resto + juez:.4f} (peor caso: USD {n * sin_cache + juez:.4f})")


def responder(limite: int | None) -> None:
    hechas = {r["pregunta_id"] for r in cargar_jsonl(RESPUESTAS)}
    pendientes = [p for p in elegir_preguntas() if p["id"] not in hechas]
    if limite is not None:
        pendientes = pendientes[:limite]
    sistema = sistema_con_corpus()
    corrida = Corrida("muestra_contexto")
    print(f"Respondiendo {len(pendientes)} preguntas con {config.modelo_respuesta()} (ya hechas: {len(hechas)})")
    with RESPUESTAS.open("a", encoding="utf-8") as f:
        for p in pendientes:
            response, reg = llamar(
                "muestra_contexto", p["id"], corrida,
                max_tokens=8000,
                system=sistema,
                messages=[{"role": "user", "content": p["pregunta"]}],
                output_config={"effort": config.esfuerzo(), **FORMATO_RESPUESTA},
            )
            r = normalizar_respuesta(parsear_json(response))
            if reg["stop_reason"] != "end_turn" or "error" in r:
                print(f"  {p['id']}: respuesta inválida (stop_reason={reg['stop_reason']}); no se guarda, se reintenta en la próxima corrida")
                continue
            fila = {"id": f"real-{p['id']}", "pregunta_id": p["id"], "brazo": "muestra_contexto", **r,
                    "costo_usd": reg["costo_usd"], "latencia_s": reg["latencia_s"], "stop_reason": reg["stop_reason"]}
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            print(f"  {p['id']} ({p['tipo']}): USD {reg['costo_usd']:.4f}, {reg['latencia_s']}s, "
                  f"caché leída {reg['tokens_cache_lectura']}, escrita {reg['tokens_cache_escritura']}")
    print(f"Costo de la corrida: USD {corrida.gastado_usd:.4f}")


def exportar() -> None:
    preguntas = {p["id"]: p for p in cargar_jsonl(PREGUNTAS)}
    respuestas = cargar_jsonl(RESPUESTAS) + cargar_jsonl(SINTETICAS)
    rng = random.Random(SEMILLA)
    rng.shuffle(respuestas)  # mezcla reales y sintéticas para que no se distingan por posición
    mapa = {f"caso-{i:02d}": r["id"] for i, r in enumerate(respuestas, 1)}
    with REVISION.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["caso", "pregunta_id", "tipo", "pregunta", "respuesta_referencia", "elementos_clave",
                    "documentos_fuente", "respuesta", "fuentes_citadas", "tu_veredicto", "tu_fuente", "notas"])
        for caso, r in zip(mapa, respuestas):
            p = preguntas[r["pregunta_id"]]
            tipo = p["tipo"] + (f"/{p['subtipo']}" if p.get("subtipo") else "")
            w.writerow([caso, p["id"], tipo, p["pregunta"], p["respuesta_referencia"],
                        " | ".join(p["elementos_clave"]), " | ".join(p["documentos_fuente"]),
                        r["respuesta"], " | ".join(r.get("fuentes", [])), "", "", ""])
    MAPA.write_text(json.dumps(mapa, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Exportadas {len(respuestas)} filas a {REVISION.relative_to(config.RAIZ)}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("estimar")
    r = sub.add_parser("responder")
    r.add_argument("--limite", type=int)
    sub.add_parser("exportar")
    args = ap.parse_args(argv)
    if args.cmd == "estimar":
        estimar()
    elif args.cmd == "responder":
        responder(args.limite)
    else:
        exportar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
