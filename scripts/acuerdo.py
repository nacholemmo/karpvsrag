"""Acuerdo entre la revisión manual y el juez sobre la muestra de 15.

Uso: python scripts/acuerdo.py   (lee evals/revision_manual.csv completado y evals/juicios_muestra.jsonl)
Escribe evals/acuerdo.md.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EVALS = RAIZ / "evals"
VEREDICTOS = ["correcta", "parcial", "incorrecta"]
FUENTES = ["correcta", "parcial", "incorrecta", "no_aplica"]


def leer_jsonl(ruta: Path) -> list[dict]:
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def kappa(pares: list[tuple[str, str]], categorias: list[str]) -> float | None:
    """Kappa de Cohen. None si no está definido (acuerdo esperado = 1)."""
    n = len(pares)
    if n == 0:
        return None
    po = sum(a == b for a, b in pares) / n
    ca, cb = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(ca[c] * cb[c] for c in categorias) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def matriz(pares: list[tuple[str, str]], categorias: list[str]) -> str:
    filas = ["| humano \\ juez | " + " | ".join(categorias) + " |", "|---" * (len(categorias) + 1) + "|"]
    for h in categorias:
        filas.append(f"| {h} | " + " | ".join(str(sum(1 for a, b in pares if a == h and b == j)) for j in categorias) + " |")
    return "\n".join(filas)


def resumen(nombre: str, pares: list[tuple[str, str]], categorias: list[str]) -> str:
    n = len(pares)
    acuerdo = sum(a == b for a, b in pares)
    k = kappa(pares, categorias)
    ktxt = "no definido" if k is None else f"{k:.2f}"
    return (f"### {nombre}\n\nAcuerdo: {acuerdo}/{n} ({acuerdo / n:.0%}). Kappa de Cohen: {ktxt}.\n\n"
            + matriz(pares, categorias) + "\n")


def main() -> int:
    revision = list(csv.DictReader((EVALS / "revision_manual.csv").open(encoding="utf-8")))
    mapa = json.loads((EVALS / "mapa_revision.json").read_text(encoding="utf-8"))
    por_id = {j["id"]: j for j in leer_jsonl(EVALS / "juicios_muestra.jsonl")}
    juicios = {caso: por_id[rid] for caso, rid in mapa.items() if rid in por_id}
    etiquetas = {}
    ruta_et = EVALS / "etiquetas_sinteticas.jsonl"
    if ruta_et.exists():
        et = {e["id"]: e for e in leer_jsonl(ruta_et)}
        etiquetas = {caso: et[rid] for caso, rid in mapa.items() if rid in et}

    incompletas = [r["caso"] for r in revision if r["tu_veredicto"].strip() not in VEREDICTOS
                   or r["tu_fuente"].strip() not in FUENTES]
    if incompletas:
        print(f"Faltan o son inválidas tus etiquetas en: {incompletas}")
        print(f"Valores válidos: tu_veredicto {VEREDICTOS}; tu_fuente {FUENTES}")
        return 1
    faltan_juicios = [r["caso"] for r in revision if r["caso"] not in juicios
                      or juicios[r["caso"]].get("veredicto") not in VEREDICTOS]
    if faltan_juicios:
        print(f"Faltan juicios para: {faltan_juicios}")
        return 1

    pv = [(r["tu_veredicto"].strip(), juicios[r["caso"]]["veredicto"]) for r in revision]
    pf = [(r["tu_fuente"].strip(), juicios[r["caso"]]["fuente"]) for r in revision]
    pfx = [(r["tu_fuente"].strip(), juicios[r["caso"]]["fuente_exacta"]) for r in revision]
    partes = ["# Acuerdo humano vs. juez (muestra de 15)\n",
              f"Juez: {next(iter(juicios.values()))['modelo_juez']}. Casos: {len(revision)}.\n",
              resumen("Veredicto (humano vs. juez)", pv, VEREDICTOS),
              resumen("Fuente (humano vs. juez)", pf, FUENTES),
              resumen("Fuente (humano vs. control en código `fuente_exacta`)", pfx, FUENTES)]

    if etiquetas:
        lineas = ["### Respuestas sintéticas (etiqueta pretendida al escribirlas)\n",
                  "| caso | pretendida | humano | juez |", "|---|---|---|---|"]
        for r in revision:
            if r["caso"] in etiquetas:
                lineas.append(f"| {r['caso']} ({mapa[r['caso']]}) | {etiquetas[r['caso']]['veredicto']} | {r['tu_veredicto']} | "
                              f"{juicios[r['caso']]['veredicto']} |")
        partes.append("\n".join(lineas) + "\n")

    desacuerdos = [r for r in revision if r["tu_veredicto"].strip() != juicios[r["caso"]]["veredicto"]]
    if desacuerdos:
        lineas = ["### Desacuerdos de veredicto\n"]
        for r in desacuerdos:
            j = juicios[r["caso"]]
            lineas.append(f"- **{r['caso']}** ({r['tipo']}): humano `{r['tu_veredicto']}`, juez `{j['veredicto']}`. "
                          f"Juez: {j['justificacion']}" + (f" Notas: {r['notas']}" if r["notas"].strip() else ""))
        partes.append("\n".join(lineas) + "\n")

    salida = EVALS / "acuerdo.md"
    salida.write_text("\n".join(partes), encoding="utf-8")
    print(salida.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
