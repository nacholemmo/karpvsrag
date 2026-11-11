# ESTADO

**Fase actual:** 2 (Evals). Implementada y revisada. Falta la revisión manual del usuario y calcular el acuerdo.

## Hecho
- **Fase 1 (corpus):** cerrada con el OK del usuario. El 11/11/2026 el corpus se recortó a 91,7k tokens de Haiku 5.5, para quedar bajo el umbral de precio de 100k.
- **Fase 2:**
  - `comun/`: configuración, precios, cliente con log JSONL y tope por corrida, formato de respuesta.
  - 50 preguntas en `evals/preguntas.jsonl`, con su validador.
  - Rúbrica (`evals/RUBRICA.md`) y juez (`evals/juez.py`), con el control en código `fuente_exacta`.
  - Revisión independiente hecha y sus correcciones aplicadas.
  - **Muestra:** 9 respuestas reales (Haiku con contexto completo y caché) más 6 sintéticas, las 15 juzgadas por Haiku. Se exportó `evals/revision_manual.csv` a ciegas.
- **Gasto real acumulado de la API:** USD 0,0271 en 24 llamadas (ver `logs/llamadas.jsonl`). La caché funciona: la primera llamada escribe ~92k tokens y las siguientes cuestan ~USD 0,001.

## Pendiente
- [ ] El usuario completa `tu_veredicto`, `tu_fuente` y `notas` en `evals/revision_manual.csv`, sin abrir `evals/juicios_muestra.jsonl`, `evals/mapa_revision.json` ni `evals/etiquetas_sinteticas.jsonl`.
- [ ] Correr `scripts/acuerdo.py`, que genera `evals/acuerdo.md`. Si el acuerdo es bajo, ajustar la rúbrica antes de la fase 3.
- [ ] OK del usuario para cerrar la fase 2 y planificar la fase 3 (brazos).

## Próximos pasos
Con el acuerdo calculado, plan de la fase 3: contexto completo, RAG con embeddings locales y BM25, y wiki con ingesta, consulta y lint.
