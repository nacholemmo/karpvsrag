"""Formato común de salida de los tres brazos: respuesta + fuentes citadas."""
from __future__ import annotations

import json

ESQUEMA_RESPUESTA = {
    "type": "object",
    "properties": {
        "respuesta": {"type": "string"},
        "fuentes": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["respuesta", "fuentes"],
    "additionalProperties": False,
}

FORMATO_RESPUESTA = {"format": {"type": "json_schema", "schema": ESQUEMA_RESPUESTA}}

INSTRUCCIONES_FORMATO = (
    "Respondé en español, de forma breve y precisa. En `fuentes` poné los nombres de archivo exactos "
    "(por ejemplo `manual-deposito.md`) de los documentos de donde sacaste la respuesta. "
    "Si la información no figura en los documentos, decilo explícitamente en `respuesta` y dejá `fuentes` vacío. "
    "Si dos documentos vigentes se contradicen, mencioná ambos valores y ambos documentos. "
    "Si hay una versión vieja y una nueva de un proceso, respondé con la vigente."
)


def texto_de(response) -> str:
    return "".join(b.text for b in response.content if getattr(b, "type", None) == "text")


def parsear_json(response) -> dict:
    """Devuelve el JSON del primer bloque de texto. Si no se puede parsear, devuelve un dict con el error."""
    texto = texto_de(response)
    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        return {"_error": f"JSON inválido: {e}", "_texto": texto}


def normalizar_respuesta(datos: dict) -> dict:
    """Asegura el formato {respuesta, fuentes}, con fuentes como lista de nombres de archivo sin ruta."""
    fuentes = datos.get("fuentes") or []
    fuentes = [str(f).strip().split("/")[-1] for f in fuentes if str(f).strip()]
    return {"respuesta": str(datos.get("respuesta", datos.get("_texto", ""))), "fuentes": fuentes,
            **({"error": datos["_error"]} if "_error" in datos else {})}
