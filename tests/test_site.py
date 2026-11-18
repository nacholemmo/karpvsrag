"""Tests de la landing sin navegador."""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = RAIZ / "site"


def test_copia_de_results_identica():
    assert (SITE / "datos" / "results.json").read_text() == (RAIZ / "resultados" / "results.json").read_text()


def test_archivos_referenciados_existen():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for ref in re.findall(r'(?:src|href)="([^"#:][^"]*)"', html):
        if ref.startswith("data:"):
            continue
        assert (SITE / ref).exists(), ref


def test_sin_recursos_externos():
    for archivo in ("index.html", "app.js", "estilos.css"):
        texto = (SITE / archivo).read_text(encoding="utf-8")
        externos = [u for u in re.findall(r"https?://[^\s\"')]+", texto) if "www.w3.org/2000/svg" not in u]
        assert externos == [], (archivo, externos)


def test_results_tiene_las_claves_que_usa_la_landing():
    r = json.loads((SITE / "datos" / "results.json").read_text())
    for b in ("contexto", "rag", "wiki"):
        m = r["brazos"][b]
        assert {"puntaje", "pct_correcta", "correcta", "parcial", "incorrecta", "n"} <= set(m["exactitud"])
        assert {"media"} <= set(m["costo_usd"]) and "mediana" in m["latencia_s"] and "media" in m["llamadas_por_pregunta"]
        for t in ("dato", "procedimiento", "cruce", "contradiccion", "version", "sin_respuesta"):
            assert "puntaje" in m["por_tipo"][t]
        assert "puntaje" in r["brazos_referencias_originales"][b]["exactitud"]
        assert "puntaje" in r["actualizacion"]["brazos"][b]["exactitud"]
    assert {"corridas", "unanime", "respuestas"} <= set(r["brazos"]["_estabilidad_juez"])
    p = r["preparacion"]
    assert {"ingesta_costo_usd", "lint_costo_usd", "ingesta_segundos"} <= set(p["wiki"]) and "indexacion_segundos" in p["rag"]
    a = r["actualizacion"]["costo_y_tiempo_de_actualizar"]
    assert "segundos" in a["rag"] and {"costo_usd", "segundos"} <= set(a["wiki"])
    assert r["meta"]["advertencias"] and r["acuerdo_humano_juez"]["v1"]["acuerdo"]
