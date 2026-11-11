"""Precios por millón de tokens (USD) y cálculo de costo de una llamada.

Fuente: tabla de modelos de la documentación de la API de Anthropic (noviembre 2026).
- Escritura de caché (TTL 5 min): 1,25 × precio de entrada.
- Lectura de caché: 0,1 × entrada en general; 0,05 × en Opus 5.5 y Sonnet 5.5.
- Haiku 5.5 cobra un tramo más caro cuando el prompt supera los 100k tokens.
  Acá se toma como "prompt" la suma de entrada sin caché + escritura + lectura de caché.
"""
from __future__ import annotations

from dataclasses import dataclass

ESCRITURA_CACHE = 1.25


@dataclass(frozen=True)
class Precio:
    entrada: float
    salida: float
    lectura_cache: float  # multiplicador sobre `entrada`
    # Tramo caro opcional: (umbral de tokens de prompt, entrada, salida)
    tramo_largo: tuple[int, float, float] | None = None


PRECIOS: dict[str, Precio] = {
    "claude-haiku-5-5": Precio(0.10, 0.50, 0.10, tramo_largo=(100_000, 0.50, 2.50)),
    "claude-sonnet-5-5": Precio(2.00, 10.00, 0.05),
    "claude-opus-5-5": Precio(4.00, 20.00, 0.05),
}


def costo_usd(modelo: str, entrada: int, salida: int, cache_escritura: int = 0, cache_lectura: int = 0) -> float:
    """Costo de una llamada a partir de los tokens de `response.usage`."""
    if modelo not in PRECIOS:
        raise KeyError(f"Modelo sin precio cargado: {modelo}. Agregalo en comun/precios.py")
    p = PRECIOS[modelo]
    precio_in, precio_out = p.entrada, p.salida
    prompt = entrada + cache_escritura + cache_lectura
    if p.tramo_largo and prompt > p.tramo_largo[0]:
        _, precio_in, precio_out = p.tramo_largo
    total = (
        entrada * precio_in
        + cache_escritura * precio_in * ESCRITURA_CACHE
        + cache_lectura * precio_in * p.lectura_cache
        + salida * precio_out
    )
    return total / 1_000_000
