"""Valida evals/preguntas.jsonl contra hechos.csv, el catálogo, los huecos y el corpus.

Uso:
    python scripts/validar_preguntas.py                         # evals/preguntas.jsonl, chequeo completo
    python scripts/validar_preguntas.py --archivo X --parcial   # un archivo parcial (sin chequear cantidades)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar_hechos import normalizar, patron_hecho  # noqa: E402

TIPOS = ["dato", "procedimiento", "cruce", "contradiccion_version", "sin_respuesta"]
POR_TIPO = 10
SUBTIPOS_CV = {"contradiccion": 5, "version": 5}
CAMPOS = ["id", "tipo", "subtipo", "pregunta", "respuesta_referencia", "elementos_clave",
          "documentos_fuente", "hechos", "comportamiento_esperado", "hueco"]


def grupos(h: dict) -> set[str]:
    return {g.strip() for g in h["grupo"].split(";") if g.strip()}


def validar(raiz: Path, archivo: Path, parcial: bool = False, actualizacion: bool = False) -> tuple[list[str], list[str], dict]:
    errores: list[str] = []
    avisos: list[str] = []
    hechos = {h["hecho_id"]: h for h in csv.DictReader((raiz / "hechos.csv").open(encoding="utf-8"))}
    catalogo = {c["archivo"] for c in csv.DictReader((raiz / "diseno" / "catalogo.csv").open(encoding="utf-8"))}
    huecos = {h["hueco_id"] for h in csv.DictReader((raiz / "diseno" / "huecos.csv").open(encoding="utf-8"))}
    textos = {p.name: normalizar(p.read_text(encoding="utf-8")) for p in (raiz / "corpus").glob("*.md")}

    preguntas = []
    for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        try:
            preguntas.append(json.loads(linea))
        except json.JSONDecodeError as e:
            errores.append(f"línea {n}: JSON inválido ({e})")
    ids = Counter(p.get("id") for p in preguntas)
    for i, c in ids.items():
        if c > 1:
            errores.append(f"{i}: id duplicado")

    for p in preguntas:
        pid = p.get("id", "?")
        faltan = [c for c in CAMPOS if c not in p]
        if faltan:
            errores.append(f"{pid}: faltan campos {faltan}")
            continue
        if not re.fullmatch(r"U\d{2}" if actualizacion else r"P\d{2}", pid):
            errores.append(f"{pid}: id con formato inválido ({'U01..U10' if actualizacion else 'P01..P50'})")
        tipo = p["tipo"]
        if tipo not in TIPOS:
            errores.append(f"{pid}: tipo inválido '{tipo}'")
            continue
        if tipo == "contradiccion_version":
            if p["subtipo"] not in SUBTIPOS_CV:
                errores.append(f"{pid}: subtipo debe ser contradiccion o version")
        elif p["subtipo"] is not None:
            errores.append(f"{pid}: subtipo solo aplica a contradiccion_version (usar null)")
        for c in ("pregunta", "respuesta_referencia", "comportamiento_esperado"):
            if not str(p[c]).strip():
                errores.append(f"{pid}: {c} vacío")
        docs, hs, claves = p["documentos_fuente"], p["hechos"], p["elementos_clave"]
        if not all(isinstance(x, list) for x in (docs, hs, claves)):
            errores.append(f"{pid}: documentos_fuente, hechos y elementos_clave deben ser listas")
            continue
        for d in docs:
            if d not in catalogo:
                errores.append(f"{pid}: documento '{d}' no está en el catálogo")
        for hid in hs:
            if hid not in hechos:
                errores.append(f"{pid}: hecho {hid} no existe")
            elif hechos[hid]["documento"] not in docs:
                errores.append(f"{pid}: el documento de {hid} ({hechos[hid]['documento']}) no está en documentos_fuente")

        if tipo == "sin_respuesta":
            if p["hueco"] not in huecos:
                errores.append(f"{pid}: hueco '{p['hueco']}' inválido")
            if docs or hs or claves:
                errores.append(f"{pid}: sin_respuesta debe tener documentos_fuente, hechos y elementos_clave vacíos")
            continue
        if p["hueco"] is not None:
            errores.append(f"{pid}: hueco solo aplica a sin_respuesta (usar null)")
        if not docs or not hs or not claves:
            errores.append(f"{pid}: necesita documentos_fuente, hechos y elementos_clave")
            continue
        for clave in claves:
            pat = patron_hecho(clave)
            if not any(pat.search(textos.get(d, "")) for d in docs):
                errores.append(f"{pid}: elemento clave '{clave}' no aparece en sus documentos fuente")
            if normalizar(clave).lower() in normalizar(p["pregunta"]).lower() and len(clave) > 3:
                avisos.append(f"{pid}: la pregunta contiene literalmente el elemento clave '{clave}'")
        hs_info = [hechos[h] for h in hs if h in hechos]
        if tipo == "procedimiento" and len(claves) < 2:
            errores.append(f"{pid}: un procedimiento necesita al menos 2 elementos clave")
        if tipo == "cruce":
            if len(set(docs)) < 2:
                errores.append(f"{pid}: un cruce necesita al menos 2 documentos fuente")
            if not any(g.startswith("X") for h in hs_info for g in grupos(h)):
                avisos.append(f"{pid}: cruce sin ningún hecho de un grupo X")
        if tipo in ("dato", "procedimiento") and any(g[0] in "CV" for h in hs_info for g in grupos(h)):
            avisos.append(f"{pid}: usa un hecho de grupo C/V en una pregunta de tipo {tipo}")
        if tipo == "contradiccion_version" and p["subtipo"] == "contradiccion":
            cs = {g for h in hs_info for g in grupos(h) if g.startswith("C")}
            if len(cs) != 1:
                errores.append(f"{pid}: una contradicción debe referirse a exactamente un grupo C")
            else:
                g = cs.pop()
                miembros = [h for h in hechos.values() if g in grupos(h)]
                for m in miembros:
                    if m["documento"] not in docs:
                        errores.append(f"{pid}: falta el documento {m['documento']} del grupo {g}")
                    if m["texto"] not in claves:
                        errores.append(f"{pid}: el elemento clave debe incluir '{m['texto']}' ({g})")
        if tipo == "contradiccion_version" and p["subtipo"] == "version":
            vigentes = [h for h in hs_info if h["reemplazado"] == "no" and any(g.startswith("V") for g in grupos(h))]
            if not vigentes:
                errores.append(f"{pid}: una pregunta de versión necesita el hecho vigente de un grupo V")
            for h in hs_info:
                if h["reemplazado"] == "si" and h["texto"] in claves:
                    errores.append(f"{pid}: el valor viejo '{h['texto']}' no puede ser elemento clave")

    stats = {"preguntas": len(preguntas), **Counter(p.get("tipo") for p in preguntas)}
    if actualizacion and not parcial:
        if len(preguntas) != 10 or set(ids) != {f"U{i:02d}" for i in range(1, 11)}:
            errores.append(f"se esperaban 10 preguntas U01..U10, hay {len(preguntas)}")
    elif not parcial:
        if len(preguntas) != POR_TIPO * len(TIPOS):
            errores.append(f"hay {len(preguntas)} preguntas, se esperaban {POR_TIPO * len(TIPOS)}")
        for t in TIPOS:
            if stats.get(t, 0) != POR_TIPO:
                errores.append(f"tipo {t}: {stats.get(t, 0)} preguntas, se esperaban {POR_TIPO}")
        sub = Counter(p.get("subtipo") for p in preguntas if p.get("tipo") == "contradiccion_version")
        for s, n in SUBTIPOS_CV.items():
            if sub.get(s, 0) != n:
                errores.append(f"contradiccion_version/{s}: {sub.get(s, 0)}, se esperaban {n}")
        cubiertos = {p.get("hueco") for p in preguntas if p.get("tipo") == "sin_respuesta"}
        if huecos - cubiertos:
            errores.append(f"huecos sin pregunta: {sorted(huecos - cubiertos)}")
        cs_cubiertos = {g for p in preguntas if p.get("subtipo") == "contradiccion"
                        for h in p.get("hechos", []) if h in hechos for g in grupos(hechos[h]) if g.startswith("C")}
        if len(cs_cubiertos) != 5:
            errores.append(f"contradicciones cubiertas: {sorted(cs_cubiertos)}, se esperaban C1-C5")
        esperados = {f"P{i:02d}" for i in range(1, 51)}
        if set(ids) != esperados:
            errores.append(f"ids faltantes o sobrantes: {sorted(esperados ^ set(ids))}")
    return errores, avisos, stats


def main(argv: list[str] | None = None) -> int:
    raiz = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", type=Path, default=raiz / "evals" / "preguntas.jsonl")
    ap.add_argument("--parcial", action="store_true")
    ap.add_argument("--actualizacion", action="store_true", help="valida evals/preguntas_actualizacion.jsonl (U01..U10)")
    args = ap.parse_args(argv)
    if args.actualizacion and args.archivo == raiz / "evals" / "preguntas.jsonl":
        args.archivo = raiz / "evals" / "preguntas_actualizacion.jsonl"
    errores, avisos, stats = validar(raiz, args.archivo, parcial=args.parcial, actualizacion=args.actualizacion)
    print(json.dumps(stats, ensure_ascii=False))
    for a in avisos:
        print(f"AVISO: {a}")
    for e in errores:
        print(f"ERROR: {e}")
    print("OK" if not errores else f"{len(errores)} errores")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
