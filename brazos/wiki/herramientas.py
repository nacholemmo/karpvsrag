"""Herramientas de archivos del agente de la wiki: listar, leer, escribir.

Rutas relativas a la raíz del repo (por ejemplo `wiki/index.md` o `corpus/manual-deposito.md`).
Cada modo define qué raíces se pueden leer y escribir. Nunca se puede escribir fuera de wiki/.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from comun import config

MAX_CARACTERES = 12_000


class RutaInvalida(ValueError):
    pass


@dataclass(frozen=True)
class Permisos:
    lectura: tuple[str, ...]
    escritura: tuple[str, ...] = ()


MODOS = {
    "ingesta": Permisos(lectura=("corpus", "wiki"), escritura=("wiki",)),
    "lint": Permisos(lectura=("corpus", "wiki"), escritura=("wiki",)),
    "consulta": Permisos(lectura=("wiki",)),
}

ESQUEMAS = {
    "listar": {
        "name": "listar",
        "description": "Lista los archivos y carpetas dentro de una carpeta (por ejemplo `wiki` o `wiki/proceso`).",
        "strict": True,
        "input_schema": {"type": "object", "properties": {"ruta": {"type": "string"}},
                         "required": ["ruta"], "additionalProperties": False},
    },
    "leer": {
        "name": "leer",
        "description": "Lee un archivo de texto (por ejemplo `wiki/index.md`). Los archivos muy largos se truncan.",
        "strict": True,
        "input_schema": {"type": "object", "properties": {"ruta": {"type": "string"}},
                         "required": ["ruta"], "additionalProperties": False},
    },
    "escribir": {
        "name": "escribir",
        "description": "Crea o reemplaza por completo un archivo Markdown dentro de `wiki/`. Pasá el contenido completo.",
        "strict": True,
        "input_schema": {"type": "object", "properties": {"ruta": {"type": "string"}, "contenido": {"type": "string"}},
                         "required": ["ruta", "contenido"], "additionalProperties": False},
    },
}


class Herramientas:
    def __init__(self, modo: str, raiz: Path = config.RAIZ):
        self.permisos = MODOS[modo]
        self.raiz = raiz.resolve()
        self.escritos: list[str] = []

    def definiciones(self) -> list[dict]:
        nombres = ["listar", "leer"] + (["escribir"] if self.permisos.escritura else [])
        return [ESQUEMAS[n] for n in nombres]

    def _resolver(self, ruta: str, raices: tuple[str, ...]) -> Path:
        if not ruta or Path(ruta).is_absolute() or ".." in Path(ruta).parts:
            raise RutaInvalida(f"Ruta inválida: {ruta!r}. Usá rutas relativas como wiki/index.md")
        destino = (self.raiz / ruta).resolve()
        for r in raices:
            base = (self.raiz / r).resolve()
            if destino == base or base in destino.parents:
                return destino
        raise RutaInvalida(f"Ruta fuera de las carpetas permitidas {list(raices)}: {ruta!r}")

    def listar(self, ruta: str) -> str:
        p = self._resolver(ruta, self.permisos.lectura)
        if not p.is_dir():
            return f"No existe la carpeta {ruta}"
        items = sorted(p.iterdir())
        lineas = [f"{x.relative_to(self.raiz)}{'/' if x.is_dir() else ''}" for x in items if not x.name.startswith(".")]
        return "\n".join(lineas) or "(vacía)"

    def leer(self, ruta: str) -> str:
        p = self._resolver(ruta, self.permisos.lectura)
        if not p.is_file():
            return f"No existe el archivo {ruta}"
        texto = p.read_text(encoding="utf-8")
        if len(texto) > MAX_CARACTERES:
            return texto[:MAX_CARACTERES] + f"\n\n[... truncado: el archivo tiene {len(texto)} caracteres]"
        return texto

    def escribir(self, ruta: str, contenido: str) -> str:
        if not self.permisos.escritura:
            raise RutaInvalida("Este modo no permite escribir")
        p = self._resolver(ruta, self.permisos.escritura)
        if p.suffix != ".md":
            raise RutaInvalida("Solo se pueden escribir archivos .md")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contenido, encoding="utf-8")
        self.escritos.append(str(p.relative_to(self.raiz)))
        return f"Escrito {p.relative_to(self.raiz)} ({len(contenido)} caracteres)"

    def ejecutar(self, nombre: str, entrada: dict) -> tuple[str, bool]:
        """Devuelve (resultado, es_error)."""
        try:
            if nombre not in {d["name"] for d in self.definiciones()}:
                return f"Herramienta no disponible: {nombre}", True
            return getattr(self, nombre)(**entrada), False
        except (RutaInvalida, TypeError) as e:
            return str(e), True
