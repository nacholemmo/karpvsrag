"""Índice del RAG: embeddings locales (multilingual-e5-small) + BM25. Todo local, sin API.

Uso: python brazos/rag/indexar.py [--forzar]
Guarda en indices/rag/ (no se versiona). Se reindexa solo si cambió el corpus (hash).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np  # noqa: E402

from brazos.rag.fragmentar import Fragmento, fragmentar_corpus  # noqa: E402
from comun import config  # noqa: E402
from comun.corpus import cargar_corpus  # noqa: E402

DIR = config.RAIZ / "indices" / "rag"
MODELO_EMBEDDINGS = "intfloat/multilingual-e5-small"
STOPWORDS = set("""a al algo ante con contra de del desde el ella ellos en entre era es esa ese eso esta este esto ha hay
la las le les lo los mas me mi mis muy ni no nos o os para pero por que se ser si sin sobre son su sus te tiene
tu un una uno unos y ya yo como cual cuando donde quien cuanto cuanta""".split())

_modelo = None


def modelo():
    global _modelo
    if _modelo is None:
        import os
        from sentence_transformers import SentenceTransformer
        try:  # primero desde la caché local, sin red
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            _modelo = SentenceTransformer(MODELO_EMBEDDINGS, device="cpu")
        except OSError:  # no está en caché: se descarga una vez de Hugging Face
            os.environ["HF_HUB_OFFLINE"] = "0"
            _modelo = SentenceTransformer(MODELO_EMBEDDINGS, device="cpu")
    return _modelo


def tokenizar(texto: str) -> list[str]:
    """Minúsculas, sin tildes, palabras y números, sin stopwords (para BM25)."""
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [w for w in re.findall(r"\w+", t) if w not in STOPWORDS]


def hash_corpus(docs: list[tuple[str, str]]) -> str:
    h = hashlib.sha256()
    for archivo, texto in docs:
        h.update(archivo.encode())
        h.update(texto.encode())
    return h.hexdigest()


def construir(forzar: bool = False) -> dict:
    docs = cargar_corpus()
    huella = hash_corpus(docs)
    meta_path = DIR / "meta.json"
    if not forzar and meta_path.exists() and json.loads(meta_path.read_text())["hash_corpus"] == huella:
        return json.loads(meta_path.read_text())
    inicio = time.perf_counter()
    frags = fragmentar_corpus(docs)
    emb = modelo().encode([f"passage: {f.texto_indexado}" for f in frags], normalize_embeddings=True,
                          batch_size=32, show_progress_bar=False)
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "fragmentos.json").write_text(json.dumps([f.dict() for f in frags], ensure_ascii=False), encoding="utf-8")
    np.save(DIR / "embeddings.npy", np.asarray(emb, dtype=np.float32))
    meta = {"hash_corpus": huella, "modelo": MODELO_EMBEDDINGS, "fragmentos": len(frags),
            "segundos": round(time.perf_counter() - inicio, 1)}
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def cargar() -> tuple[list[Fragmento], np.ndarray]:
    construir()
    frags = [Fragmento(**d) for d in json.loads((DIR / "fragmentos.json").read_text(encoding="utf-8"))]
    return frags, np.load(DIR / "embeddings.npy")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    args = ap.parse_args(argv)
    print(json.dumps(construir(args.forzar), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
