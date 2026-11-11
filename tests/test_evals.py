"""Tests de acuerdo (kappa), fuente_exacta y validador de preguntas, sin API."""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "evals"))

import acuerdo  # noqa: E402
import juez  # noqa: E402
import validar_preguntas as vp  # noqa: E402


def test_kappa_perfecto_y_azar():
    assert acuerdo.kappa([("a", "a"), ("b", "b")], ["a", "b"]) == pytest.approx(1.0)
    assert acuerdo.kappa([("a", "b"), ("b", "a")], ["a", "b"]) == pytest.approx(-1.0)
    assert acuerdo.kappa([("a", "a"), ("a", "a")], ["a", "b"]) is None


def P(tipo, docs, subtipo=None, hechos=()):
    return {"id": "P01", "tipo": tipo, "subtipo": subtipo, "documentos_fuente": docs, "hechos": list(hechos)}


def test_fuente_exacta_dato_alcanza_una():
    assert juez.fuente_exacta(P("dato", ["a.md", "b.md"]), ["b.md"]) == "correcta"
    assert juez.fuente_exacta(P("dato", ["a.md"]), ["z.md"]) == "incorrecta"
    assert juez.fuente_exacta(P("dato", ["a.md"]), []) == "incorrecta"


def test_fuente_exacta_cruce_exige_todas():
    assert juez.fuente_exacta(P("cruce", ["a.md", "b.md"]), ["a.md"]) == "parcial"
    assert juez.fuente_exacta(P("cruce", ["a.md", "b.md"]), ["b.md", "a.md", "c.md"]) == "correcta"


def test_fuente_exacta_version_alcanza_la_vigente():
    # H002 ($ 1.500.000, vigente) está en la política v2; H015 ($ 800.000, viejo) en el manual 2023
    p = P("contradiccion_version", ["politica-creditos-cobranzas-v2.md", "manual-creditos-2023.md"],
          subtipo="version", hechos=["H002", "H015"])
    assert juez.fuente_exacta(p, ["politica-creditos-cobranzas-v2.md"]) == "correcta"
    assert juez.fuente_exacta(p, ["manual-creditos-2023.md"]) == "parcial"


def test_fuente_exacta_sin_respuesta():
    assert juez.fuente_exacta(P("sin_respuesta", []), ["a.md"]) == "no_aplica"


def escribir(tmp_path, preguntas):
    ruta = tmp_path / "p.jsonl"
    ruta.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in preguntas), encoding="utf-8")
    return ruta


BASE = {"id": "P01", "tipo": "dato", "subtipo": None, "pregunta": "¿Cuánto es el límite inicial para un cliente nuevo?",
        "respuesta_referencia": "$ 1.500.000", "elementos_clave": ["$ 1.500.000"],
        "documentos_fuente": ["politica-creditos-cobranzas-v2.md"], "hechos": ["H002"],
        "comportamiento_esperado": "Dar el monto", "hueco": None}


def test_pregunta_valida_en_parcial(tmp_path):
    errores, avisos, _ = vp.validar(RAIZ, escribir(tmp_path, [BASE]), parcial=True)
    assert errores == []
    assert any("grupo C/V" in a for a in avisos)  # H002 es V1: avisa en una pregunta de dato


def test_elemento_clave_inexistente_falla(tmp_path):
    p = dict(BASE, elementos_clave=["$ 9.999.999"])
    errores, _, _ = vp.validar(RAIZ, escribir(tmp_path, [p]), parcial=True)
    assert any("no aparece" in e for e in errores)


def test_version_no_admite_valor_viejo_como_clave(tmp_path):
    p = dict(BASE, tipo="contradiccion_version", subtipo="version", elementos_clave=["$ 800.000"],
             documentos_fuente=["politica-creditos-cobranzas-v2.md", "manual-creditos-2023.md"], hechos=["H002", "H015"])
    errores, _, _ = vp.validar(RAIZ, escribir(tmp_path, [p]), parcial=True)
    assert any("valor viejo" in e for e in errores)


def test_sin_respuesta_debe_ir_vacia(tmp_path):
    p = dict(BASE, tipo="sin_respuesta", hueco="H1")
    errores, _, _ = vp.validar(RAIZ, escribir(tmp_path, [p]), parcial=True)
    assert any("vacíos" in e for e in errores)


def test_conteo_completo_falla_con_una(tmp_path):
    errores, _, _ = vp.validar(RAIZ, escribir(tmp_path, [BASE]), parcial=False)
    assert any("se esperaban 50" in e for e in errores)
