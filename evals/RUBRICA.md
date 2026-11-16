# Rúbrica del juez

El juez compara la respuesta de un brazo con la respuesta de referencia de la pregunta. Devuelve dos etiquetas y una justificación breve. Este archivo es, tal cual, la instrucción que recibe el modelo juez (`evals/juez.py` lo carga como system prompt), y es también la guía para la revisión manual.

## Qué recibe el juez

- La **pregunta** y su **tipo**: `dato`, `procedimiento`, `cruce`, `contradiccion_version` (subtipo `contradiccion` o `version`) o `sin_respuesta`.
- La **respuesta de referencia** y los **elementos clave**, que son las frases o valores que una respuesta correcta tiene que decir, con las mismas palabras o con otras equivalentes.
- El **comportamiento esperado**.
- Los **documentos fuente**, es decir, los archivos donde está la respuesta.
- La **respuesta evaluada** y las **fuentes que citó**.

## Etiqueta 1: `veredicto`

| Valor | Cuándo |
|---|---|
| `correcta` | Dice todos los elementos clave, con valores exactos (montos, plazos, responsables) o equivalentes sin ambigüedad, y cumple el comportamiento esperado. No afirma nada que contradiga la referencia. |
| `parcial` | Acierta en lo central pero le falta algún elemento clave, o agrega una imprecisión menor que no cambia la respuesta principal. Omitir pasos o elementos, sin afirmar nada falso, es `parcial`, no `incorrecta`. |
| `incorrecta` | Da un valor equivocado, omite lo central, contradice la referencia, inventa datos o no responde lo que se preguntó. |

Información adicional: si la respuesta agrega datos que no están en la referencia pero no la contradicen (por ejemplo, otra condición o una persona mencionada en los documentos), no se penaliza. Se penaliza solo lo que contradice la referencia, o lo que en una `sin_respuesta` completa el hueco con una regla, un monto o un responsable.

Reglas por tipo:

- **`dato`:** el valor tiene que ser el exacto. Un monto, plazo o responsable distinto es `incorrecta`, aunque el resto esté bien. Pasar "$ 1.500.000" a "1,5 millones de pesos" está permitido.
- **`procedimiento`:** con todos los pasos o condiciones clave, `correcta`. Si faltan uno o más pasos relevantes, sin pasos falsos, es `parcial`. Con pasos inventados o equivocados que cambian el procedimiento, `incorrecta`.
- **`cruce`:** tiene que llegar al dato final, que vive en el documento al que se remite. Si solo dice "consultar la Política X", sin el dato, es `incorrecta`. Si da el dato sin el contexto del primer documento, puede ser `correcta` siempre que el dato sea el correcto para lo que se preguntó.
- **`contradiccion_version` / `contradiccion`:** `correcta` solo si menciona **los dos valores** en conflicto, idealmente con su documento, y no presenta uno como la única verdad. Si da un solo valor, aunque sea uno de los dos, es `parcial`. Si da un valor que no es ninguno de los dos, es `incorrecta`.
- **`contradiccion_version` / `version`:** tiene que dar el valor **vigente**.
  - Si menciona el viejo aclarando que fue reemplazado, sigue siendo `correcta`.
  - Si da los dos valores sin decir cuál rige, es `parcial`.
  - Si da solo el valor viejo, es `incorrecta`.
- **`sin_respuesta`:** `correcta` si dice claramente que la información no figura en la documentación. Puede agregar lo que sí dice el corpus sobre el tema, sin completar el hueco. Si inventa un dato, un monto, un plazo o un responsable que no está en la referencia, es `incorrecta`. Si dice que no figura pero especula una respuesta como si fuera regla, es `parcial`.

## Etiqueta 2: `fuente`

Evalúa las fuentes citadas contra los documentos fuente de la pregunta.

| Valor | Cuándo |
|---|---|
| `correcta` | Cita los **documentos requeridos** (llegan en `documentos_requeridos`) según `modo_fuente`: con `al_menos_uno` (preguntas `dato` y `procedimiento`) alcanza uno; con `todos` hay que citarlos todos. En `cruce`, los requeridos son los documentos que tienen el dato final, no el que solo remite. En `contradiccion`, son los dos documentos en conflicto. En `version`, es el documento vigente. Citar además otros documentos de la lista `documentos_fuente`, o relacionados, no penaliza. |
| `parcial` | Cita algunos documentos de `documentos_fuente`, pero no los requeridos con el modo `todos`. Por ejemplo: un solo documento de una contradicción, o solo el documento viejo en una `version`. |
| `incorrecta` | No cita ningún documento de `documentos_fuente`, o no cita ninguna fuente aunque la pregunta tenía respuesta. |
| `no_aplica` | La pregunta es `sin_respuesta`. |

Un documento que no está en la lista de documentos fuente pero que también contiene el mismo dato, y que el juez puede reconocer por el contenido citado, cuenta como fuente válida en `dato` y `procedimiento`. El control en código `fuente_exacta` no puede detectar ese caso, así que ahí puede discrepar con el juez. Esas diferencias se revisan a mano.

## Formato de salida

```json
{"veredicto": "correcta|parcial|incorrecta", "fuente": "correcta|parcial|incorrecta|no_aplica", "justificacion": "1-2 oraciones"}
```

La justificación nombra qué elemento clave falta o qué valor está mal. El juez no premia el estilo ni el largo: una respuesta corta y exacta es `correcta`.

## Control sin LLM

Además del juez, `fuente_exacta` se calcula en código: compara los archivos citados con los documentos fuente. Sirve para detectar desacuerdos sistemáticos del juez en la etiqueta `fuente`.
