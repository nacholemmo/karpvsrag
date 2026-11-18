# Los 10 fallos más interesantes

Todos salen de la corrida real: Haiku 5.5 responde y juzga. Las respuestas completas están en `resultados/respuestas_*.jsonl` y los juicios en `resultados/juicios*.jsonl`. Hay ocho fallos de respuestas (RAG, wiki, contexto y la propia evaluación) y dos del proceso de construir la wiki.

---

## 1. RAG: el documento con el dato no entra en el top-8 (P32, cruce)

- **Pregunta:** con qué frecuencia se audita a los proveedores. El procedimiento de alta remite a la Política de Calidad, que dice "auditoría anual".
- **Qué pasó:** los 8 fragmentos recuperados venían de compras: el procedimiento de alta, la política de compras, el manual 2023, las actas y la reposición. Ninguno era de `politica-calidad-inocuidad.md`. El modelo respondió, con honestidad, que la política "no fue incluida".
- **Causa:** la pregunta usa el vocabulario de compras ("proveedor", "alta") y el dato vive en un documento de calidad. Es el único fallo de recuperación por documento sobre 40 preguntas con respuesta (recall top-8 = 39/40, `resultados/recall_rag.json`).

## 2. RAG: el documento entra, el fragmento no (P44, P19, P11; procedimientos 3/10)

- **Qué pasó:**
  - En P44 (cuántas cotizaciones pedir para una compra de $ 8.000.000) el top-8 incluía `politica-compras.md`, pero no el fragmento del artículo de cotizaciones. La respuesta fue "los fragmentos no indican la cantidad".
  - En P19 (ausencia por enfermedad) y P11 (gestión de mora) pasó lo mismo: llegaron partes del documento correcto, pero no las que tenían los pasos clave.
- **Causa:** los procedimientos están repartidos en varias secciones y el top-8 trae solo una parte. Por eso el RAG saca 0,55 en procedimientos, contra 1,00 del contexto completo y 0,90 de la wiki.
- **Lección:** el recall medido por documento (39/40) sobreestima la calidad de la recuperación. Lo que importa es el fragmento.

## 3. RAG después de la actualización: el cruce se corta en el documento que remite (U09)

- **Pregunta:** a partir de qué monto escala el reclamo de Hermanos Lutz, con el umbral ya actualizado a $ 400.000.
- **Qué pasó:** se recuperaron el mail del reclamo, actas y el instructivo de Mostrador, pero no `procedimiento-reclamos-v2.md`. Respuesta: "no hay valor concreto". Es el único `incorrecta` de los 30 de la prueba de actualización.
- **Causa:** es el mismo patrón del fallo 1. El mail usa el lenguaje del caso concreto, y el dato está en un procedimiento genérico al que el mail solo nombra.

## 4. RAG: ve la contradicción pero elige un ganador (P37, P40)

- **Qué pasó:** en P37 (conciliación de remitos: 48 horas en el manual contra 24 horas en la minuta) la respuesta mencionó los dos plazos y después eligió el del manual "por ser el documento formal". En P40 hizo lo mismo con el plazo de entrega. El juez marcó las dos como `parcial`.
- **Causa:** con fragmentos sueltos, el modelo infiere una jerarquía (manual > minuta) que el corpus no establece. El contexto completo, que ve los dos documentos enteros, dio 5/5 en contradicciones.

## 5. Wiki: un dato se pierde en la compilación (P41, versión)

- **Pregunta:** cada cuánto se hace el inventario general. Valor vigente: "dos veces por año", según el Manual de Depósito 2025.
- **Qué pasó:** la wiki respondió que "no define una periodicidad fija", que solo consta el inventario de junio y que el próximo es en diciembre. Juicio: `incorrecta`.
- **Causa:** "dos veces por año" no aparece en ninguna de las 52 páginas. Tampoco el valor viejo "una vez por año". Al compilar, el agente resumió el manual y dejó afuera ese dato. Como la consulta solo lee la wiki, no tiene forma de recuperarlo. Es el costo de la compresión.

## 6. Wiki: una contradicción plantada nunca se registró (P40, C5)

- **Pregunta:** en cuánto tiempo se entrega un pedido. El Manual del Vendedor dice "24 a 48 horas" y la FAQ de clientes dice "72 horas".
- **Qué pasó:** la wiki respondió solo "72 horas". `parcial`, con fuente `parcial`.
- **Causa:** "24 a 48" no figura en ninguna página. Del Manual del Vendedor, un documento largo, el agente solo extrajo el pedido mínimo y los descuentos. La contradicción no se pierde por mala redacción: se pierde porque uno de sus lados nunca entró a la wiki.

## 7. Wiki: el compilador inventa y la consulta lo repite (P22, P49; sin respuesta 0,70)

- **Qué pasó:** en P22 y P49 (quién lleva o aprueba presentarse a una licitación) la wiki respondió que "seguramente" intervengan Comercial y Administración. El juez lo tomó como completar un hueco.
- **Causa:** esa frase no está en el corpus. Está en `wiki/proceso/reunion-compras-quincenal.md:35`, escrita por el agente de ingesta. El acta solo dice que Ernesto lo tiene que hablar con Claudio.
- **Por qué importa:** la wiki "lavó" una especulación del compilador hasta convertirla en conocimiento con fuente, y la consulta la repitió con confianza. Es el peor tipo de error de este patrón: la cita `[fuente: acta-compras-quincenal.md]` le da una apariencia de respaldo que no tiene.

## 8. La evaluación también falla: una referencia incompleta castigaba respuestas fieles (P25)

- **Pregunta:** qué hacer si roban mercadería en ruta. Es un hueco sin procedimiento.
- **Qué pasó:** la referencia decía que las notas no registran nada, pero `corpus/notas-turno-noche.md:13` dice "le dije q llame a la policia y a walter pero la verdad NO SE, no tenemos nada escrito". El contexto y el RAG citaron esa frase y el juez los marcó `parcial` por "contradecir la referencia".
- **Corrección:** se completó la referencia y se re-juzgó P25 en los tres brazos (los juicios anteriores están en `resultados/juicios_P25_antes_de_corregir_referencia.jsonl`; queda registrado en `results.json`). Contexto y RAG pasaron de `parcial` a `correcta`.
- **Caso relacionado, sin corregir:** el único `incorrecta` del contexto completo es P46 (condonación de intereses). La respuesta deriva el caso a Marta Ifrán, que en el acta tiene a cargo preparar la propuesta. El juez lo leyó como completar el hueco de "quién aprueba". Es una zona gris, y la dejamos como está.

## 9. Proceso: el agente de ingesta "terminaba" sin escribir y leía un índice truncado (wiki v1)

- **Qué pasó:** en la primera compilación, 6 de 50 sesiones cerraron sin escribir ninguna página, entre ellas la Política de Créditos v2. En la prueba de la fase 3, la wiki contestó la tasa de mora vieja (2,5%) en lugar de la vigente (3%).
- **Causas:**
  - El agente intentaba escribir muchas páginas en un solo turno, la respuesta se cortaba por `max_tokens` y el harness lo tomaba como el final de la sesión.
  - La herramienta `leer` truncaba los archivos a 12k caracteres y el índice ya medía 17k, así que 14 páginas quedaron fuera de él.
- **Arreglo:** guardia de "sin escrituras", descarte del turno cortado por largo con el pedido de escribir de a una página, y un límite de lectura de 40k. Costo de esa versión, descartada: USD 0,477 (`resultados/ingesta_wiki_primera_pasada.json`).

## 10. Proceso: el esquema de la wiki filtraba respuestas de referencia (wiki v2)

- **Qué pasó:** los ejemplos de `ESQUEMA.md` eran literalmente respuestas de la evaluación:
  - "48 horas hábiles… antes 24 horas de recibida" (P43);
  - "$ 1.500.000" (P26);
  - "Lapacho" (P45).

  Como el esquema va en el system prompt de la ingesta y de la consulta, solo el brazo wiki las veía.
- **Cómo se detectó:** una revisión independiente; ningún test lo atrapaba.
- **Arreglo:** ejemplos ficticios, un test que falla si el esquema contiene cualquier elemento clave de las preguntas y la reconstrucción de la wiki (v3, USD 0,543).
- **Gasto total de la compilación de la wiki, sumando las dos versiones descartadas:** ~USD 1,61, frente a USD 0,54 de la versión final.
- **Fallo relacionado:** una llamada del lint llegó a 106.698 tokens de prompt y se cobró en el tramo caro de Haiku (más de 100k), porque el tope de contexto se chequeaba después de enviar y no antes.
