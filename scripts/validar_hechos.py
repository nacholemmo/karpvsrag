"""Valida hechos.csv contra el catálogo y el corpus.

Uso:
    python scripts/validar_hechos.py                 # validación completa (criterio de cierre de la fase 1)
    python scripts/validar_hechos.py --parcial       # los documentos que faltan cuentan como pendientes
    python scripts/validar_hechos.py --parcial --tanda 2
    python scripts/validar_hechos.py --raiz otra/carpeta

Sale con código 1 si encuentra errores.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

CAMPOS_HECHOS = ["hecho_id", "texto", "documento", "area", "tipo", "reemplazado", "reemplazado_por", "grupo", "notas"]
CAMPOS_CATALOGO = ["doc_id", "archivo", "titulo", "area", "formato", "fecha", "autor",
                   "largo_objetivo_palabras", "prolijidad", "estilo", "tanda", "referencias_a", "notas"]
TIPOS = {"monto", "plazo", "porcentaje", "responsable", "paso_procedimiento", "excepcion",
         "referencia_cruzada", "version", "contradiccion", "seccion", "dato"}
CANTIDAD_CONTRADICCIONES = 5
CANTIDAD_DOCUMENTOS = 50


@dataclass
class Informe:
    errores: list[str] = field(default_factory=list)
    pendientes: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errores.append(msg)


def normalizar(texto: str) -> str:
    """Única normalización permitida: colapsar espacios en blanco (incluye saltos de línea)."""
    return re.sub(r"\s+", " ", texto)


def patron_hecho(texto: str) -> re.Pattern:
    """Match literal con límites de palabra en los bordes alfanuméricos.

    Así "8%" no matchea dentro de "18%" y "F8" no matchea dentro de "F80", pero "REC-" sí matchea en "REC-0001".
    """
    t = normalizar(texto)
    izq = r"(?<!\w)" if t[:1].isalnum() else ""
    der = r"(?!\w)" if t[-1:].isalnum() else ""
    return re.compile(izq + re.escape(t) + der)


def leer_csv(ruta: Path, campos: list[str], informe: Informe) -> list[dict]:
    if not ruta.exists():
        informe.error(f"No existe {ruta.name}")
        return []
    with ruta.open(encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        faltan = [c for c in campos if c not in (lector.fieldnames or [])]
        if faltan:
            informe.error(f"{ruta.name}: faltan columnas {faltan}")
            return []
        return list(lector)


def grupos_de(fila: dict) -> list[str]:
    return [g.strip() for g in fila["grupo"].split(";") if g.strip()]


def validar(raiz: Path, parcial: bool = False, tanda: str | None = None) -> tuple[Informe, dict]:
    inf = Informe()
    catalogo = leer_csv(raiz / "diseno" / "catalogo.csv", CAMPOS_CATALOGO, inf)
    hechos = leer_csv(raiz / "hechos.csv", CAMPOS_HECHOS, inf)
    corpus_dir = raiz / "corpus"
    stats: dict = {}
    if inf.errores:
        return inf, stats

    # --- Catálogo ---
    por_archivo = {}
    ids_cat = set()
    for c in catalogo:
        if c["doc_id"] in ids_cat:
            inf.error(f"catálogo: doc_id duplicado {c['doc_id']}")
        ids_cat.add(c["doc_id"])
        if c["archivo"] in por_archivo:
            inf.error(f"catálogo: archivo duplicado {c['archivo']}")
        por_archivo[c["archivo"]] = c
    if not parcial and len(catalogo) != CANTIDAD_DOCUMENTOS:
        inf.error(f"catálogo: tiene {len(catalogo)} documentos, se esperaban {CANTIDAD_DOCUMENTOS}")

    # --- Estructura de hechos ---
    por_id = {}
    for h in hechos:
        hid = h["hecho_id"]
        if hid in por_id:
            inf.error(f"{hid}: hecho_id duplicado")
        por_id[hid] = h
        if not h["texto"].strip():
            inf.error(f"{hid}: texto vacío")
        if h["tipo"] not in TIPOS:
            inf.error(f"{hid}: tipo inválido '{h['tipo']}'")
        if h["reemplazado"] not in {"si", "no"}:
            inf.error(f"{hid}: reemplazado debe ser si/no, es '{h['reemplazado']}'")
        if h["documento"] not in por_archivo:
            inf.error(f"{hid}: el documento '{h['documento']}' no está en el catálogo")
        elif h["area"] != por_archivo[h["documento"]]["area"]:
            inf.error(f"{hid}: área '{h['area']}' no coincide con la del catálogo")
        gs = grupos_de(h)
        if any(g.startswith("C") for g in gs) != (h["tipo"] == "contradiccion"):
            inf.error(f"{hid}: tipo 'contradiccion' y grupo C* deben ir juntos")
        if any(g.startswith("V") for g in gs) != (h["tipo"] == "version"):
            inf.error(f"{hid}: tipo 'version' y grupo V* deben ir juntos")
        for g in gs:
            if not re.fullmatch(r"[CVX]\d+", g):
                inf.error(f"{hid}: grupo con formato inválido '{g}'")

    # --- Reemplazos ---
    for h in hechos:
        hid, rp = h["hecho_id"], h["reemplazado_por"].strip()
        if h["reemplazado"] == "si":
            if not rp:
                inf.error(f"{hid}: reemplazado=si sin reemplazado_por")
            elif rp not in por_id:
                inf.error(f"{hid}: reemplazado_por apunta a {rp}, que no existe")
            else:
                nuevo = por_id[rp]
                if nuevo["reemplazado"] == "si":
                    inf.error(f"{hid}: su reemplazo {rp} también está reemplazado")
                if not set(grupos_de(h)) & set(grupos_de(nuevo)):
                    inf.error(f"{hid}: no comparte grupo V con su reemplazo {rp}")
                if nuevo["documento"] == h["documento"]:
                    # Válido solo en documentos revisados que conservan el valor viejo en su historial de cambios.
                    inf.avisos.append(f"{hid}: versión dentro del mismo documento ({h['documento']}, revisión)")
        elif rp:
            inf.error(f"{hid}: reemplazado=no pero tiene reemplazado_por")

    # --- Grupos ---
    miembros = defaultdict(list)
    for h in hechos:
        for g in grupos_de(h):
            miembros[g].append(h)
    contradicciones = sorted(g for g in miembros if g.startswith("C"))
    if len(contradicciones) != CANTIDAD_CONTRADICCIONES:
        inf.error(f"hay {len(contradicciones)} grupos de contradicción, se esperaban {CANTIDAD_CONTRADICCIONES}")
    for g in contradicciones:
        docs = {h["documento"] for h in miembros[g]}
        if len(docs) < 2:
            inf.error(f"{g}: la contradicción tiene que involucrar al menos 2 documentos")
        if any(h["reemplazado"] == "si" for h in miembros[g]):
            inf.error(f"{g}: una contradicción no puede tener hechos reemplazados (eso es una versión)")
    for g in sorted(x for x in miembros if x.startswith("V")):
        estados = {h["reemplazado"] for h in miembros[g]}
        if estados != {"si", "no"}:
            inf.error(f"{g}: un grupo de versión necesita al menos un hecho reemplazado y uno vigente")
    for g in sorted(x for x in miembros if x.startswith("X")):
        if len({h["documento"] for h in miembros[g]}) < 2:
            inf.error(f"{g}: un cruce tiene que involucrar al menos 2 documentos")

    # --- Cobertura catálogo <-> hechos ---
    con_hechos = {h["documento"] for h in hechos}
    for archivo in por_archivo:
        if archivo not in con_hechos:
            inf.error(f"{archivo}: está en el catálogo pero no tiene hechos")

    # --- Corpus ---
    existentes = {p.name for p in corpus_dir.glob("*.md")} if corpus_dir.exists() else set()
    for archivo in sorted(existentes - set(por_archivo)):
        inf.error(f"corpus/{archivo}: no está en el catálogo")

    en_alcance = {a for a, c in por_archivo.items() if tanda is None or c["tanda"] == tanda}
    if tanda is not None and not en_alcance:
        inf.error(f"no hay documentos en la tanda {tanda}")

    textos: dict[str, str] = {}
    for archivo in sorted(en_alcance):
        if archivo not in existentes:
            (inf.pendientes if parcial else inf.errores).append(f"corpus/{archivo}: no existe")
            continue
        textos[archivo] = normalizar((corpus_dir / archivo).read_text(encoding="utf-8"))

    verificados = 0
    for h in hechos:
        if h["documento"] not in textos:
            continue
        if patron_hecho(h["texto"]).search(textos[h["documento"]]):
            verificados += 1
        else:
            inf.error(f"{h['hecho_id']}: '{h['texto']}' no aparece (como palabra completa) en corpus/{h['documento']}")

    # --- Contradicciones: los documentos del par no deberían citarse entre sí ---
    for g in contradicciones:
        docs = sorted({h["documento"] for h in miembros[g]})
        for a in docs:
            for b in docs:
                if a != b and a in textos and b in por_archivo and por_archivo[b]["titulo"] in textos[a]:
                    inf.avisos.append(f"{g}: corpus/{a} menciona por título a '{por_archivo[b]['titulo']}'")

    # --- Huecos ---
    ruta_huecos = raiz / "diseno" / "huecos.csv"
    if ruta_huecos.exists():
        for hu in leer_csv(ruta_huecos, ["hueco_id", "tema", "documento_que_lo_roza", "que_dice", "que_no_dice"], inf):
            for d in (x.strip() for x in hu["documento_que_lo_roza"].split(";") if x.strip()):
                if d not in por_archivo:
                    inf.error(f"hueco {hu['hueco_id']}: el documento '{d}' no está en el catálogo")

    # --- Estadísticas ---
    palabras_total = chars_total = 0
    for archivo in sorted(existentes & set(por_archivo)):
        crudo = (corpus_dir / archivo).read_text(encoding="utf-8")
        palabras = len(crudo.split())
        palabras_total += palabras
        chars_total += len(crudo)
        objetivo = int(por_archivo[archivo]["largo_objetivo_palabras"])
        if archivo in en_alcance and not (0.6 * objetivo <= palabras <= 1.5 * objetivo):
            inf.avisos.append(f"corpus/{archivo}: {palabras} palabras (objetivo {objetivo})")
    stats = {
        "documentos_en_corpus": len(existentes),
        "hechos_totales": len(hechos),
        "hechos_verificados": verificados,
        "hechos_en_alcance": sum(1 for h in hechos if h["documento"] in en_alcance),
        "palabras_corpus": palabras_total,
        # Calibrado con count_tokens de Haiku 5.5 sobre este corpus (2,34 caracteres por token).
        # El valor exacto está en resultados/tokens_corpus.json (scripts/contar_tokens.py).
        "tokens_estimados": int(chars_total / 2.34),
        "contradicciones": len(contradicciones),
        "versiones": len([g for g in miembros if g.startswith("V")]),
        "cruces": len([g for g in miembros if g.startswith("X")]),
    }
    return inf, stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--parcial", action="store_true", help="los documentos faltantes cuentan como pendientes")
    ap.add_argument("--tanda", help="validar el texto solo de los documentos de esta tanda")
    args = ap.parse_args(argv)

    inf, stats = validar(args.raiz, parcial=args.parcial, tanda=args.tanda)
    for k, v in stats.items():
        print(f"{k}: {v}")
    if inf.avisos:
        print(f"\nAVISOS ({len(inf.avisos)}):")
        for a in inf.avisos:
            print(f"  - {a}")
    if inf.pendientes:
        print(f"\nPENDIENTES ({len(inf.pendientes)}): documentos todavía no escritos")
    if inf.errores:
        print(f"\nERRORES ({len(inf.errores)}):")
        for e in inf.errores:
            print(f"  - {e}")
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
