# ESTADO

**Fase actual:** 3 (Brazos) implementada y revisada. Falta el OK del usuario para cerrarla. Próxima: fase 4 (corrida y resultados), con plan a aprobar.

## Hecho
- **Fase 1** (corpus, 91,7k tokens) y **fase 2** (50 preguntas, juez Haiku, acuerdo humano vs. juez de 80% en v2): cerradas.
- **Fase 3:**
  - Tres brazos con formato común: `brazos/contexto`, `brazos/rag` y `brazos/wiki`.
  - Las 5 preguntas de prueba (P03, P14, P27, P37, P48) dan correcta en los tres brazos con la wiki v3 (`resultados/prueba_fase3/`).
  - Revisión independiente hecha y corregida: filtración en `ESQUEMA.md`, tope de contexto, excepciones de archivos, RAG con e5 a 512 tokens.
  - Wiki v3 reconstruida con el harness y el esquema finales: ingesta USD 0,543, lint USD 0,06, 52 páginas, lint sin errores.
- **Gasto real acumulado de la API:** USD 1,876. Por brazo, en `logs/llamadas.jsonl`: la ingesta de la wiki suma 1,61 entre las tres versiones y el lint 0,16. Saldo aproximado: USD 1,96.

## Pendiente
- [ ] OK del usuario para cerrar la fase 3.
- [ ] Plan de la fase 4: 50 preguntas × 3 brazos, juicios, `results.json`, prueba de actualización (3 documentos modificados y 10 preguntas nuevas) y `fallos.md`.

## Notas para la fase 4
- **Errores de contenido de la wiki que detectó la revisión de la fase 3** (sobre la v2; revisar si siguen en la v3):
  - V6 registrada como contradicción;
  - C5 no registrada;
  - huecos desactualizados por la ingesta cronológica.
- **Candidatos para `fallos.md`:** las sesiones de ingesta sin escrituras (v1), el índice truncado (v1), la filtración del esquema (v2) y el agente de lint que corrige de a poco.
- **Inconsistencias accidentales del corpus que encontró la revisión:**
  - orden de compra en Lapacho vs. Tacuarí;
  - efectivo "exclusivamente contra recibo oficial" vs. la constancia del FAQ de vendedores.
