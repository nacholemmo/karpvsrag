"""Brazo 1: contexto completo. Todo el corpus va en el system prompt (con caché) y se hace una sola llamada."""
from __future__ import annotations

from comun import config
from comun.corpus import cargar_corpus, formatear_corpus
from comun.formato import FORMATO_RESPUESTA, INSTRUCCIONES_FORMATO, normalizar_respuesta, parsear_json
from comun.llm import Corrida, llamar

NOMBRE = "contexto"

SISTEMA = (
    "Sos un asistente que responde preguntas de empleados de Distribuidora Quebracho Azul S.A. "
    "usando únicamente los documentos internos que siguen. " + INSTRUCCIONES_FORMATO
)

_sistema_cache: list[dict] | None = None


def sistema_con_corpus() -> list[dict]:
    """System prompt estable (mismo texto byte a byte en cada llamada) para que la caché funcione."""
    global _sistema_cache
    if _sistema_cache is None:
        corpus = formatear_corpus(cargar_corpus())
        _sistema_cache = [
            {"type": "text", "text": SISTEMA},
            {"type": "text", "text": f"<corpus>\n{corpus}\n</corpus>", "cache_control": {"type": "ephemeral"}},
        ]
    return _sistema_cache


def responder(pregunta: dict, corrida: Corrida, brazo: str = NOMBRE) -> dict:
    response, reg = llamar(
        brazo, pregunta["id"], corrida,
        max_tokens=8000,
        system=sistema_con_corpus(),
        messages=[{"role": "user", "content": pregunta["pregunta"]}],
        output_config={"effort": config.esfuerzo(), **FORMATO_RESPUESTA},
    )
    r = normalizar_respuesta(parsear_json(response))
    return {**r, "valido": reg["stop_reason"] == "end_turn" and "error" not in r,
            "stop_reason": reg["stop_reason"], "costo_usd": reg["costo_usd"],
            "latencia_s": reg["latencia_s"], "llamadas": 1, "extra": {}}
