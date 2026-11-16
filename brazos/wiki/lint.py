"""Lint de la wiki: chequeos en código (gratis) y, opcionalmente, un agente que corrige lo encontrado.

Uso:
    python brazos/wiki/lint.py                 # solo chequeos en código; sale con 1 si hay errores
    python brazos/wiki/lint.py --corregir      # además, un agente corrige los errores (usa la API)

Chequeos:
- enlaces internos rotos;
- páginas sin ninguna cita `[fuente: x.md]` (salvo index.md);
- citas a archivos que no existen en corpus/;
- páginas que no están en index.md;
- datos duros (montos, porcentajes, horarios) de una línea que no aparecen textuales en ninguno de los documentos citados en esa línea.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from comun import config  # noqa: E402
from validar_hechos import normalizar, patron_hecho  # noqa: E402

ENLACE = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
CITA = re.compile(r"\[fuente:\s*([^\]\s]+\.md)\s*\]")
DATO_DURO = re.compile(r"\$ ?\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+(?:,\d+)?\s?%|\b\d{1,2}:\d{2}\b")
MAX_TURNOS_CORRECCION = 25


def chequear(wiki: Path, corpus: Path) -> list[str]:
    errores: list[str] = []
    paginas = sorted(p for p in wiki.rglob("*.md"))
    if not paginas:
        return ["la wiki está vacía"]
    textos_corpus = {p.name: normalizar(p.read_text(encoding="utf-8")) for p in corpus.glob("*.md")}
    indice = wiki / "index.md"
    enlazadas_desde_indice: set[Path] = set()
    if not indice.exists():
        errores.append("falta wiki/index.md")
    for p in paginas:
        rel = p.relative_to(wiki)
        texto = p.read_text(encoding="utf-8")
        for destino in ENLACE.findall(texto):
            if destino.startswith(("http://", "https://")):
                continue
            objetivo = (p.parent / destino).resolve()
            if not objetivo.exists():
                errores.append(f"{rel}: enlace roto a {destino}")
            elif p == indice:
                enlazadas_desde_indice.add(objetivo)
        citas = CITA.findall(texto)
        if p != indice and not citas:
            errores.append(f"{rel}: no tiene ninguna cita [fuente: ...]")
        for c in set(citas):
            if c not in textos_corpus:
                errores.append(f"{rel}: cita un archivo inexistente: {c}")
        for n, linea in enumerate(texto.splitlines(), 1):
            fuentes = [c for c in CITA.findall(linea) if c in textos_corpus]
            if not fuentes:
                continue
            for dato in set(DATO_DURO.findall(linea)):
                pat = patron_hecho(dato.strip())
                if not any(pat.search(textos_corpus[f]) for f in fuentes):
                    errores.append(f"{rel}:{n}: el dato '{dato.strip()}' no aparece textual en {fuentes}")
    for p in paginas:
        if p != indice and p.resolve() not in enlazadas_desde_indice:
            errores.append(f"{p.relative_to(wiki)}: no está en index.md")
    return errores


SISTEMA_LINT = (
    "Sos el agente que mantiene la wiki interna de Distribuidora Quebracho Azul S.A. Vas a corregir errores "
    "detectados por un chequeo automático. Podés leer corpus/ para verificar datos, pero solo podés escribir en wiki/. "
    "Seguí este esquema:\n\n" + (config.RAIZ / "ESQUEMA.md").read_text(encoding="utf-8")
)


def corregir(errores: list[str]) -> dict:
    from brazos.wiki.agente import sesion
    from brazos.wiki.herramientas import Herramientas
    from comun.llm import Corrida

    corrida = Corrida("wiki_lint")
    lista = "\n".join(f"- {e}" for e in errores[:60])
    mensaje = (f"El chequeo automático de la wiki encontró estos errores:\n\n{lista}\n\n"
               "Corregilos. Para un dato que no aparece textual, abrí el documento citado y copiá el valor exacto, "
               "o corregí la cita si el dato está en otro documento. Agregá al índice las páginas que falten. "
               "Reescribí cada página completa al corregirla. Cuando termines, resumí en dos líneas lo que cambiaste.")
    r = sesion("wiki_lint", "lint", corrida, Herramientas("lint"), SISTEMA_LINT, mensaje, MAX_TURNOS_CORRECCION)
    return {"costo_usd": round(r.costo_usd, 6), "turnos": r.turnos, "cortada": r.cortada, "escritos": sorted(set(r.escritos))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corregir", action="store_true")
    args = ap.parse_args(argv)
    wiki, corpus = config.RAIZ / "wiki", config.CORPUS
    errores = chequear(wiki, corpus)
    print(f"Chequeo en código: {len(errores)} errores")
    for e in errores:
        print(f"  - {e}")
    if args.corregir and errores:
        antes = len(errores)
        res = corregir(errores)
        print(f"Corrección con agente: {json.dumps(res, ensure_ascii=False)}")
        errores = chequear(wiki, corpus)
        print(f"Después de corregir: {len(errores)} errores")
        registro = config.RAIZ / "resultados" / "lint_wiki.json"
        historial = json.loads(registro.read_text(encoding="utf-8")) if registro.exists() else []
        from datetime import datetime, timezone
        historial.append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                          "errores_antes": antes, "errores_despues": len(errores), **res})
        registro.write_text(json.dumps(historial, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for e in errores:
            print(f"  - {e}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
