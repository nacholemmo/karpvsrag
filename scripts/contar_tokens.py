"""Mide con la API (count_tokens, sin costo) cuántos tokens ocupa el corpus completo en un prompt.

Uso: .venv/bin/python scripts/contar_tokens.py [--por-documento]

Importa porque Haiku 5.5 cobra 5× más cuando el prompt supera los 100k tokens.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comun import config  # noqa: E402
from comun.corpus import cargar_corpus, formatear_corpus  # noqa: E402
from comun.llm import cliente  # noqa: E402
from comun.precios import PRECIOS  # noqa: E402


def contar(texto: str, modelo: str) -> int:
    return cliente().messages.count_tokens(model=modelo, messages=[{"role": "user", "content": texto}]).input_tokens


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--por-documento", action="store_true", help="contar también cada documento (50 llamadas gratuitas)")
    args = ap.parse_args()

    modelo = config.modelo_respuesta()
    docs = cargar_corpus()
    total = contar(formatear_corpus(docs), modelo)
    salida = {"modelo": modelo, "documentos": len(docs), "tokens_corpus_formateado": total}
    tramo = PRECIOS.get(modelo) and PRECIOS[modelo].tramo_largo
    if tramo:
        salida["umbral_tramo_caro"] = tramo[0]
        salida["margen_bajo_umbral"] = tramo[0] - total
    if args.por_documento:
        salida["por_documento"] = {a: contar(t, modelo) for a, t in docs}
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    destino = config.RAIZ / "resultados" / "tokens_corpus.json"
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nGuardado en {destino.relative_to(config.RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
