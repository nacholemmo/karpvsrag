# Contexto completo vs. RAG vs. wiki LLM

Este experimento compara tres formas de responder preguntas sobre 50 documentos de procesos de una distribuidora mayorista de alimentos **ficticia**:

1. **Contexto completo:** todos los documentos van en el prompt (~92k tokens, con caché).
2. **RAG híbrido:** fragmentos por sección, embeddings locales (`multilingual-e5-small`) y BM25, fusionados con Reciprocal Rank Fusion. Al modelo le llegan los 8 mejores fragmentos.
3. **Wiki LLM al estilo Karpathy:** un agente compila los documentos en una wiki Markdown (`wiki/`, siguiendo `ESQUEMA.md`), y otro agente responde navegando **solo** esa wiki.

Los tres brazos usan el mismo modelo (Claude Haiku 5.5) y devuelven el mismo formato: respuesta más fuentes citadas.

> Landing con resultados y gráficos: *(link a Render, se agrega al publicar)*

## Resultados (50 preguntas)

| Brazo | Puntaje | Correctas | Costo por consulta | Latencia (mediana) | Preparación |
|---|---|---|---|---|---|
| Contexto completo | **0,98** | 98% | USD 0,0013 | 2,2 s | ninguna |
| Wiki | 0,87 | 80% | USD 0,0026 | 5,0 s (3 llamadas) | USD 0,60 y 42 min (ingesta + lint) |
| RAG | 0,83 | 74% | USD 0,0005 | 2,2 s | 35 s de indexación local, USD 0 |

- **Puntaje:** correcta + 0,5 × parcial, por voto mayoritario de 3 corridas del juez. Hay 10 preguntas de cada tipo: dato puntual, procedimiento, cruce de documentos, contradicción o versión, y sin respuesta en el corpus.
- **Los tres sacan 10/10 en datos puntuales.**
- **El RAG** cae en procedimientos (0,60), porque recupera solo parte de los pasos.
- **La wiki** cae en las preguntas sin respuesta (0,65) y pierde datos al compilar. Por ejemplo, la frecuencia del inventario no quedó en ninguna página y una de las contradicciones plantadas nunca se registró.
- **Prueba de actualización** (3 documentos modificados, 10 preguntas nuevas):

  | Brazo | Puntaje | Costo de actualizar |
  |---|---|---|
  | Contexto | 1,00 | USD 0 |
  | Wiki | 1,00 | USD 0,049, incompleta: quedaron valores viejos en páginas que no se reescribieron |
  | RAG | 0,90 | 33 s de reindexación local |

Detalle completo en [`resultados/resumen.md`](resultados/resumen.md), [`resultados/results.json`](resultados/results.json) y los 10 fallos más interesantes, con su causa, en [`resultados/fallos.md`](resultados/fallos.md).

## Límites

- **Corpus chico y sintético:** 50 documentos de una empresa inventada, escritos por agentes, con defectos plantados (versiones, contradicciones, cruces y huecos). Con ~92k tokens, el corpus entra entero en el contexto; con un corpus mucho más grande, el contexto completo deja de ser viable y la comparación cambia.
- **Un solo modelo:** Claude Haiku 5.5, que además hace de juez, así que hay sesgo de autoevaluación. El acuerdo humano vs. juez se midió en una muestra de 15: 73% en la v1 de la rúbrica y 80% en la v2, ajustada mirando esa misma muestra.
- **Una sola corrida por brazo.** El juez se corrió 3 veces y fue unánime en 139/150 veredictos.
- **Preguntas y referencias escritas por agentes** a partir de `hechos.csv`. Después de la corrida se corrigieron las referencias de las 10 preguntas sin respuesta con un criterio uniforme. Se publican los dos puntajes, y la diferencia máxima entre ellos es de 0,02.
- **Prompts casi iguales en los tres brazos:** solo el del RAG dice "si los fragmentos no alcanzan, decilo".
- **La wiki se compiló tres veces:** la primera tenía bugs del harness y la segunda tenía un esquema que filtraba respuestas. Los resultados usan la tercera. El gasto de las versiones descartadas se informa aparte.

## Cómo reproducirlo

Requisitos: Python 3.12, [uv](https://docs.astral.sh/uv/) y una clave de la API de Anthropic, solo para los pasos que llaman al modelo.

```bash
git clone <este repo> && cd <repo>
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt   # incluye PyTorch para CPU
cp .env.example .env                                 # completar ANTHROPIC_API_KEY
```

**Sin gastar en la API:** todos los resultados, la wiki y las respuestas están versionados.

```bash
.venv/bin/python scripts/validar_hechos.py     # cada hecho plantado aparece textual en su documento
.venv/bin/python scripts/validar_preguntas.py  # 50 preguntas consistentes con hechos.csv y el corpus
.venv/bin/python -m pytest -q
.venv/bin/python scripts/resultados.py         # recalcula results.json desde las respuestas y los juicios
.venv/bin/python brazos/rag/indexar.py && .venv/bin/python scripts/recall_rag.py   # RAG local
.venv/bin/python brazos/wiki/lint.py           # chequeos de la wiki en código
```

**Corrida completa, con API.** Cada script estima o loguea el costo; el gasto real de este repo fue de unos USD 2,46 en total.

```bash
.venv/bin/python scripts/contar_tokens.py                        # gratis
.venv/bin/python brazos/wiki/ingesta.py                          # compila la wiki (~USD 0,55)
.venv/bin/python brazos/wiki/lint.py --corregir
.venv/bin/python brazos/correr.py --brazo contexto --prueba      # siempre primero 5 preguntas
.venv/bin/python brazos/correr.py --brazo contexto --todas --estimar
.venv/bin/python brazos/correr.py --brazo contexto --todas       # idem rag y wiki
.venv/bin/python evals/juez.py --respuestas resultados/respuestas_contexto.jsonl \
  --respuestas resultados/respuestas_rag.jsonl --respuestas resultados/respuestas_wiki.jsonl \
  --salida resultados/juicios.jsonl
.venv/bin/python scripts/resultados.py
```

Cada llamada queda registrada en `logs/llamadas.jsonl` (no versionado) con el brazo, la pregunta, los tokens, el costo y la latencia. `PRESUPUESTO_USD` corta una corrida que se pase del tope.

El tag `linea-base` marca el corpus de la corrida principal. Después se modificaron 3 documentos para la prueba de actualización (`git diff linea-base -- corpus/`).

## Landing (`site/`)

Sitio estático en HTML, CSS y JS sin paso de build. Lee `site/datos/results.json`, una copia que `scripts/resultados.py` escribe junto con `resultados/results.json`.

- **Ver la landing en local:** `python -m http.server -d site 8000` y abrir http://localhost:8000.
- **Antes de publicar:** completar la URL del repo en `site/config.js` (`REPO_URL`).
- **Publicar en Render**, de cualquiera de estas dos formas:
  - con el blueprint `render.yaml` (New → Blueprint);
  - a mano: New → Static Site, con *Publish directory* `site` y *Build command* vacío.

## Estructura

| Ruta | Contenido |
|---|---|
| `corpus/` | 50 documentos |
| `hechos.csv` | fuente de verdad de los datos plantados |
| `diseno/` | biblia de la empresa, catálogo y huecos |
| `evals/` | preguntas, rúbrica, juez y muestra de revisión manual |
| `brazos/` | contexto, RAG y wiki, más el runner común |
| `wiki/` | wiki compilada |
| `resultados/` | respuestas, juicios, métricas y fallos |
| `site/` | landing |
| `comun/` | cliente con log, costos y formato |

`CLAUDE.md` y `ESTADO.md` documentan las decisiones del proyecto.

## Licencia

MIT. Todo el contenido es sintético: la empresa, las personas y los datos son inventados.
