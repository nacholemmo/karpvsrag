"""Corre un brazo sobre un conjunto de preguntas y guarda resultados/respuestas_<brazo>.jsonl.

Uso:
    python brazos/correr.py --brazo contexto --prueba            # las 5 preguntas de prueba
    python brazos/correr.py --brazo rag --preguntas P01,P02
    python brazos/correr.py --brazo wiki --todas --limite 5
    python brazos/correr.py --brazo contexto --todas --estimar   # costo estimado, sin API

Saltea las preguntas ya respondidas. Una respuesta inválida (stop_reason distinto de end_turn o JSON roto)
no se guarda y se reintenta en la próxima corrida.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comun import config  # noqa: E402
from comun.llm import Corrida  # noqa: E402
from comun.precios import costo_usd  # noqa: E402

BRAZOS = {"contexto": "brazos.contexto.brazo", "rag": "brazos.rag.brazo", "wiki": "brazos.wiki.brazo"}
# Una pregunta por tipo, fijas: dato, procedimiento, cruce, contradicción, sin respuesta.
PRUEBA = ["P03", "P14", "P27", "P37", "P48"]
PREGUNTAS = config.RAIZ / "evals" / "preguntas.jsonl"


def cargar_jsonl(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def archivo_salida(brazo: str, sufijo: str = "") -> Path:
    return config.RAIZ / "resultados" / f"respuestas_{brazo}{sufijo}.jsonl"


def estimar(brazo: str, n: int) -> None:
    modelo = config.modelo_respuesta()
    if brazo == "contexto":
        tok = json.loads((config.RAIZ / "resultados" / "tokens_corpus.json").read_text())["tokens_prompt_contexto_completo"]
        total = costo_usd(modelo, 50, 1500, cache_escritura=tok) + (n - 1) * costo_usd(modelo, 50, 1500, cache_lectura=tok)
        peor = n * costo_usd(modelo, tok, 1500)
    elif brazo == "rag":
        total = peor = n * costo_usd(modelo, 4500, 1500)
    else:  # wiki: ~5 turnos con contexto creciente hasta ~25k, con caché parcial
        total = n * (costo_usd(modelo, 15_000, 3000, cache_lectura=45_000))
        peor = n * costo_usd(modelo, 60_000, 4000)
    print(f"Brazo {brazo}, {n} preguntas con {modelo}: USD {total:.4f} estimado (peor caso USD {peor:.4f})")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brazo", choices=BRAZOS, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prueba", action="store_true")
    g.add_argument("--todas", action="store_true")
    g.add_argument("--preguntas")
    ap.add_argument("--limite", type=int)
    ap.add_argument("--estimar", action="store_true")
    ap.add_argument("--sufijo", default="", help="sufijo del archivo de salida (por ejemplo _actualizacion)")
    ap.add_argument("--archivo-preguntas", type=Path, default=PREGUNTAS)
    args = ap.parse_args(argv)

    todas = {p["id"]: p for p in cargar_jsonl(args.archivo_preguntas)}
    ids = PRUEBA if args.prueba else sorted(todas) if args.todas else args.preguntas.split(",")
    salida = archivo_salida(args.brazo, args.sufijo)
    hechas = {r["pregunta_id"] for r in cargar_jsonl(salida)}
    pendientes = [todas[i] for i in ids if i not in hechas]
    if args.limite is not None:
        pendientes = pendientes[: args.limite]
    if args.estimar:
        estimar(args.brazo, len(pendientes))
        return 0

    modulo = importlib.import_module(BRAZOS[args.brazo])
    corrida = Corrida(f"brazo_{args.brazo}")
    print(f"Brazo {args.brazo}: {len(pendientes)} preguntas pendientes (ya hechas: {len(hechas)}) con {config.modelo_respuesta()}")
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("a", encoding="utf-8") as f:
        for p in pendientes:
            r = modulo.responder(p, corrida)
            if not r.pop("valido"):
                print(f"  {p['id']}: respuesta inválida (stop_reason={r.get('stop_reason')}); no se guarda")
                continue
            fila = {"id": f"{args.brazo}-{p['id']}", "pregunta_id": p["id"], "brazo": args.brazo, **r}
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            f.flush()
            print(f"  {p['id']} ({p['tipo']}): USD {r['costo_usd']:.4f}, {r['latencia_s']:.1f}s, "
                  f"{r['llamadas']} llamada(s), fuentes {r['fuentes']}")
    print(f"Costo de la corrida: USD {corrida.gastado_usd:.4f} en {corrida.llamadas} llamadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
