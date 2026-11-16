"""Tests de los brazos sin API: herramientas de la wiki, fragmentador, RRF y lint."""
import os
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from brazos.rag.fragmentar import fragmentar_documento  # noqa: E402
from brazos.wiki.herramientas import Herramientas  # noqa: E402
from brazos.wiki import lint  # noqa: E402


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "corpus").mkdir()
    (tmp_path / "wiki").mkdir()
    (tmp_path / "corpus" / "doc.md").write_text("El pedido mínimo es de $ 250.000 y el corte es a las 16:00 hs.", encoding="utf-8")
    return tmp_path


# --- Herramientas ---

def test_consulta_no_puede_leer_corpus(repo):
    h = Herramientas("consulta", raiz=repo)
    salida, error = h.ejecutar("leer", {"ruta": "corpus/doc.md"})
    assert error and "fuera" in salida
    salida, error = h.ejecutar("leer", {"ruta": "wiki/../corpus/doc.md"})
    assert error


def test_consulta_no_tiene_escribir(repo):
    h = Herramientas("consulta", raiz=repo)
    assert "escribir" not in {d["name"] for d in h.definiciones()}
    _, error = h.ejecutar("escribir", {"ruta": "wiki/x.md", "contenido": "x"})
    assert error


def test_ingesta_no_puede_escribir_corpus(repo):
    h = Herramientas("ingesta", raiz=repo)
    for ruta in ("corpus/doc.md", "corpus/nuevo.md", "../afuera.md", "/tmp/x.md", "wiki/../corpus/doc.md"):
        _, error = h.ejecutar("escribir", {"ruta": ruta, "contenido": "pisado"})
        assert error, ruta
    assert "pisado" not in (repo / "corpus" / "doc.md").read_text()


def test_ingesta_lee_corpus_y_escribe_wiki(repo):
    h = Herramientas("ingesta", raiz=repo)
    assert "$ 250.000" in h.ejecutar("leer", {"ruta": "corpus/doc.md"})[0]
    salida, error = h.ejecutar("escribir", {"ruta": "wiki/proceso/pedidos.md", "contenido": "# Pedidos"})
    assert not error and (repo / "wiki" / "proceso" / "pedidos.md").exists()
    _, error = h.ejecutar("escribir", {"ruta": "wiki/x.txt", "contenido": "x"})
    assert error  # solo .md


def test_symlink_a_corpus_no_escapa(repo):
    os.symlink(repo / "corpus", repo / "wiki" / "atajo")
    h = Herramientas("consulta", raiz=repo)
    _, error = h.ejecutar("leer", {"ruta": "wiki/atajo/doc.md"})
    assert error


# --- Fragmentador ---

def test_fragmentador_cubre_todo_y_respeta_secciones():
    texto = "# Manual\n\nIntro.\n\n## 1. Alcance\n\nPárrafo A.\n\n## 2. Plazos\n\nPárrafo B con 48 horas.\n"
    frags = fragmentar_documento("m.md", texto)
    assert {f.seccion for f in frags} == {"Manual", "Manual > 1. Alcance", "Manual > 2. Plazos"}
    juntos = " ".join(f.texto for f in frags)
    for parte in ("Intro.", "Párrafo A.", "Párrafo B con 48 horas."):
        assert parte in juntos
    assert all(f.titulo_doc == "Manual" for f in frags)


def test_fragmentador_subdivide_secciones_largas():
    parrafos = "\n\n".join(" ".join(["palabra"] * 100) + f" fin{i}" for i in range(8))
    frags = fragmentar_documento("x.md", "## Larga\n\n" + parrafos)
    assert len(frags) > 1
    assert all(len(f.texto.split()) <= 350 + 101 for f in frags)
    juntos = " ".join(f.texto for f in frags)
    assert all(f"fin{i}" in juntos for i in range(8))


def test_rrf():
    from brazos.rag.brazo import rrf
    # el 2 está segundo en un ranking y primero en el otro: le gana al 1 (primero y tercero)
    assert rrf([[1, 2, 3], [2, 3, 1]])[0] == 2
    assert rrf([[5, 6], [5, 7]])[0] == 5


# --- Lint ---

def test_lint_detecta_problemas(repo):
    w = repo / "wiki"
    (w / "proceso").mkdir()
    (w / "index.md").write_text("- [Pedidos](proceso/pedidos.md): pedido mínimo\n", encoding="utf-8")
    (w / "proceso" / "pedidos.md").write_text(
        "# Pedidos\n- Mínimo: $ 250.000 [fuente: doc.md]\n- Corte: 17:00 [fuente: doc.md]\n"
        "- [roto](../proceso/no-existe.md)\n- Otro [fuente: inventado.md]\n", encoding="utf-8")
    (w / "proceso" / "huerfana.md").write_text("# Sin citas\n", encoding="utf-8")
    errores = lint.chequear(w, repo / "corpus")
    texto = "\n".join(errores)
    assert "enlace roto" in texto
    assert "inventado.md" in texto
    assert "'17:00'" in texto and "'$ 250.000'" not in texto
    assert "huerfana.md: no tiene ninguna cita" in texto
    assert "huerfana.md: no está en index.md" in texto


def test_lint_wiki_limpia(repo):
    w = repo / "wiki"
    (w / "index.md").write_text("- [Pedidos](pedidos.md): mínimo\n", encoding="utf-8")
    (w / "pedidos.md").write_text("# Pedidos\n- Mínimo: $ 250.000, corte 16:00 [fuente: doc.md]\n", encoding="utf-8")
    assert lint.chequear(w, repo / "corpus") == []


def test_lint_no_toma_el_punto_final_como_parte_del_monto(repo):
    w = repo / "wiki"
    (w / "index.md").write_text("- [P](p.md): x\n", encoding="utf-8")
    (w / "p.md").write_text("# P\n- El mínimo es $ 250.000. [fuente: doc.md]\n", encoding="utf-8")
    assert lint.chequear(w, repo / "corpus") == []
