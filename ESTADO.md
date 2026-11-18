# ESTADO

**Fase actual:** proyecto completo. Las 6 fases están cerradas con el OK del usuario.

## Hecho
1. **Corpus:** 50 documentos sintéticos, 232 hechos plantados y validador. Recortado a 91,7k tokens de Haiku 5.5.
2. **Evals:** 50 preguntas y juez Haiku con rúbrica. Acuerdo humano vs. juez del 73% (v1) y 80% (v2).
3. **Brazos:** contexto completo, RAG híbrido (e5-small + BM25 + RRF) y wiki estilo Karpathy (v3).
4. **Resultados:** 50 preguntas × 3 brazos, voto de 3 juicios.

   | Brazo | Puntaje |
   |---|---|
   | contexto | 0,98 |
   | wiki | 0,87 |
   | RAG | 0,83 |

   Actualización: contexto 1,00, wiki 1,00 (con la actualización incompleta documentada) y RAG 0,90. Más `fallos.md`, `results.json` y el tag `linea-base`.
5. **Landing:** `site/` (estática, Render con `render.yaml`).
6. **Post:** `borrador-linkedin.md` (219 palabras, revisado contra los datos).

**Gasto real total de la API:** USD 2,46 (ver `logs/llamadas.jsonl`).

## Pendientes del usuario
- [ ] Completar `REPO_URL` en `site/config.js`.
- [ ] Pushear con el tag: `git push && git push --tags`.
- [ ] Publicar en Render: blueprint `render.yaml`, o Static Site con *Publish directory* `site` y sin build.
- [ ] Reemplazar `[link a la landing]` y `[link al repo]` en `borrador-linkedin.md` y en el README ("se agrega al publicar").
