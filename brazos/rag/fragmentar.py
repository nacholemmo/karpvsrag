"""Fragmentación del corpus por secciones Markdown.

- Corta en cada título `#`, `##` o `###`. El fragmento lleva la ruta de títulos como contexto.
- Una sección de más de MAX_PALABRAS se subdivide por párrafos, con solapamiento de 1 párrafo.
- Los documentos sin títulos (mails, notas) se cortan en ventanas de párrafos.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

MAX_PALABRAS = 350
TITULO = re.compile(r"^(#{1,3})\s+(.*\S)\s*$")


@dataclass
class Fragmento:
    id: str
    archivo: str
    titulo_doc: str
    seccion: str
    texto: str

    @property
    def texto_indexado(self) -> str:
        cabecera = self.titulo_doc + (f" > {self.seccion}" if self.seccion else "")
        return f"{cabecera}\n{self.texto}"

    def dict(self) -> dict:
        return asdict(self)


def _parrafos(lineas: list[str]) -> list[str]:
    bloques, actual = [], []
    for l in lineas:
        if l.strip():
            actual.append(l.rstrip())
        elif actual:
            bloques.append("\n".join(actual))
            actual = []
    if actual:
        bloques.append("\n".join(actual))
    return bloques


def _ventanas(parrafos: list[str], max_palabras: int = MAX_PALABRAS) -> list[str]:
    """Agrupa párrafos en ventanas de hasta max_palabras, repitiendo el último párrafo de la ventana anterior."""
    if not parrafos:
        return []
    ventanas, actual, n = [], [], 0
    for p in parrafos:
        w = len(p.split())
        if actual and n + w > max_palabras:
            ventanas.append("\n\n".join(actual))
            actual, n = [actual[-1]], len(actual[-1].split())  # solapamiento de 1 párrafo
        actual.append(p)
        n += w
    ventanas.append("\n\n".join(actual))
    return ventanas


def fragmentar_documento(archivo: str, texto: str) -> list[Fragmento]:
    lineas = texto.splitlines()
    titulo_doc = archivo
    for l in lineas:
        m = TITULO.match(l)
        if m and len(m.group(1)) == 1:
            titulo_doc = m.group(2)
            break
    # Secciones: (ruta de títulos, líneas)
    secciones: list[tuple[str, list[str]]] = []
    ruta: list[tuple[int, str]] = []
    actuales: list[str] = []
    for l in lineas:
        m = TITULO.match(l)
        if m:
            secciones.append((" > ".join(t for _, t in ruta), actuales))
            nivel = len(m.group(1))
            ruta = [(n, t) for n, t in ruta if n < nivel] + [(nivel, m.group(2))]
            actuales = []
        else:
            actuales.append(l)
    secciones.append((" > ".join(t for _, t in ruta), actuales))

    frags: list[Fragmento] = []
    for seccion, ls in secciones:
        for v in _ventanas(_parrafos(ls)):
            frags.append(Fragmento(f"{archivo}#{len(frags)}", archivo, titulo_doc, seccion, v))
    return frags


def fragmentar_corpus(docs: list[tuple[str, str]]) -> list[Fragmento]:
    return [f for archivo, texto in docs for f in fragmentar_documento(archivo, texto)]
