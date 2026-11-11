"""Cliente de la API con log JSONL, costo por llamada y tope de presupuesto por corrida."""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from comun import config
from comun.precios import costo_usd

LOG_LLAMADAS = config.LOGS / "llamadas.jsonl"


class PresupuestoExcedido(RuntimeError):
    pass


@dataclass
class Corrida:
    """Agrupa las llamadas de una ejecución y corta si se pasa del presupuesto."""

    nombre: str
    presupuesto_usd: float = field(default_factory=config.presupuesto_usd)
    id: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6])
    gastado_usd: float = 0.0
    llamadas: int = 0

    def verificar(self) -> None:
        if self.gastado_usd >= self.presupuesto_usd:
            raise PresupuestoExcedido(
                f"Corrida '{self.nombre}': gastado USD {self.gastado_usd:.4f} >= presupuesto USD {self.presupuesto_usd:.2f}"
            )


_cliente: anthropic.Anthropic | None = None


def cliente() -> anthropic.Anthropic:
    global _cliente
    if _cliente is None:
        _cliente = anthropic.Anthropic(max_retries=4)
    return _cliente


def registro_desde_usage(brazo: str, pregunta_id: str | None, modelo: str, usage, latencia_s: float,
                         corrida: Corrida, stop_reason: str | None, request_id: str | None) -> dict:
    entrada = usage.input_tokens or 0
    salida = usage.output_tokens or 0
    escritura = getattr(usage, "cache_creation_input_tokens", 0) or 0
    lectura = getattr(usage, "cache_read_input_tokens", 0) or 0
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corrida": corrida.id,
        "corrida_nombre": corrida.nombre,
        "brazo": brazo,
        "pregunta": pregunta_id,
        "modelo": modelo,
        "tokens_entrada": entrada,
        "tokens_salida": salida,
        "tokens_cache_escritura": escritura,
        "tokens_cache_lectura": lectura,
        "costo_usd": round(costo_usd(modelo, entrada, salida, escritura, lectura), 8),
        "latencia_s": round(latencia_s, 3),
        "stop_reason": stop_reason,
        "request_id": request_id,
    }


def escribir_log(registro: dict, ruta: Path | None = None) -> None:
    ruta = ruta or LOG_LLAMADAS
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def llamar(brazo: str, pregunta_id: str | None, corrida: Corrida, *, modelo: str | None = None, **params):
    """Hace una llamada a messages.create, la registra y devuelve (response, registro).

    `params` se pasa tal cual a la API (system, messages, max_tokens, output_config, tools, ...).
    """
    corrida.verificar()
    modelo = modelo or config.modelo_respuesta()
    params.setdefault("max_tokens", 4000)
    inicio = time.perf_counter()
    response = cliente().messages.create(model=modelo, **params)
    latencia = time.perf_counter() - inicio
    registro = registro_desde_usage(brazo, pregunta_id, modelo, response.usage, latencia, corrida,
                                    response.stop_reason, getattr(response, "_request_id", None))
    escribir_log(registro)
    corrida.gastado_usd += registro["costo_usd"]
    corrida.llamadas += 1
    return response, registro
