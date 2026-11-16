"""Brazo 2: RAG híbrido. Embeddings + BM25, fusión con Reciprocal Rank Fusion, top-k fragmentos al modelo."""
from __future__ import annotations

import os

import numpy as np
from rank_bm25 import BM25Okapi

from brazos.rag import indexar
from comun import config
from comun.formato import FORMATO_RESPUESTA, INSTRUCCIONES_FORMATO, normalizar_respuesta, parsear_json
from comun.llm import Corrida, llamar

NOMBRE = "rag"
RRF_K = 60

SISTEMA = (
    "Sos un asistente que responde preguntas de empleados de Distribuidora Quebracho Azul S.A. "
    "usando únicamente los fragmentos de documentos internos que se te pasan con cada pregunta. "
    "Cada fragmento indica su archivo de origen; citá ese archivo en `fuentes`. "
    "Si los fragmentos no alcanzan para responder, decilo. " + INSTRUCCIONES_FORMATO
)

_estado: dict = {}


def top_k() -> int:
    return int(os.environ.get("TOP_K") or 8)


def _cargar():
    if not _estado:
        frags, emb = indexar.cargar()
        _estado.update(frags=frags, emb=emb, bm25=BM25Okapi([indexar.tokenizar(f.texto_indexado) for f in frags]))
    return _estado


def rrf(rankings: list[list[int]], k: int = RRF_K) -> list[int]:
    """Reciprocal Rank Fusion: suma 1/(k + posición) de cada ranking. Devuelve los índices ordenados."""
    puntaje: dict[int, float] = {}
    for ranking in rankings:
        for pos, idx in enumerate(ranking, 1):
            puntaje[idx] = puntaje.get(idx, 0.0) + 1.0 / (k + pos)
    return sorted(puntaje, key=lambda i: (-puntaje[i], i))


def recuperar(consulta: str, k: int | None = None) -> list:
    e = _cargar()
    q = indexar.modelo().encode([f"query: {consulta}"], normalize_embeddings=True)[0]
    denso = list(np.argsort(-(e["emb"] @ q)))
    lexico = list(np.argsort(-e["bm25"].get_scores(indexar.tokenizar(consulta))))
    orden = rrf([[int(i) for i in denso], [int(i) for i in lexico]])
    return [e["frags"][i] for i in orden[: (k or top_k())]]


def responder(pregunta: dict, corrida: Corrida, brazo: str = NOMBRE) -> dict:
    frags = recuperar(pregunta["pregunta"])
    contexto = "\n\n".join(
        f'<fragmento archivo="{f.archivo}" seccion="{f.seccion}">\n{f.texto}\n</fragmento>' for f in frags)
    response, reg = llamar(
        brazo, pregunta["id"], corrida,
        max_tokens=8000,
        system=SISTEMA,
        messages=[{"role": "user", "content": f"<fragmentos>\n{contexto}\n</fragmentos>\n\nPregunta: {pregunta['pregunta']}"}],
        output_config={"effort": config.esfuerzo(), **FORMATO_RESPUESTA},
    )
    r = normalizar_respuesta(parsear_json(response))
    return {**r, "valido": reg["stop_reason"] == "end_turn" and "error" not in r,
            "stop_reason": reg["stop_reason"], "costo_usd": reg["costo_usd"],
            "latencia_s": reg["latencia_s"], "llamadas": 1,
            "extra": {"recuperados": [f.id for f in frags], "top_k": len(frags)}}
