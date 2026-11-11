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

- **Empresa ficticia:** Distribuidora Quebracho Azul S.A., en el Gran Rosario, Argentina. Montos en ARS con formato `$ 1.500.000`. "Hoy", para el corpus, es noviembre de 2025.
- **`diseno/`** guarda el diseño y queda fuera de `corpus/`, así ningún brazo lo lee:
  - `empresa.md`: la biblia, con personas, sistemas y línea de tiempo;
  - `catalogo.csv`: los 50 documentos, con formato, largo, prolijidad y tanda;
  - `huecos.csv`: temas que el corpus roza sin responder (base de las preguntas "sin respuesta").
- **`hechos.csv`** es la fuente de verdad. `texto` es una cadena literal que debe aparecer en su documento.
  - `tipo` ∈ {monto, plazo, porcentaje, responsable, paso_procedimiento, excepcion, referencia_cruzada, version, contradiccion, seccion, dato}.
  - `grupo` admite varios valores separados por `;`: `V*` para versiones vieja/nueva (tipo `version`), `C*` para contradicciones (tipo `contradiccion`, exactamente 5) y `X*` para cruces entre documentos.
  - Los hechos viejos tienen `reemplazado=si` y `reemplazado_por=<hecho_id>`.
- **Contradicciones:** en ellas ningún documento menciona al otro. En las versiones, el documento nuevo puede decir que reemplaza al viejo.
- Los documentos los escribieron subagentes en 5 tandas de 10, a partir de la biblia, el catálogo y sus hechos asignados. No pueden inventar datos duros fuera de esas fuentes.

## Comandos

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv -r requirements.txt
.venv/bin/python scripts/validar_hechos.py              # validación completa (criterio de cierre de la fase 1)
.venv/bin/python scripts/validar_hechos.py --parcial --tanda N
.venv/bin/python -m pytest -q
```
