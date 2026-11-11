# Contexto completo vs. RAG vs. wiki LLM

Este experimento compara tres formas de responder preguntas sobre unos 50 documentos de procesos de una distribuidora mayorista de alimentos **ficticia**:

1. **Contexto completo:** todos los documentos van en el prompt.
2. **RAG híbrido:** fragmentos, embeddings locales y BM25, con fusión de rankings.
3. **Wiki LLM al estilo Karpathy:** un agente compila los documentos en una wiki Markdown y responde navegándola.

> En construcción. Las instrucciones completas, los resultados y los límites se agregan al cerrar las fases siguientes.

## Estado actual

Fase 1, el corpus sintético. Para validar que cada hecho plantado aparece en su documento:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt
.venv/bin/python scripts/validar_hechos.py
```

## Licencia

MIT. Todo el contenido es sintético: la empresa, las personas y los datos son inventados.
