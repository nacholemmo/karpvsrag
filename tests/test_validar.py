"""Tests del validador sobre un mini-corpus armado en un directorio temporal."""
import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validar_hechos as v  # noqa: E402

CATALOGO = [
    # doc_id, archivo, area, tanda
    ("D01", "a.md", "ventas", "1"),
    ("D02", "b.md", "ventas", "1"),
    ("D03", "c.md", "compras", "2"),
]
TEXTOS = {
    "a.md": "# A\nEl pedido mínimo es de $ 250.000.\nEl alta la aprueba el Jefe\nde Compras.\n",
    "b.md": "# B\nEl pedido mínimo era de $ 150.000.\nEl alta la aprueba Calidad.\n",
    "c.md": "# C\nVer el punto 4 del documento A.\n",
}
HECHOS = [
    # hecho_id, texto, documento, area, tipo, reemplazado, reemplazado_por, grupo
    ("H001", "$ 250.000", "a.md", "ventas", "version", "no", "", "V1"),
    ("H002", "$ 150.000", "b.md", "ventas", "version", "si", "H001", "V1"),
    ("H003", "la aprueba el Jefe de Compras", "a.md", "ventas", "contradiccion", "no", "", "C1"),
    ("H004", "la aprueba Calidad", "b.md", "ventas", "contradiccion", "no", "", "C1"),
    ("H005", "punto 4 del documento A", "c.md", "compras", "referencia_cruzada", "no", "", "X1"),
    ("H006", "# A", "a.md", "ventas", "seccion", "no", "", "X1"),
]


def armar(tmp: Path, hechos=HECHOS, textos=TEXTOS, catalogo=CATALOGO) -> Path:
    (tmp / "diseno").mkdir()
    (tmp / "corpus").mkdir()
    with (tmp / "diseno" / "catalogo.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=v.CAMPOS_CATALOGO)
        w.writeheader()
        for doc_id, archivo, area, tanda in catalogo:
            w.writerow({"doc_id": doc_id, "archivo": archivo, "titulo": archivo, "area": area,
                        "formato": "manual", "fecha": "01/01/2025", "autor": "X",
                        "largo_objetivo_palabras": "10", "prolijidad": "2", "estilo": "",
                        "tanda": tanda, "referencias_a": "", "notas": ""})
    with (tmp / "hechos.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=v.CAMPOS_HECHOS)
        w.writeheader()
        for fila in hechos:
            w.writerow(dict(zip(v.CAMPOS_HECHOS, list(fila) + [""])))
    for nombre, texto in textos.items():
        (tmp / "corpus" / nombre).write_text(texto, encoding="utf-8")
    return tmp


@pytest.fixture(autouse=True)
def sin_minimos(monkeypatch):
    # El mini-corpus tiene 1 contradicción y 3 documentos.
    monkeypatch.setattr(v, "CANTIDAD_CONTRADICCIONES", 1)
    monkeypatch.setattr(v, "CANTIDAD_DOCUMENTOS", 3)


def test_corpus_valido(tmp_path):
    inf, stats = v.validar(armar(tmp_path))
    assert inf.errores == []
    assert stats["hechos_verificados"] == len(HECHOS)


def test_salto_de_linea_se_normaliza(tmp_path):
    # "Jefe\nde Compras" en el texto tiene que matchear "Jefe de Compras".
    inf, _ = v.validar(armar(tmp_path))
    assert not any("H003" in e for e in inf.errores)


def test_hecho_ausente_falla(tmp_path):
    textos = dict(TEXTOS, **{"a.md": "# A\nEl pedido mínimo es de $250.000.\nla aprueba el Jefe de Compras"})
    inf, _ = v.validar(armar(tmp_path, textos=textos))
    assert any("H001" in e for e in inf.errores)


def test_mayusculas_y_tildes_no_se_normalizan(tmp_path):
    textos = dict(TEXTOS, **{"b.md": "# B\n$ 150.000\nLa aprueba calidad"})
    inf, _ = v.validar(armar(tmp_path, textos=textos))
    assert any("H004" in e for e in inf.errores)


def test_reemplazo_inexistente_falla(tmp_path):
    hechos = [list(h) for h in HECHOS]
    hechos[1][6] = "H999"
    inf, _ = v.validar(armar(tmp_path, hechos=hechos))
    assert any("H999" in e for e in inf.errores)


def test_contradiccion_en_un_solo_documento_falla(tmp_path):
    hechos = [list(h) for h in HECHOS]
    hechos[3][2] = "a.md"
    textos = dict(TEXTOS, **{"a.md": TEXTOS["a.md"] + "la aprueba Calidad"})
    inf, _ = v.validar(armar(tmp_path, hechos=hechos, textos=textos))
    assert any("C1" in e for e in inf.errores)


def test_tipo_y_grupo_incoherentes_fallan(tmp_path):
    hechos = [list(h) for h in HECHOS]
    hechos[0][4] = "monto"  # está en V1 pero no es tipo version
    inf, _ = v.validar(armar(tmp_path, hechos=hechos))
    assert any("H001" in e and "version" in e for e in inf.errores)


def test_documento_faltante_parcial_vs_completo(tmp_path):
    textos = {k: t for k, t in TEXTOS.items() if k != "c.md"}
    raiz = armar(tmp_path, textos=textos)
    inf_completo, _ = v.validar(raiz)
    inf_parcial, _ = v.validar(raiz, parcial=True)
    assert any("c.md" in e for e in inf_completo.errores)
    assert inf_parcial.errores == [] and len(inf_parcial.pendientes) == 1


def test_tanda_limita_el_chequeo_textual(tmp_path):
    textos = dict(TEXTOS, **{"c.md": "# C\nnada"})
    inf, _ = v.validar(armar(tmp_path, textos=textos), tanda="1")
    assert inf.errores == []


def test_archivo_fuera_de_catalogo_falla(tmp_path):
    textos = dict(TEXTOS, **{"intruso.md": "hola"})
    inf, _ = v.validar(armar(tmp_path, textos=textos))
    assert any("intruso.md" in e for e in inf.errores)


def test_documento_sin_hechos_falla(tmp_path):
    catalogo = CATALOGO + [("D04", "d.md", "rrhh", "2")]
    inf, _ = v.validar(armar(tmp_path, catalogo=catalogo), parcial=True)
    assert any("d.md" in e and "no tiene hechos" in e for e in inf.errores)
