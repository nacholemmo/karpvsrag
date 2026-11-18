# Resumen de resultados

Modelo: claude-haiku-5-5 (responde y juzga). Commit: 56262a8. Puntaje: correcta + 0,5 × parcial, sobre el total de preguntas.

## Corrida principal (50 preguntas)

| Brazo | Puntaje | Correcta | Parcial | Incorrecta | Costo/consulta (media) | Latencia (mediana) | Llamadas/consulta |
|---|---|---|---|---|---|---|---|
| contexto | 0.960 | 94.0% | 4.0% | 2.0% | USD 0.00134 | 2.2 s | 1.00 |
| rag | 0.810 | 70.0% | 22.0% | 8.0% | USD 0.00054 | 2.2 s | 1.00 |
| wiki | 0.870 | 78.0% | 18.0% | 4.0% | USD 0.00259 | 5.0 s | 3.04 |

### Puntaje por tipo de pregunta

| Tipo | contexto | rag | wiki |
|---|---|---|---|
| dato | 1.00 (10/10) | 1.00 (10/10) | 1.00 (10/10) |
| procedimiento | 1.00 (10/10) | 0.55 (3/10) | 0.90 (8/10) |
| cruce | 1.00 (10/10) | 0.85 (8/10) | 0.90 (8/10) |
| contradiccion | 1.00 (5/5) | 0.80 (3/5) | 0.90 (4/5) |
| version | 1.00 (5/5) | 0.70 (3/5) | 0.80 (4/5) |
| sin_respuesta | 0.80 (7/10) | 0.90 (8/10) | 0.70 (5/10) |

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

Acuerdo humano vs. juez (muestra de 15): v1 11/15 (kappa 0.4915), v2 12/15 (kappa 0.5833). v2 se calculó después de ajustar la rúbrica y dos referencias mirando estas mismas 15 respuestas; las etiquetas de fuente y el veredicto de un caso los completó Claude a pedido del usuario.
