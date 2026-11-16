"""Brazo 3: consulta a la wiki. Un agente navega wiki/ (sin acceso a corpus/) y responde con fuentes."""
from __future__ import annotations

from brazos.wiki.agente import sesion
from brazos.wiki.herramientas import Herramientas
from comun import config
from comun.formato import FORMATO_RESPUESTA, INSTRUCCIONES_FORMATO, normalizar_respuesta, parsear_json
from comun.llm import Corrida

NOMBRE = "wiki"
MAX_TURNOS = 8

SISTEMA = (
    "Sos un asistente que responde preguntas de empleados de Distribuidora Quebracho Azul S.A. "
    "usando únicamente la wiki interna en wiki/. No tenés acceso a los documentos originales. "
    "Empezá leyendo `wiki/index.md` y abrí solo las páginas necesarias. "
    "Las páginas citan sus fuentes como `[fuente: archivo.md]`: en `fuentes` poné esos nombres de archivo "
    "(no las rutas de la wiki). " + INSTRUCCIONES_FORMATO + "\n\nEsquema con el que está escrita la wiki:\n\n"
    + (config.RAIZ / "ESQUEMA.md").read_text(encoding="utf-8")
)


def responder(pregunta: dict, corrida: Corrida, brazo: str = NOMBRE) -> dict:
    h = Herramientas("consulta")
    r = sesion(brazo, pregunta["id"], corrida, h, SISTEMA, pregunta["pregunta"], MAX_TURNOS,
               output_config=FORMATO_RESPUESTA,
               mensaje_cierre="Llegaste al límite de páginas. Respondé ahora con lo que leíste, en el formato pedido.")
    datos = normalizar_respuesta(parsear_json(r.respuesta_final))
    return {**datos, "valido": r.stop_reason == "end_turn" and "error" not in datos,
            "stop_reason": r.stop_reason, "costo_usd": round(r.costo_usd, 8), "latencia_s": round(r.latencia_s, 3),
            "llamadas": r.turnos, "extra": {"max_prompt_tokens": r.max_prompt, "cortada": r.cortada}}
