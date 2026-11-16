# CLAUDE.md: memoria del proyecto

Experimento que compara tres formas de responder preguntas sobre unos 50 documentos de procesos de una empresa ficticia:

1. contexto completo;
2. RAG híbrido (embeddings + BM25);
3. una wiki LLM estilo Karpathy.

Para retomar el trabajo alcanza con leer este archivo y `ESTADO.md`.

## Forma de trabajo (pedida por el usuario)

- El trabajo va por fases. En cada una: plan, aprobación del usuario, implementación y revisión. **No se avanza de fase sin su OK.**
- La revisión la hace un subagente que no vio la implementación: corre el código, busca errores y verifica los criterios de la fase. Se corrige lo que encuentre antes de avanzar.
- Al cerrar cada fase se actualizan este archivo y `ESTADO.md`.
- Si algo es ambiguo, se pregunta antes de asumir.
- Commits chicos al cerrar cada fase, con mensajes claros. **Nunca hacer push** (lo hace el usuario).

## Reglas técnicas

- Python 3.12 (`.python-version`) con entorno `uv` en `.venv/`. Las dependencias van pinneadas en `requirements.txt`.
- Proveedor de API: **Anthropic**. La clave sale de `ANTHROPIC_API_KEY`. Los modelos salen de `MODELO_RESPUESTA` (el mismo en los tres brazos) y `MODELO_JUEZ`. Ver `.env.example`.
- Cada llamada a la API se registra en un log JSONL con brazo, pregunta, tokens de entrada y salida, costo y latencia. Los logs crudos van en `logs/` (no se versionan) y los agregados en `resultados/`.
- Antes de cada corrida completa se estima el costo y se pide confirmación. Siempre se prueba primero con 5 preguntas.
- Solo se publican números reales salidos de las corridas.
- Todo es sintético: ninguna empresa, persona ni dato real.

## Reglas de repo (va a ser público)

- Se versionan `corpus/`, `hechos.csv`, `diseno/`, las preguntas, la `wiki/` generada, `resultados/` y `site/`.
- No se versionan `.env`, entornos, cachés, índices ni embeddings (ver `.gitignore`).
- Chequeo antes de cada commit: `bash scripts/chequeo_publico.sh`, que busca claves, rutas personales y el
  usuario local. Además se revisa a mano que no haya nombres de empresas reales.
- El README va en español.

## Decisiones de la fase 1 (corpus)

- **Tamaño del corpus:** se midió con `count_tokens` en la fase 2: 130,6k tokens con el tokenizador de Haiku 5.5. La estimación por caracteres/4 de la fase 1 lo subestimaba. Se recortaron 39 documentos, conservando todos los hechos y lo que usan las preguntas, y el prompt completo quedó en **91,7k tokens**, por debajo del umbral de 100k de Haiku. El validador estima con 2,34 caracteres por token, calibrado.
- **Empresa ficticia:** Distribuidora Quebracho Azul S.A., en el Gran Rosario, Argentina. Montos en ARS con formato `$ 1.500.000`. "Hoy", para el corpus, es noviembre de 2025.
- **`diseno/`** guarda el diseño y queda fuera de `corpus/`, así ningún brazo lo lee:
  - `empresa.md`: la biblia, con personas, sistemas y línea de tiempo;
  - `catalogo.csv`: los 50 documentos, con formato, largo, prolijidad y tanda;
  - `huecos.csv`: temas que el corpus roza sin responder (base de las preguntas "sin respuesta").
- **`hechos.csv`** es la fuente de verdad. `texto` es una cadena literal que debe aparecer en su documento.
  - `tipo` ∈ {monto, plazo, porcentaje, responsable, paso_procedimiento, excepcion, referencia_cruzada, version, contradiccion, seccion, dato}.
  - `grupo` admite varios valores separados por `;`: `V*` para versiones vieja/nueva (tipo `version`), `C*` para contradicciones (tipo `contradiccion`, exactamente 5) y `X*` para cruces entre documentos.
  - Los hechos viejos tienen `reemplazado=si` y `reemplazado_por=<hecho_id>`.
- **Contradicciones (C1-C5):** ninguno de los dos documentos indica cuál prevalece. La única cita entre pares es C4: el Manual de Depósito remite a la Política de Calidad solo por las temperaturas (cruce X8), y el validador lo reporta como aviso esperado. En las versiones (V1-V15), el documento nuevo puede decir que reemplaza al viejo o no.
- **Validador:** el match es literal con límites de palabra en los bordes alfanuméricos ("8%" no matchea dentro de "18%"). Solo se normalizan los espacios. La detección de citas entre pares C solo compara el título exacto del catálogo: no ve formas cortas como "la Política de Créditos".
- **Hechos agregados después del diseño:** H213 en adelante son datos o reglas que los redactores necesitaron. Cada uno lo dice en `notas`.
- **Herramienta de diseño:** no hay generador versionado. `hechos.csv` se edita directamente (con `csv` de Python, para respetar el quoting).
- Los documentos los escribieron subagentes en 5 tandas de 10, a partir de la biblia, el catálogo y sus hechos asignados. No podían inventar datos duros fuera de esas fuentes. Una revisión independiente encontró contradicciones accidentales (donación de mercadería, desbloqueo de cuentas), una C que en realidad era versión y matices que indicaban qué documento prevalecía. Todo eso quedó corregido.

## Decisiones de la fase 2 (evals)

- **Presupuesto:** el saldo de la API es chico (USD 3,84 a noviembre de 2026), así que todo va con **Haiku 5.5** (`claude-haiku-5-5`), que responde y juzga.
  - El sesgo de autoevaluación se declara como límite y se mide con la revisión manual.
  - Haiku 5.5 cobra 5× más si el prompt supera los 100k tokens: hay que medir con `scripts/contar_tokens.py`.
- **`comun/`:**
  - `llm.llamar()` loguea cada llamada en `logs/llamadas.jsonl` (no se versiona) con brazo, pregunta, tokens, caché, costo, latencia, `stop_reason` y `request_id`.
  - `Corrida` corta si el gasto supera `PRESUPUESTO_USD`. El chequeo es antes de cada llamada, así que se puede pasar por una.
  - Effort por defecto: `low`.
- **Formato común de los brazos:** `{"respuesta", "fuentes": [archivo.md]}`, con salida estructurada (`comun/formato.py`).
- **Preguntas** (`evals/preguntas.jsonl`): 50, 10 por tipo. `contradiccion_version` se divide en 5 contradicciones (C1-C5) y 5 versiones. Las 10 `sin_respuesta` cubren los 8 huecos, más 2 facetas extra de H2 y H4 (a propósito).
- **Documentos requeridos para la fuente** (`juez.documentos_requeridos`):
  - dato y procedimiento: al menos uno;
  - cruce: los documentos destino (con el dato, no el que remite, sin reemplazados);
  - contradicción: los dos;
  - versión: el vigente.

  `fuente_exacta` es el control en código. No reconoce documentos alternativos que también contienen el dato, así que puede discrepar con el juez.
- **Límite conocido:** en varios cruces el documento destino alcanza solo para responder. Se mide la llegada al dato, no el salto obligatorio entre documentos.
- **Juicios y respuestas con `stop_reason` distinto de `end_turn` o JSON inválido:** no se guardan, y se reintentan al volver a correr.
- **Revisión manual a ciegas:** `evals/revision_manual.csv` usa ids opacos (`caso-NN`). El mapeo está en `evals/mapa_revision.json` y las etiquetas pretendidas de las 6 sintéticas en `evals/etiquetas_sinteticas.jsonl`. No hay que mirarlos antes de revisar.

- **Calibración del juez:** con la revisión manual se corrigieron P01 y P22 y se ajustó la rúbrica (v1 → v2). El juez Haiku no es determinista, así que conviene reportar su variación cuando se re-juzgue.

## Comandos

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv -r requirements.txt
.venv/bin/python scripts/validar_hechos.py              # validación completa (criterio de cierre de la fase 1)
.venv/bin/python scripts/validar_hechos.py --parcial --tanda N
.venv/bin/python -m pytest -q
.venv/bin/python scripts/validar_preguntas.py
.venv/bin/python scripts/contar_tokens.py                  # gratis (count_tokens)
.venv/bin/python evals/muestra.py estimar                  # costo estimado, sin API
.venv/bin/python evals/muestra.py responder --limite 5     # primero 5, después sin --limite
.venv/bin/python evals/juez.py --respuestas evals/muestra_respuestas.jsonl --respuestas evals/respuestas_sinteticas.jsonl --salida evals/juicios_muestra.jsonl
.venv/bin/python evals/muestra.py exportar                 # revision_manual.csv a ciegas
.venv/bin/python scripts/acuerdo.py                        # cuando el CSV esté completo
```
