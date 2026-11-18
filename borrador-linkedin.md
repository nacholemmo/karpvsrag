Quise ver qué funciona mejor para responder preguntas sobre los procesos de una empresa: meter todos los documentos en el prompt, buscar solo los fragmentos relevantes (RAG) o dejar que un agente compile una wiki, como propuso Karpathy.

Armé una distribuidora ficticia con 50 documentos llenos de trampas: versiones viejas que nadie borró, manuales que se contradicen y preguntas que la documentación no responde. Usé el mismo modelo en los tres casos y un juez con rúbrica.

Con el corpus entero en el contexto, el puntaje fue 0,98 sobre 1. La wiki llegó a 0,87 y el RAG a 0,83. Al RAG le costaron los procedimientos: traía el documento correcto, pero no siempre el fragmento con todos los pasos.

La sorpresa vino de la wiki. El agente que la compilaba a veces daba un documento por terminado sin haber escrito una sola página. La política de créditos vigente nunca llegó a la wiki, y me enteré porque respondió con la tasa de mora vieja. Corregí el programa que la armaba y la reconstruí.

Ojo con generalizar: el corpus es sintético y entra entero en el contexto. Con miles de documentos la cuenta cambia. Además, el mismo modelo que respondía hizo de juez.

Datos, código y cada respuesta están publicados para auditarlos.
https://contexto-vs-rag-vs-wiki.onrender.com · https://github.com/nacholemmo/karpvsrag

¿Ustedes cómo resuelven las consultas sobre documentación interna?
