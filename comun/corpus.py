"""Carga del corpus y formato para meterlo en un prompt."""
from __future__ import annotations

from pathlib import Path

from comun.config import CORPUS


def cargar_corpus(directorio: Path = CORPUS) -> list[tuple[str, str]]:
    """Lista de (archivo, texto), ordenada por nombre para que el prompt sea estable (caché)."""
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(directorio.glob("*.md"))]


def formatear_corpus(docs: list[tuple[str, str]]) -> str:
    """Todos los documentos, cada uno envuelto en una etiqueta con su nombre de archivo."""
    partes = [f'<documento archivo="{archivo}">\n{texto.strip()}\n</documento>' for archivo, texto in docs]
    return "\n\n".join(partes)
