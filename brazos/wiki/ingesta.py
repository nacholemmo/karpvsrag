"""Ingesta: un agente compila corpus/ en wiki/, un documento por sesión, en orden cronológico.

Uso:
    python brazos/wiki/ingesta.py --limite 5             # los 5 primeros pendientes (prueba)
    python brazos/wiki/ingesta.py                        # todos los pendientes
    python brazos/wiki/ingesta.py --documentos a.md,b.md --rehacer   # reingestar documentos puntuales (fase 4)

El progreso y el costo por documento quedan en resultados/ingesta_wiki.json (se puede retomar).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from brazos.wiki.agente import sesion  # noqa: E402
from brazos.wiki.herramientas import Herramientas  # noqa: E402
from comun import config  # noqa: E402
from comun.llm import Corrida  # noqa: E402

ESTADO = config.RAIZ / "resultados" / "ingesta_wiki.json"
MAX_TURNOS = 15

SISTEMA = (
    "Sos el agente que mantiene la wiki interna de Distribuidora Quebracho Azul S.A. "
    "Tu trabajo es incorporar documentos de corpus/ a wiki/ siguiendo al pie de la letra este esquema:\n\n"
    + (config.RAIZ / "ESQUEMA.md").read_text(encoding="utf-8")
)

MENSAJE = """Incorporá a la wiki el documento `corpus/{archivo}`.

Pasos:
1. Leé el documento completo.
2. Leé `wiki/index.md` (si no existe, lo vas a crear) y las páginas existentes que este documento afecte.
3. Creá o actualizá las páginas que correspondan. Para actualizar, reescribí la página completa conservando lo que ya tenía y sumando lo nuevo, con su fuente. Aplicá las reglas de versiones, contradicciones, huecos y referencias cruzadas.
4. Actualizá `wiki/index.md` con cada página nueva.

Copiá los datos duros textualmente. No modifiques corpus/. Cuando termines, respondé en una o dos líneas qué páginas creaste o actualizaste."""


def orden_cronologico() -> list[str]:
    filas = list(csv.DictReader((config.RAIZ / "diseno" / "catalogo.csv").open(encoding="utf-8")))
    return [f["archivo"] for f in sorted(filas, key=lambda f: (datetime.strptime(f["fecha"], "%d/%m/%Y"), f["archivo"]))]


def cargar_estado() -> dict:
    return json.loads(ESTADO.read_text(encoding="utf-8")) if ESTADO.exists() else {"documentos": {}}


def guardar_estado(estado: dict) -> None:
    docs = estado["documentos"].values()
    estado["resumen"] = {
        "documentos_ingeridos": len(estado["documentos"]),
        "costo_usd": round(sum(d["costo_usd"] for d in docs), 6),
        "segundos": round(sum(d["segundos"] for d in docs), 1),
        "turnos": sum(d["turnos"] for d in docs),
        "sesiones_cortadas": [a for a, d in estado["documentos"].items() if d["cortada"]],
        "sesiones_sin_escrituras": [a for a, d in estado["documentos"].items() if not d["escritos"]],
    }
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int)
    ap.add_argument("--documentos", help="lista separada por comas")
    ap.add_argument("--rehacer", action="store_true", help="reingestar aunque ya figuren como hechos")
    ap.add_argument("--etiqueta", default="ingesta", help="nombre de la corrida en el log (por ejemplo, actualizacion)")
    args = ap.parse_args(argv)

    estado = cargar_estado()
    orden = orden_cronologico()
    candidatos = [d for d in orden if d in args.documentos.split(",")] if args.documentos else orden
    pendientes = [d for d in candidatos if args.rehacer or d not in estado["documentos"]]
    if args.limite is not None:
        pendientes = pendientes[: args.limite]
    corrida = Corrida(f"wiki_{args.etiqueta}")
    print(f"Ingesta de {len(pendientes)} documentos con {config.modelo_respuesta()} "
          f"(presupuesto de la corrida USD {corrida.presupuesto_usd:.2f})")
    for archivo in pendientes:
        inicio = time.perf_counter()
        h = Herramientas("ingesta")
        r = sesion("wiki_ingesta", archivo, corrida, h, SISTEMA, MENSAJE.format(archivo=archivo), MAX_TURNOS,
                   exigir_escritura=True)
        estado["documentos"][archivo] = {
            "costo_usd": round(r.costo_usd, 6), "turnos": r.turnos, "segundos": round(time.perf_counter() - inicio, 1),
            "max_prompt_tokens": r.max_prompt, "cortada": r.cortada, "escritos": sorted(set(r.escritos)),
            "avisos_sin_escritura": r.avisos_sin_escritura, "cortes_por_largo": r.cortes_por_largo,
            "etiqueta": args.etiqueta,
        }
        guardar_estado(estado)
        print(f"  {archivo}: USD {r.costo_usd:.4f}, {r.turnos} turnos, prompt máx {r.max_prompt}, "
              f"{len(set(r.escritos))} páginas escritas" + (f", CORTADA ({r.cortada})" if r.cortada else ""))
    print(f"Costo de la corrida: USD {corrida.gastado_usd:.4f}. Acumulado de la ingesta: {estado.get('resumen')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
