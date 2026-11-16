# ESTADO

**Fase actual:** 2 (Evals) cerrada con el OK del usuario. Próxima: fase 3 (brazos), con plan a aprobar.

## Hecho
- **Fase 1 (corpus):** cerrada con el OK del usuario. El 11/11/2026 el corpus se recortó a 91,7k tokens de Haiku 5.5, para quedar bajo el umbral de precio de 100k.
- **Fase 2:**
  - `comun/`: configuración, precios, cliente con log JSONL y tope por corrida, formato de respuesta.
  - 50 preguntas en `evals/preguntas.jsonl`, con su validador.
  - Rúbrica (`evals/RUBRICA.md`) y juez (`evals/juez.py`), con el control en código `fuente_exacta`.
  - Revisión independiente hecha y sus correcciones aplicadas.
  - **Muestra:** 9 respuestas reales (Haiku con contexto completo y caché) más 6 sintéticas, las 15 juzgadas por Haiku. Se exportó `evals/revision_manual.csv` a ciegas.
- **Caché:** funciona. La primera llamada escribe ~92k tokens y las siguientes cuestan ~USD 0,001.

- **Acuerdo humano vs. juez en veredicto:** v1 11/15 (73%, kappa 0,49); v2 12/15 (80%, kappa 0,58), después de corregir P01 y P22 y ajustar la rúbrica (algo inflado: se ajustó mirando estas 15). Contra las 6 sintéticas, el juez acierta 6/6 en v2 (5/6 en v1). Detalles en `evals/acuerdo.md` y `evals/acuerdo_v1.md`.
- **Gasto real acumulado de la API:** ver `logs/llamadas.jsonl`. Cerca de USD 0,04 al cierre de la fase 2.

## Próximos pasos
Plan de la fase 3: contexto completo, RAG con embeddings locales y BM25, y wiki con ingesta, consulta y lint.
