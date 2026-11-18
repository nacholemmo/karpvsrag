"""Tests de la agregación de resultados (sin API)."""
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import resultados as r  # noqa: E402


def test_puntaje_y_porcentajes():
    e = r.exactitud(["correcta", "parcial", "incorrecta", "correcta"])
    assert e["n"] == 4 and e["correcta"] == 2
    assert e["puntaje"] == pytest.approx((2 + 0.5) / 4)
    assert e["pct_parcial"] == 25.0


def test_percentil():
    assert r.percentil([1, 2, 3, 4, 5], 0.5) == 3
    assert r.percentil([1, 2, 3, 4, 5], 0.9) == pytest.approx(4.6)


def test_pregunta_sin_respuesta_valida_cuenta_como_incorrecta():
    preguntas = {"P01": {"id": "P01", "tipo": "dato", "subtipo": None},
                 "P02": {"id": "P02", "tipo": "contradiccion_version", "subtipo": "version"}}
    respuestas = [{"id": "x-P01", "pregunta_id": "P01", "costo_usd": 0.001, "latencia_s": 2.0, "llamadas": 1}]
    juicios = {"x-P01": {"veredicto": "correcta", "fuente": "correcta", "fuente_exacta": "correcta"}}
    m = r.metricas_brazo("x", preguntas, respuestas, juicios)
    assert m["sin_respuesta_valida"] == ["P02"]
    assert m["exactitud"]["incorrecta"] == 1 and m["exactitud"]["puntaje"] == 0.5
    assert m["por_tipo"]["version"]["incorrecta"] == 1
