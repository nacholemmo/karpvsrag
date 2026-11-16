"""Recuperación del RAG sin API: ¿los documentos requeridos de cada pregunta entran en el top-k?

Uso: python scripts/recall_rag.py [--k 5 8 12]
Usa la misma regla de documentos requeridos que el juez (evals/juez.documentos_requeridos).
Escribe resultados/recall_rag.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "evals"))

from brazos.rag.brazo import recuperar  # noqa: E402
from juez import documentos_requeridos  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, nargs="+", default=[5, 8, 12])
    args = ap.parse_args(argv)
    preguntas = [json.loads(l) for l in (RAIZ / "evals" / "preguntas.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    kmax = max(args.k)
    res = {k: defaultdict(lambda: [0, 0]) for k in args.k}
    fallos = defaultdict(list)
    for p in preguntas:
        req, modo = documentos_requeridos(p)
        if modo == "no_aplica":
            continue
        frags = recuperar(p["pregunta"], kmax)
        clase = p.get("subtipo") or p["tipo"]
        for k in args.k:
            docs = {f.archivo for f in frags[:k]}
            ok = set(req) <= docs if modo == "todos" else bool(set(req) & docs)
            res[k][clase][1] += 1
            res[k][clase][0] += ok
            if not ok:
                fallos[k].append(p["id"])
    salida = {}
    for k in args.k:
        tot_ok = sum(v[0] for v in res[k].values())
        tot = sum(v[1] for v in res[k].values())
        salida[f"top_{k}"] = {"total": f"{tot_ok}/{tot}", **{c: f"{a}/{b}" for c, (a, b) in sorted(res[k].items())},
                              "fallos": fallos[k]}
        print(f"top-{k}: {tot_ok}/{tot} | " + " | ".join(f"{c} {a}/{b}" for c, (a, b) in sorted(res[k].items()))
              + f" | fallos: {fallos[k]}")
    (RAIZ / "resultados" / "recall_rag.json").write_text(json.dumps(salida, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
