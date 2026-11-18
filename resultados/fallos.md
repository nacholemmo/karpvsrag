# Los 10 fallos más interesantes

Todos salen de la corrida real: Haiku 5.5 responde y juzga. Las respuestas completas están en `resultados/respuestas_*.jsonl` y los juicios en `resultados/juicios*.jsonl`. Hay ocho fallos de respuestas (RAG, wiki, contexto y la propia evaluación) y dos del proceso de construir la wiki.

---

## 1. RAG: el documento con el dato no entra en el top-8 (P32, cruce)

- **Pregunta:** con qué frecuencia se audita a los proveedores. El procedimiento de alta remite a la Política de Calidad, que dice "auditoría anual".
- **Qué pasó:** los 8 fragmentos recuperados venían de compras: el procedimiento de alta, la política de compras, el manual 2023, las actas y la reposición. Ninguno era de `politica-calidad-inocuidad.md`. El modelo respondió, con honestidad, que la política "no fue incluida".
- **Causa:** la pregunta usa el vocabulario de compras ("proveedor", "alta") y el dato vive en un documento de calidad. Es el único fallo de recuperación por documento sobre 40 preguntas con respuesta (recall top-8 = 39/40, `resultados/recall_rag.json`).

## 2. RAG: el documento entra, el fragmento no (P19, P11 y P44; procedimientos 3/10)

- **Qué pasó:**
  - En P19 (qué hacer ante una ausencia por enfermedad) el top-8 incluía `reglamento-interno.md`, pero llegaron sus fragmentos `#6` y `#7`, no el `#3` con los artículos de aviso y certificado. La respuesta dijo que el procedimiento "no fue provisto".
  - En P11 (gestión de mora) llegaron partes del instructivo, pero no los fragmentos con el mail de intimación y la carta documento.
  - Lo mismo afectó a una pregunta de versión, P44 (cuántas cotizaciones para una compra de $ 8.000.000): `politica-compras.md` entró al top-8, pero no el fragmento del artículo de cotizaciones, y la respuesta fue "los fragmentos no indican la cantidad".
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

## 7. Wiki: la actualización incremental dejó valores viejos vigentes en páginas no reescritas (U05)

- **Qué pasó:** después de modificar 3 documentos, la reingesta incremental (USD 0,049) reescribió las páginas principales con el valor nuevo y el viejo marcado como "Antes (reemplazado)". Pero no tocó otras páginas que repetían esos datos:
  - `wiki/proceso/circuito-de-compra.md` (líneas 6, 7 y 20) sigue diciendo que el Jefe de Compras aprueba "hasta $ 2.000.000" y que los frescos no requieren cotizaciones;
  - `wiki/proceso/reclamo-hermanos-lutz-sucursal-4.md:16` sigue con el umbral de $ 500.000.

  En U05, la consulta citó `circuito-de-compra.md`. Con la referencia original quedó `parcial`; con la referencia corregida, que reconoce la ambigüedad del artículo 13, los tres juicios dieron `correcta`. El error de la wiki sigue ahí aunque esta pregunta no lo penalice.
- **Causa:** el agente de ingesta actualiza las páginas que encuentra desde el documento que procesa. Nadie revisa las otras páginas que copiaron el dato. El lint en código (0 errores) tampoco lo detecta: el valor viejo sigue siendo textual en el documento, dentro del historial de cambios.
- **Por qué importa:** en una wiki compilada, cada dato duplicado es un lugar más para desactualizarse. El costo bajo de la actualización (USD 0,049) es el costo de una actualización **incompleta**.

## 8. La evaluación también falla: referencias de "sin respuesta" que castigaban respuestas fieles al corpus

- **Qué pasó:** en las preguntas sin respuesta, varias referencias omitían cosas que el corpus sí dice sobre el tema, y el juez castigaba a las respuestas que las mencionaban. Por ejemplo:
  - **P25:** las notas del turno noche registran que el supervisor sugirió llamar a la policía y a Walter (`corpus/notas-turno-noche.md:13`).
  - **P22/P49:** el acta de compras dice que Ernesto lo tiene que hablar con Claudio "y seguro con Comercial y Administración" (`corpus/acta-compras-quincenal.md:40`).
  - **P46:** el acta del comité registra que hoy se condona "según quién lo pida" y que Marta prepara la propuesta.

  La referencia de P25 además citaba un artículo sobre siniestros que el recorte del corpus había eliminado.
- **Sesgo en la corrección:** con referencias originales, esto castigaba 5 veces a la wiki, 2 al contexto y 1 al RAG. Primero se corrigió solo P25, que favorecía al contexto y al RAG; lo detectó la revisión independiente. Después se aplicó un mismo criterio a las 10 preguntas sin respuesta y a U05: la referencia incluye lo que el corpus dice y saca lo que no dice. Las referencias las revisó un subagente que no vio ninguna respuesta, y se volvieron a juzgar las 33 respuestas afectadas.
- **Reporte:** `results.json` informa los dos puntajes, con referencias originales (una corrida del juez) y corregidas (voto de 3). Una sola referencia defectuosa mueve hasta 0,03 el puntaje de un brazo.
- **Cuánto pesa la referencia y cuánto el ruido del juez:**
  - Al volver a juzgar las 30 respuestas `sin_respuesta` con las referencias corregidas, cambiaron 12 veredictos.
  - Con referencias fijas, el juez es bastante estable: en 3 corridas independientes, **139 de 150 veredictos fueron unánimes**, 11 fueron 2 a 1 y ninguno tuvo tres veredictos distintos. El puntaje por brazo varió como mucho 0,03 entre corridas (RAG 0,81-0,84).
  - La mayor parte del cambio vino de las referencias, no del azar.
- **Resultado:** con voto mayoritario de 3 juicios y referencias corregidas, el puntaje global queda en contexto 0,98, wiki 0,87 y RAG 0,83. La wiki sigue en 5/10 en las preguntas sin respuesta: tiende a agregar contexto del corpus que el juez lee como "completar el hueco".
- **Otro hallazgo de la revisión, que no se cambió:** el juez fue inconsistente en P46, porque marcó `correcta` la respuesta del RAG, que derivaba a la misma persona que las respuestas marcadas `incorrecta`.

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
