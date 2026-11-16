"""Bucle de agente con herramientas de archivos (manual, sin beta). Cada turno se registra con comun.llm.llamar."""
from __future__ import annotations

from dataclasses import dataclass, field

from brazos.wiki.herramientas import Herramientas
from comun import config
from comun.llm import Corrida, llamar

# Haiku 5.5 cobra 5x por encima de 100k tokens de prompt: si una sesión se acerca, se le pide que cierre.
LIMITE_PROMPT = 70_000


@dataclass
class ResultadoSesion:
    respuesta_final: object = None  # último response de la API
    turnos: int = 0
    costo_usd: float = 0.0
    latencia_s: float = 0.0
    max_prompt: int = 0
    cortada: str | None = None  # motivo si se cortó por tope de turnos o de contexto
    stop_reason: str | None = None
    escritos: list[str] = field(default_factory=list)


def sesion(brazo: str, etiqueta: str, corrida: Corrida, herramientas: Herramientas, sistema: str,
           mensaje: str, max_turnos: int, output_config: dict | None = None,
           mensaje_cierre: str = "Llegaste al límite de esta sesión. Terminá ahora sin usar más herramientas.") -> ResultadoSesion:
    """Corre el bucle: modelo -> tool_use -> tool_result -> ... hasta end_turn o un tope."""
    res = ResultadoSesion()
    mensajes: list = [{"role": "user", "content": mensaje}]
    oc = {"effort": config.esfuerzo(), **(output_config or {})}
    cerrar = False
    while True:
        params = dict(
            max_tokens=16000,
            system=[{"type": "text", "text": sistema, "cache_control": {"type": "ephemeral"}}],
            messages=mensajes,
            tools=herramientas.definiciones(),
            tool_choice={"type": "none"} if cerrar else {"type": "auto"},
            cache_control={"type": "ephemeral"},
            output_config=oc,
        )
        response, reg = llamar(brazo, etiqueta, corrida, **params)
        res.turnos += 1
        res.costo_usd += reg["costo_usd"]
        res.latencia_s += reg["latencia_s"]
        prompt = reg["tokens_entrada"] + reg["tokens_cache_escritura"] + reg["tokens_cache_lectura"]
        res.max_prompt = max(res.max_prompt, prompt)
        res.respuesta_final, res.stop_reason = response, response.stop_reason
        mensajes.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            break
        resultados = []
        for b in response.content:
            if getattr(b, "type", None) == "tool_use":
                salida, es_error = herramientas.ejecutar(b.name, dict(b.input))
                resultados.append({"type": "tool_result", "tool_use_id": b.id, "content": salida, "is_error": es_error})
        if cerrar:  # ya se pidió cerrar y aun así pidió herramientas
            res.cortada = res.cortada or "no cerró"
            break
        if res.turnos >= max_turnos or prompt >= LIMITE_PROMPT:
            res.cortada = "turnos" if res.turnos >= max_turnos else "contexto"
            cerrar = True
            resultados.append({"type": "text", "text": mensaje_cierre})
        mensajes.append({"role": "user", "content": resultados})
    res.escritos = list(herramientas.escritos)
    return res
