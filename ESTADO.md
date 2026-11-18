# ESTADO

**Fase actual:** 5 (landing) implementada y revisada. Falta el OK del usuario para cerrarla. Próxima: fase 6 (borrador del post).

## Hecho
- **Fases 1 a 3:** cerradas. Corpus de 91,7k tokens, 50 preguntas con juez Haiku y tres brazos (wiki v3).
- **Fase 4:**
  - Corrida principal: 50 × 3, más 3 corridas del juez. Tag `linea-base`.
  - Prueba de actualización: 3 documentos y 10 preguntas.
  - `results.json`, `resumen.md` y `fallos.md`.
  - Revisión independiente hecha y corregida (fallo falso reemplazado; referencias `sin_respuesta` y U05 corregidas de forma uniforme y re-juzgadas).
  - README con resultados y límites.
- **Resultados (voto de 3, referencias corregidas):**

  | Brazo | Puntaje | USD por consulta |
  |---|---|---|
  | contexto | 0,98 | 0,0013 |
  | wiki | 0,87 | 0,0026 |
  | RAG | 0,83 | 0,0005 |

  Actualización: contexto 1,00, wiki 1,00 (actualización incompleta, ver `fallos.md` #7) y RAG 0,90.
- **Gasto real acumulado de la API:** USD 2,46 (ver `logs/llamadas.jsonl`). Saldo aproximado: USD 1,38.

## Pendiente
- [x] Fase 4 cerrada.
- [x] Fase 5: landing en `site/`, revisada por un subagente (correcciones aplicadas). Falta el OK del usuario.
- [ ] Completar `REPO_URL` en `site/config.js` y publicar en Render (usuario).
- [ ] Fase 6: `borrador-linkedin.md`.
- [ ] Agregar al README el link a la landing cuando esté publicada.
- [ ] Push: lo hace el usuario, incluido el tag `linea-base`.
