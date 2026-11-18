# Resumen de resultados

Modelo: claude-haiku-5-5 (responde y juzga). Commit: ddfdd63. Puntaje: correcta + 0,5 × parcial, sobre el total de preguntas.

## Corrida principal (50 preguntas)

| Brazo | Puntaje | Correcta | Parcial | Incorrecta | Costo/consulta (media) | Latencia (mediana) | Llamadas/consulta |
|---|---|---|---|---|---|---|---|
| contexto | 0.970 | 96.0% | 2.0% | 2.0% | USD 0.00134 | 2.2 s | 1.00 |
| rag | 0.820 | 72.0% | 20.0% | 8.0% | USD 0.00054 | 2.2 s | 1.00 |
| wiki | 0.870 | 78.0% | 18.0% | 4.0% | USD 0.00259 | 5.0 s | 3.04 |

### Puntaje por tipo de pregunta

| Tipo | contexto | rag | wiki |
|---|---|---|---|
| dato | 1.00 (10/10) | 1.00 (10/10) | 1.00 (10/10) |
| procedimiento | 1.00 (10/10) | 0.55 (3/10) | 0.90 (8/10) |
| cruce | 1.00 (10/10) | 0.85 (8/10) | 0.90 (8/10) |
| contradiccion | 1.00 (5/5) | 0.80 (3/5) | 0.90 (4/5) |
| version | 1.00 (5/5) | 0.70 (3/5) | 0.80 (4/5) |
| sin_respuesta | 0.85 (8/10) | 0.95 (9/10) | 0.70 (5/10) |

### Fuentes (etiqueta del juez)

| Brazo | correcta | parcial | incorrecta | no_aplica |
|---|---|---|---|---|
| contexto | 39 | 1 | 0 | 10 |
| rag | 38 | 0 | 2 | 10 |
| wiki | 36 | 3 | 1 | 10 |

## Preparación

- Wiki: ingesta de 50 documentos USD 0.5434 en 42.2 min + lint USD 0.0601 (3 pasadas); 52 páginas.
- RAG: indexación local en 34.7 s, USD 0.
- Contexto: Sin preparación. La primera llamada de cada corrida escribe ~92k tokens en caché (~USD 0,012).

## Prueba de actualización (10 preguntas sobre 3 documentos modificados)

| Brazo | Puntaje | Correcta | Parcial | Incorrecta | Costo/consulta (media) | Latencia (mediana) | Llamadas/consulta |
|---|---|---|---|---|---|---|---|
| contexto | 1.000 | 100.0% | 0.0% | 0.0% | USD 0.00220 | 2.4 s | 1.00 |
| rag | 0.850 | 80.0% | 10.0% | 10.0% | USD 0.00058 | 3.1 s | 1.00 |
| wiki | 0.950 | 90.0% | 10.0% | 0.0% | USD 0.00275 | 5.2 s | 3.00 |

```json
{
 "documentos_modificados": [
  "politica-compras.md",
  "procedimiento-reclamos-v2.md",
  "reglamento-interno.md"
 ],
 "contexto": {
  "costo_usd": 0.0,
  "segundos": 0.0,
  "nota": "No hay nada que reconstruir. La primera consulta después del cambio reescribe la caché del corpus: costó USD 0.0117, contra ~USD 0,0012 de una consulta con caché caliente."
 },
 "rag": {
  "costo_usd": 0.0,
  "segundos": 33.3,
  "fragmentos": 389,
  "nota": "Reindexación local completa (sin reindexado incremental): se recalculan todos los embeddings."
 },
 "wiki": {
  "costo_usd": 0.049178,
  "segundos": 193.8,
  "turnos": 16,
  "paginas_escritas": [
   "wiki/index.md",
   "wiki/politica/aprobacion-de-compras.md",
   "wiki/politica/horas-extras.md",
   "wiki/politica/politica-de-compras.md",
   "wiki/politica/reglamento-interno-personal.md",
   "wiki/proceso/procedimiento-de-reclamos.md"
  ],
  "lint": "0 errores después de la reingesta; no hizo falta corrección con agente (USD 0)",
  "nota": "Reingesta incremental de los 3 documentos sobre la wiki v3."
 }
}
```

Acuerdo humano vs. juez (muestra de 15): v1 11/15 (kappa 0.4915), v2 12/15 (kappa 0.5833). v2 se calculó después de ajustar la rúbrica y dos referencias mirando estas mismas 15 respuestas; las etiquetas de fuente y el veredicto de un caso los completó Claude a pedido del usuario.
