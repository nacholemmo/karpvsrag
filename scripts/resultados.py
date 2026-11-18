"""Agrega respuestas, juicios y métricas de preparación en resultados/results.json y resultados/resumen.md. Sin API.

Uso: python scripts/resultados.py
Determinístico: solo lee archivos de resultados/, evals/ e indices/. No redondea a favor: guarda los valores
con 4-6 decimales y el resumen los muestra con 1 decimal en porcentajes.
"""
from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
EVALS = RAIZ / "evals"
sys.path.insert(0, str(RAIZ / "scripts"))
from acuerdo import kappa  # noqa: E402

BRAZOS = ["contexto", "rag", "wiki"]
VEREDICTOS = ["correcta", "parcial", "incorrecta"]
FUENTES = ["correcta", "parcial", "incorrecta", "no_aplica"]
CLASES = ["dato", "procedimiento", "cruce", "contradiccion", "version", "sin_respuesta"]


def jsonl(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def clase(p: dict) -> str:
    return p.get("subtipo") or p["tipo"]


def percentil(xs: list[float], q: float) -> float:
    xs = sorted(xs)
    if not xs:
        return 0.0
    i = (len(xs) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def exactitud(veredictos: list[str]) -> dict:
    n = len(veredictos)
    c = Counter(veredictos)
    d = {"n": n, **{v: c.get(v, 0) for v in VEREDICTOS}}
    if n:
        d.update({f"pct_{v}": round(100 * c.get(v, 0) / n, 2) for v in VEREDICTOS})
        d["puntaje"] = round((c.get("correcta", 0) + 0.5 * c.get("parcial", 0)) / n, 4)
    return d


def votar(juicios_por_corrida: list[dict]) -> dict:
    """Voto mayoritario entre corridas del juez, por id de respuesta.

    Si las tres etiquetas difieren, se toma la del medio (parcial). fuente_exacta no depende del juez.
    """
    out = {}
    for rid in juicios_por_corrida[0]:
        js = [c[rid] for c in juicios_por_corrida if rid in c]
        def mayoria(campo, orden):
            cnt = Counter(j[campo] for j in js)
            top, n = cnt.most_common(1)[0]
            if n > 1 or len(js) == 1:
                return top
            presentes = sorted(cnt, key=orden.index)
            return presentes[len(presentes) // 2]
        out[rid] = {**js[0], "veredicto": mayoria("veredicto", VEREDICTOS), "fuente": mayoria("fuente", FUENTES),
                    "votos": [j["veredicto"] for j in js]}
    return out


def estabilidad(juicios_por_corrida: list[dict], preguntas: dict) -> dict:
    """Cuánto cambian los veredictos entre corridas del juez."""
    ids = list(juicios_por_corrida[0])
    patrones = Counter()
    for rid in ids:
        n = len({c[rid]["veredicto"] for c in juicios_por_corrida if rid in c})
        patrones[{1: "unanime", 2: "dos_a_uno", 3: "todas_distintas"}[n]] += 1
    por_corrida = {}
    for b in BRAZOS:
        por_corrida[b] = []
        for c in juicios_por_corrida:
            vs = [c[r]["veredicto"] for r in ids if r.startswith(f"{b}-")]
            por_corrida[b].append(exactitud(vs)["puntaje"])
    return {"corridas": len(juicios_por_corrida), "respuestas": len(ids), **dict(patrones),
            "puntaje_por_corrida": por_corrida,
            "rango_por_brazo": {b: round(max(v) - min(v), 4) for b, v in por_corrida.items()}}


def metricas_brazo(brazo: str, preguntas: dict, respuestas: list[dict], juicios: dict) -> dict:
    """juicios: id de respuesta -> juicio. Las preguntas sin respuesta válida cuentan como incorrectas."""
    por_preg = {r["pregunta_id"]: r for r in respuestas}
    veredictos, por_clase, fuentes, fuentes_exactas, faltantes = [], defaultdict(list), Counter(), Counter(), []
    for pid, p in sorted(preguntas.items()):
        r = por_preg.get(pid)
        j = juicios.get(r["id"]) if r else None
        if j is None:
            faltantes.append(pid)
            v = "incorrecta"
        else:
            v = j["veredicto"]
            fuentes[j["fuente"]] += 1
            fuentes_exactas[j["fuente_exacta"]] += 1
        veredictos.append(v)
        por_clase[clase(p)].append(v)
    costos = [r["costo_usd"] for r in respuestas]
    lat = [r["latencia_s"] for r in respuestas]
    llamadas = [r.get("llamadas", 1) for r in respuestas]
    return {
        "exactitud": exactitud(veredictos),
        "por_tipo": {c: exactitud(por_clase[c]) for c in CLASES if por_clase.get(c)},
        "fuente_juez": {f: fuentes.get(f, 0) for f in FUENTES},
        "fuente_exacta": {f: fuentes_exactas.get(f, 0) for f in FUENTES},
        "sin_respuesta_valida": faltantes,
        "costo_usd": {"total": round(sum(costos), 6), "media": round(statistics.mean(costos), 6) if costos else 0,
                      "mediana": round(statistics.median(costos), 6) if costos else 0,
                      "p90": round(percentil(costos, 0.9), 6)},
        "latencia_s": {"media": round(statistics.mean(lat), 3) if lat else 0,
                       "mediana": round(statistics.median(lat), 3) if lat else 0,
                       "p90": round(percentil(lat, 0.9), 3)},
        "llamadas_por_pregunta": {"media": round(statistics.mean(llamadas), 3) if llamadas else 0,
                                  "max": max(llamadas) if llamadas else 0},
    }


def acuerdo_humano() -> dict:
    rev_path, mapa_path = EVALS / "revision_manual.csv", EVALS / "mapa_revision.json"
    if not rev_path.exists() or not mapa_path.exists():
        return {}
    rev = list(csv.DictReader(rev_path.open(encoding="utf-8")))
    mapa = json.loads(mapa_path.read_text(encoding="utf-8"))
    out = {}
    for nombre, archivo in (("v1", "juicios_muestra_v1.jsonl"), ("v2", "juicios_muestra.jsonl")):
        j = {x["id"]: x for x in jsonl(EVALS / archivo)}
        pares = [(r["tu_veredicto"].strip(), j[mapa[r["caso"]]]["veredicto"]) for r in rev if mapa.get(r["caso"]) in j]
        if pares:
            k = kappa(pares, VEREDICTOS)
            out[nombre] = {"n": len(pares), "acuerdo": sum(a == b for a, b in pares),
                           "kappa": round(k, 4) if k is not None else None}
    out["nota"] = ("v2 se calculó después de ajustar la rúbrica y dos referencias mirando estas mismas 15 respuestas; "
                   "las etiquetas de fuente y el veredicto de un caso los completó Claude a pedido del usuario.")
    return out


def preparacion() -> dict:
    base_path = RES / "ingesta_wiki_v3_linea_base.json"  # congelado antes de la prueba de actualización
    ing = json.loads((base_path if base_path.exists() else RES / "ingesta_wiki.json").read_text(encoding="utf-8"))
    docs = ing["documentos"]
    base = {a: d for a, d in docs.items() if d.get("etiqueta", "ingesta") == "ingesta"}
    lint = json.loads((RES / "lint_wiki.json").read_text(encoding="utf-8")) if (RES / "lint_wiki.json").exists() else []
    lint_base = [x for x in lint if x.get("etapa", "construccion") == "construccion"]
    rag_seg = json.loads((RES / "rag_indice_linea_base.json").read_text())["segundos"]
    fallidas = {}
    for nombre, archivo in (("v1_primera_pasada", "ingesta_wiki_primera_pasada.json"),
                            ("v1_parcheada", "ingesta_wiki_v1_parcheada.json"),
                            ("v2_esquema_con_fuga", "ingesta_wiki_v2_esquema_con_fuga.json")):
        if (RES / archivo).exists():
            r = json.loads((RES / archivo).read_text(encoding="utf-8")).get("resumen", {})
            fallidas[nombre] = {"costo_usd": r.get("costo_usd"), "segundos": r.get("segundos")}
    return {
        "wiki": {
            "ingesta_costo_usd": round(sum(d["costo_usd"] for d in base.values()), 6),
            "ingesta_segundos": round(sum(d["segundos"] for d in base.values()), 1),
            "ingesta_turnos": sum(d["turnos"] for d in base.values()),
            "documentos": len(base),
            "lint_costo_usd": round(sum(x["costo_usd"] for x in lint_base), 6),
            "lint_pasadas": len(lint_base),
            "paginas": len(list((RAIZ / "wiki").rglob("*.md"))),
            "versiones_descartadas_no_sumadas": fallidas,
        },
        "rag": {"indexacion_segundos": rag_seg, "costo_usd": 0.0,
                "modelo_embeddings": "intfloat/multilingual-e5-small (local, CPU)"},
        "contexto": {"nota": "Sin preparación. La primera llamada de cada corrida escribe ~92k tokens en caché (~USD 0,012)."},
    }


def armar(sufijo: str = "", archivo_preguntas: str = "preguntas.jsonl", juicios_archivo: str | None = None,
          triple: bool = False) -> dict | None:
    preguntas = {p["id"]: p for p in jsonl(EVALS / archivo_preguntas)}
    if triple:
        corridas = [{j["id"]: j for j in jsonl(RES / f"juicios{sufijo}{r}.jsonl")} for r in ("", "_r2", "_r3")]
        corridas = [c for c in corridas if c]
        juicios = votar(corridas)
    else:
        juicios = {j["id"]: j for j in jsonl(RES / (juicios_archivo or f"juicios{sufijo}.jsonl"))}
    if not preguntas or not juicios:
        return None
    res = {b: metricas_brazo(b, preguntas, jsonl(RES / f"respuestas_{b}{sufijo}.jsonl"), juicios) for b in BRAZOS}
    if triple:
        res["_estabilidad_juez"] = estabilidad(corridas, preguntas)
    return res


def main() -> int:
    tokens = json.loads((RES / "tokens_corpus.json").read_text())
    def git(*a):
        return subprocess.run(["git", *a], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
    commit = {"linea_base_corrida_principal": git("rev-parse", "--short", "linea-base^{commit}"),
              "nota": "La corrida principal se hizo sobre el corpus del tag linea-base; la prueba de actualización, sobre el corpus actual."}
    recall = json.loads((RES / "recall_rag.json").read_text()) if (RES / "recall_rag.json").exists() else {}
    out = {
        "meta": {
            "modelo_respuesta": "claude-haiku-5-5", "modelo_juez": "claude-haiku-5-5", "effort": "low",
            "rag_top_k": 8, "preguntas": 50, "documentos": 50,
            "tokens_corpus_haiku": tokens["tokens_prompt_contexto_completo"], "commit": commit,
            "puntaje": "correcta + 0,5 × parcial, sobre el total de preguntas",
            "juez": "Tres corridas independientes del juez por respuesta; veredicto por voto mayoritario (si las tres difieren, parcial). "
                    "Las métricas con referencias originales usan una sola corrida.",
            "advertencias": [
                "Corpus sintético de 50 documentos de una empresa ficticia.",
                "Un solo modelo (Haiku 5.5) responde en los tres brazos y también juzga: hay sesgo de autoevaluación.",
                "Una sola corrida por brazo; el juez no es determinista.",
                "Las preguntas y las referencias las escribieron agentes a partir de hechos.csv; no hubo revisión humana de las 50.",
                "Solo el prompt del RAG dice 'si los fragmentos no alcanzan, decilo'; el resto de las instrucciones de formato es igual en los tres brazos.",
                "El juez puede deducir el brazo por el estilo de la respuesta (el RAG menciona 'fragmentos' y la wiki, 'wiki').",
            ],
        },
        "correccion_de_referencias": {
            "que": "Las 10 preguntas sin_respuesta y U05 se re-evaluaron con referencias corregidas por un criterio uniforme: "
                   "incluir lo que el corpus sí dice del tema y sacar lo que no dice. Las revisó un subagente sin ver respuestas.",
            "por_que": "Las referencias originales omitían contenido del corpus y el juez castigaba respuestas fieles "
                       "(5 veces a la wiki, 2 al contexto, 1 al RAG). Una primera corrección solo de P25 favorecía a contexto y RAG.",
            "puntaje_principal": "brazos = referencias corregidas; brazos_referencias_originales = referencias tal como estaban en la corrida",
            "estabilidad_del_juez": "Al volver a juzgar las 30 respuestas sin_respuesta con referencias corregidas cambiaron 12 veredictos. "
                                    "Con referencias fijas, en 3 corridas del juez, 139/150 veredictos fueron unánimes (ver brazos._estabilidad_juez): "
                                    "la mayor parte del cambio vino de las referencias.",
            "archivos": ["evals/preguntas_referencias_originales.jsonl", "resultados/juicios_referencias_originales.jsonl",
                         "resultados/juicios_actualizacion_referencias_originales.jsonl"],
        },
        "acuerdo_humano_juez": acuerdo_humano(),
        "recall_rag": recall,
        "brazos": armar(triple=True),
        "brazos_referencias_originales": armar(juicios_archivo="juicios_referencias_originales.jsonl"),
        "preparacion": preparacion(),
        "actualizacion": None,
    }
    act = armar("_actualizacion", "preguntas_actualizacion.jsonl", triple=True)
    if act:
        datos_act = json.loads((RES / "actualizacion.json").read_text()) if (RES / "actualizacion.json").exists() else {}
        out["actualizacion"] = {"brazos": act, "costo_y_tiempo_de_actualizar": datos_act,
                                "brazos_referencias_originales": armar("_actualizacion", "preguntas_actualizacion.jsonl",
                                                                       "juicios_actualizacion_referencias_originales.jsonl")}
    (RES / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RES / "resumen.md").write_text(resumen(out), encoding="utf-8")
    print((RES / "resumen.md").read_text(encoding="utf-8"))
    return 0


def pct(d: dict, k: str) -> str:
    return f"{d.get(k, 0):.1f}%"


def tabla_brazos(brazos: dict) -> list[str]:
    l = ["| Brazo | Puntaje | Correcta | Parcial | Incorrecta | Costo/consulta (media) | Latencia (mediana) | Llamadas/consulta |",
         "|---|---|---|---|---|---|---|---|"]
    for b in BRAZOS:
        m = brazos[b]
        e = m["exactitud"]
        l.append(f"| {b} | {e['puntaje']:.3f} | {pct(e, 'pct_correcta')} | {pct(e, 'pct_parcial')} | "
                 f"{pct(e, 'pct_incorrecta')} | USD {m['costo_usd']['media']:.5f} | {m['latencia_s']['mediana']:.1f} s | "
                 f"{m['llamadas_por_pregunta']['media']:.2f} |")
    return l


def resumen(out: dict) -> str:
    l = ["# Resumen de resultados", "",
         f"Modelo: {out['meta']['modelo_respuesta']} (responde y juzga). Corrida principal sobre el tag linea-base "
         f"({out['meta']['commit']['linea_base_corrida_principal']}). "
         f"Puntaje: {out['meta']['puntaje']}.", "", "## Corrida principal (50 preguntas)", ""]
    l += tabla_brazos(out["brazos"])
    e = out["brazos"].get("_estabilidad_juez")
    if e:
        l += ["", f"Juez: voto mayoritario de {e['corridas']} corridas. De {e['respuestas']} respuestas: "
              f"{e.get('unanime', 0)} unánimes, {e.get('dos_a_uno', 0)} 2 a 1, {e.get('todas_distintas', 0)} con tres veredictos distintos. "
              "Puntaje por corrida: " + "; ".join(f"{b} {', '.join(f'{x:.2f}' for x in v)}" for b, v in e["puntaje_por_corrida"].items()) + "."]
    l += ["", "Con las referencias originales (una corrida del juez, sin la corrección de las 10 sin_respuesta y U05):", ""]
    l += tabla_brazos(out["brazos_referencias_originales"])
    l += ["", "### Puntaje por tipo de pregunta", "", "| Tipo | " + " | ".join(BRAZOS) + " |", "|---" * 4 + "|"]
    for c in CLASES:
        celdas = []
        for b in BRAZOS:
            d = out["brazos"][b]["por_tipo"].get(c)
            celdas.append(f"{d['puntaje']:.2f} ({d['correcta']}/{d['n']})" if d else "-")
        l.append(f"| {c} | " + " | ".join(celdas) + " |")
    l += ["", "### Fuentes (etiqueta del juez)", "", "| Brazo | correcta | parcial | incorrecta | no_aplica |", "|---|---|---|---|---|"]
    for b in BRAZOS:
        f = out["brazos"][b]["fuente_juez"]
        l.append(f"| {b} | " + " | ".join(str(f[k]) for k in FUENTES) + " |")
    p = out["preparacion"]
    l += ["", "## Preparación", "",
          f"- Wiki: ingesta de {p['wiki']['documentos']} documentos USD {p['wiki']['ingesta_costo_usd']:.4f} en "
          f"{p['wiki']['ingesta_segundos'] / 60:.1f} min + lint USD {p['wiki']['lint_costo_usd']:.4f} "
          f"({p['wiki']['lint_pasadas']} pasadas); {p['wiki']['paginas']} páginas.",
          f"- RAG: indexación local en {p['rag']['indexacion_segundos']} s, USD 0.",
          f"- Contexto: {p['contexto']['nota']}"]
    if out.get("actualizacion"):
        l += ["", "## Prueba de actualización (10 preguntas sobre 3 documentos modificados)", ""]
        l += tabla_brazos(out["actualizacion"]["brazos"])
        l += ["", "Con las referencias originales:", ""]
        l += tabla_brazos(out["actualizacion"]["brazos_referencias_originales"])
        l += ["", "```json", json.dumps(out["actualizacion"]["costo_y_tiempo_de_actualizar"], ensure_ascii=False, indent=1), "```"]
    a = out.get("acuerdo_humano_juez", {})
    if a.get("v1"):
        l += ["", f"Acuerdo humano vs. juez (muestra de 15): v1 {a['v1']['acuerdo']}/{a['v1']['n']} (kappa {a['v1']['kappa']}), "
              f"v2 {a['v2']['acuerdo']}/{a['v2']['n']} (kappa {a['v2']['kappa']}). {a['nota']}"]
    return "\n".join(l) + "\n"


if __name__ == "__main__":
    sys.exit(main())
