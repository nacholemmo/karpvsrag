"""Juez: compara respuestas de un brazo contra la referencia de cada pregunta, según evals/RUBRICA.md.

Uso:
    python evals/juez.py --respuestas evals/muestra_respuestas.jsonl [--respuestas otro.jsonl] --salida evals/juicios_muestra.jsonl

Cada línea de un archivo de respuestas: {"id": "...", "pregunta_id": "P07", "brazo": "...", "respuesta": "...", "fuentes": [...]}
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comun import config  # noqa: E402
from comun.formato import parsear_json  # noqa: E402
from comun.llm import Corrida, llamar  # noqa: E402

RUBRICA = (config.RAIZ / "evals" / "RUBRICA.md").read_text(encoding="utf-8")
PREGUNTAS = config.RAIZ / "evals" / "preguntas.jsonl"
HECHOS = {h["hecho_id"]: h for h in csv.DictReader((config.RAIZ / "hechos.csv").open(encoding="utf-8"))}

ESQUEMA_JUICIO = {
    "type": "object",
    "properties": {
        "veredicto": {"type": "string", "enum": ["correcta", "parcial", "incorrecta"]},
        "fuente": {"type": "string", "enum": ["correcta", "parcial", "incorrecta", "no_aplica"]},
        "justificacion": {"type": "string"},
    },
    "required": ["veredicto", "fuente", "justificacion"],
    "additionalProperties": False,
}

SISTEMA = (
    "Sos un evaluador estricto y consistente. Aplicá exactamente la rúbrica que sigue. "
    "No uses conocimiento externo: la única verdad es la respuesta de referencia y sus elementos clave.\n\n" + RUBRICA
)


def cargar_jsonl(ruta: Path) -> list[dict]:
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def documentos_requeridos(pregunta: dict) -> tuple[list[str], str]:
    """Qué documentos tiene que citar una respuesta para que la fuente sea correcta, y con qué modo.

    - dato / procedimiento: al menos uno de los documentos fuente.
    - cruce: todos los documentos destino (los que tienen el dato, no los que solo remiten), sin versiones reemplazadas.
    - contradiccion: los dos documentos en conflicto.
    - version: el documento vigente.
    """
    tipo, sub = pregunta["tipo"], pregunta.get("subtipo")
    if tipo == "sin_respuesta":
        return [], "no_aplica"
    hs = [HECHOS[h] for h in pregunta["hechos"] if h in HECHOS]
    if sub == "version":
        return sorted({h["documento"] for h in hs if h["reemplazado"] == "no"}), "todos"
    if tipo == "cruce":
        destino = sorted({h["documento"] for h in hs if h["tipo"] != "referencia_cruzada" and h["reemplazado"] == "no"})
        return (destino or sorted(pregunta["documentos_fuente"])), "todos"
    if sub == "contradiccion":
        return sorted(pregunta["documentos_fuente"]), "todos"
    return sorted(pregunta["documentos_fuente"]), "al_menos_uno"


def fuente_exacta(pregunta: dict, citadas: list[str]) -> str:
    """Control determinístico de la etiqueta fuente (sin LLM). Mismo criterio que la rúbrica."""
    necesarias, modo = documentos_requeridos(pregunta)
    if modo == "no_aplica":
        return "no_aplica"
    necesarias, citadas = set(necesarias), set(citadas)
    if (necesarias <= citadas) if modo == "todos" else (necesarias & citadas):
        return "correcta"
    return "parcial" if (citadas & set(pregunta["documentos_fuente"])) else "incorrecta"


def mensaje_juez(pregunta: dict, respuesta: dict) -> str:
    caso = {
        "pregunta": pregunta["pregunta"],
        "tipo": pregunta["tipo"],
        "subtipo": pregunta.get("subtipo"),
        "respuesta_referencia": pregunta["respuesta_referencia"],
        "elementos_clave": pregunta["elementos_clave"],
        "comportamiento_esperado": pregunta["comportamiento_esperado"],
        "documentos_fuente": pregunta["documentos_fuente"],
        "documentos_requeridos": documentos_requeridos(pregunta)[0],
        "modo_fuente": documentos_requeridos(pregunta)[1],
        "respuesta_evaluada": respuesta["respuesta"],
        "fuentes_citadas": respuesta.get("fuentes", []),
    }
    return "Evaluá este caso y devolvé el JSON pedido.\n\n" + json.dumps(caso, ensure_ascii=False, indent=2)


def juzgar(pregunta: dict, respuesta: dict, corrida: Corrida) -> dict:
    response, registro = llamar(
        "juez", pregunta["id"], corrida,
        modelo=config.modelo_juez(),
        max_tokens=8000,
        system=SISTEMA,
        messages=[{"role": "user", "content": mensaje_juez(pregunta, respuesta)}],
        output_config={"effort": config.esfuerzo(),
                       "format": {"type": "json_schema", "schema": ESQUEMA_JUICIO}},
    )
    datos = parsear_json(response)
    valido = (registro["stop_reason"] == "end_turn" and "_error" not in datos
              and datos.get("veredicto") in ("correcta", "parcial", "incorrecta"))
    return {
        "valido": valido,
        "id": respuesta["id"],
        "pregunta_id": pregunta["id"],
        "brazo": respuesta.get("brazo"),
        "veredicto": datos.get("veredicto"),
        "fuente": datos.get("fuente"),
        "justificacion": datos.get("justificacion", datos.get("_error")),
        "fuente_exacta": fuente_exacta(pregunta, respuesta.get("fuentes", [])),
        "modelo_juez": registro["modelo"],
        "costo_usd": registro["costo_usd"],
        "stop_reason": registro["stop_reason"],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--respuestas", type=Path, action="append", required=True)
    ap.add_argument("--salida", type=Path, required=True)
    args = ap.parse_args(argv)

    preguntas = {p["id"]: p for p in cargar_jsonl(PREGUNTAS)}
    respuestas = [r for ruta in args.respuestas for r in cargar_jsonl(ruta)]
    hechos = {j["id"] for j in cargar_jsonl(args.salida)} if args.salida.exists() else set()
    pendientes = [r for r in respuestas if r["id"] not in hechos]
    corrida = Corrida("juez")
    print(f"Juzgando {len(pendientes)} respuestas (ya juzgadas: {len(hechos)}) con {config.modelo_juez()}")
    with args.salida.open("a", encoding="utf-8") as f:
        for r in pendientes:
            j = juzgar(preguntas[r["pregunta_id"]], r, corrida)
            if not j.pop("valido"):
                print(f"  {r['id']}: juicio inválido (stop_reason={j['stop_reason']}); no se guarda, se reintenta en la próxima corrida")
                continue
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
            print(f"  {r['id']} ({r['pregunta_id']}): {j['veredicto']} / fuente {j['fuente']} (exacta: {j['fuente_exacta']})")
    print(f"Costo de la corrida: USD {corrida.gastado_usd:.4f} en {corrida.llamadas} llamadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
