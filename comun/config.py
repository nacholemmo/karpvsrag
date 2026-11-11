"""Configuración por variables de entorno (o `.env` en la raíz del repo, que no se versiona)."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "corpus"
LOGS = RAIZ / "logs"

# Las variables ya definidas en el entorno tienen prioridad sobre el .env.
load_dotenv(RAIZ / ".env", override=False)

MODELO_POR_DEFECTO = "claude-haiku-5-5"


def modelo_respuesta() -> str:
    return os.environ.get("MODELO_RESPUESTA") or MODELO_POR_DEFECTO


def modelo_juez() -> str:
    return os.environ.get("MODELO_JUEZ") or MODELO_POR_DEFECTO


def esfuerzo() -> str:
    """Nivel de effort (low/medium/high/xhigh/max) para las respuestas y el juez."""
    return os.environ.get("ESFUERZO") or "low"


def presupuesto_usd() -> float:
    """Tope de gasto por corrida. Si se supera, la corrida se corta con error."""
    return float(os.environ.get("PRESUPUESTO_USD") or "0.50")
