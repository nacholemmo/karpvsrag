"""Tests de costo, log y formato sin llamar a la API."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comun import llm  # noqa: E402
from comun.formato import normalizar_respuesta, parsear_json  # noqa: E402
from comun.precios import costo_usd  # noqa: E402


def test_costo_haiku_tramo_corto():
    # 50k entrada a $0,10/M + 1k salida a $0,50/M
    assert costo_usd("claude-haiku-5-5", 50_000, 1_000) == pytest.approx(0.005 + 0.0005)


def test_costo_haiku_tramo_largo():
    # 120k de prompt supera el umbral: $0,50/M entrada y $2,50/M salida
    assert costo_usd("claude-haiku-5-5", 120_000, 1_000) == pytest.approx(0.06 + 0.0025)


def test_costo_con_cache():
    # 80k leídos de caché (0,1×) + 1k entrada + 500 salida
    c = costo_usd("claude-haiku-5-5", 1_000, 500, cache_lectura=80_000)
    assert c == pytest.approx((1_000 * 0.10 + 80_000 * 0.01 + 500 * 0.50) / 1e6)
    # escritura de caché a 1,25×
    c2 = costo_usd("claude-haiku-5-5", 0, 0, cache_escritura=80_000)
    assert c2 == pytest.approx(80_000 * 0.125 / 1e6)


def test_el_umbral_cuenta_los_tokens_de_cache():
    corto = costo_usd("claude-haiku-5-5", 1_000, 0, cache_lectura=98_000)
    largo = costo_usd("claude-haiku-5-5", 1_000, 0, cache_lectura=100_000)
    assert largo > corto * 4


def test_modelo_desconocido_falla():
    with pytest.raises(KeyError):
        costo_usd("modelo-inexistente", 1, 1)


class ClienteFalso:
    def __init__(self, usage):
        self.messages = SimpleNamespace(create=self._create)
        self.usage = usage

    def _create(self, **kw):
        return SimpleNamespace(usage=self.usage, stop_reason="end_turn", content=[], _request_id="req_x")


def test_llamar_registra_y_acumula(tmp_path, monkeypatch):
    usage = SimpleNamespace(input_tokens=1000, output_tokens=200, cache_creation_input_tokens=0, cache_read_input_tokens=0)
    monkeypatch.setattr(llm, "_cliente", ClienteFalso(usage))
    log = tmp_path / "l.jsonl"
    monkeypatch.setattr(llm, "LOG_LLAMADAS", log)
    corrida = llm.Corrida("test", presupuesto_usd=1.0)
    _, reg = llm.llamar("contexto", "P01", corrida, modelo="claude-haiku-5-5", messages=[])
    assert reg["brazo"] == "contexto" and reg["pregunta"] == "P01"
    assert reg["costo_usd"] == pytest.approx((1000 * 0.10 + 200 * 0.50) / 1e6)
    assert corrida.llamadas == 1 and corrida.gastado_usd == pytest.approx(reg["costo_usd"])
    linea = json.loads(log.read_text().splitlines()[0])
    for campo in ("brazo", "pregunta", "tokens_entrada", "tokens_salida", "costo_usd", "latencia_s"):
        assert campo in linea


def test_presupuesto_corta_antes_de_llamar(monkeypatch):
    llamado = []
    monkeypatch.setattr(llm, "_cliente", SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: llamado.append(1))))
    corrida = llm.Corrida("test", presupuesto_usd=0.01)
    corrida.gastado_usd = 0.02
    with pytest.raises(llm.PresupuestoExcedido):
        llm.llamar("contexto", "P01", corrida, messages=[])
    assert llamado == []


def test_formato_respuesta():
    resp = SimpleNamespace(content=[SimpleNamespace(type="text", text='{"respuesta": "x", "fuentes": ["corpus/a.md", " b.md "]}')])
    assert normalizar_respuesta(parsear_json(resp)) == {"respuesta": "x", "fuentes": ["a.md", "b.md"]}
    malo = SimpleNamespace(content=[SimpleNamespace(type="text", text="no es json")])
    r = normalizar_respuesta(parsear_json(malo))
    assert "error" in r and r["respuesta"] == "no es json"
