# Acuerdo humano vs. juez (muestra de 15)

Juez: claude-haiku-5-5. Casos: 15.

### Veredicto (humano vs. juez)

Acuerdo: 11/15 (73%). Kappa de Cohen: 0.49.

| humano \ juez | correcta | parcial | incorrecta |
|---|---|---|---|
| correcta | 8 | 2 | 2 |
| parcial | 0 | 1 | 0 |
| incorrecta | 0 | 0 | 2 |

### Fuente (humano vs. juez)

Acuerdo: 13/15 (87%). Kappa de Cohen: 0.79.

| humano \ juez | correcta | parcial | incorrecta | no_aplica |
|---|---|---|---|---|
| correcta | 8 | 0 | 0 | 0 |
| parcial | 0 | 1 | 2 | 0 |
| incorrecta | 0 | 0 | 1 | 0 |
| no_aplica | 0 | 0 | 0 | 3 |

### Fuente (humano vs. control en código `fuente_exacta`)

Acuerdo: 15/15 (100%). Kappa de Cohen: 1.00.

| humano \ juez | correcta | parcial | incorrecta | no_aplica |
|---|---|---|---|---|
| correcta | 8 | 0 | 0 | 0 |
| parcial | 0 | 3 | 0 | 0 |
| incorrecta | 0 | 0 | 1 | 0 |
| no_aplica | 0 | 0 | 0 | 3 |

### Respuestas sintéticas (etiqueta pretendida al escribirlas)

| caso | pretendida | humano | juez |
|---|---|---|---|
| caso-02 (sint-5) | incorrecta | correcta | incorrecta |
| caso-05 (sint-6) | parcial | parcial | parcial |
| caso-06 (sint-4) | incorrecta | incorrecta | incorrecta |
| caso-09 (sint-1) | parcial | correcta | incorrecta |
| caso-12 (sint-3) | incorrecta | incorrecta | incorrecta |
| caso-15 (sint-2) | correcta | correcta | correcta |

### Desacuerdos de veredicto

- **caso-02** (contradiccion_version/version): humano `correcta`, juez `incorrecta`. Juez: La respuesta da solo el valor viejo de 24 horas, presentándolo como vigente, cuando el valor vigente es 48 horas hábiles según el Procedimiento v2. Además cita únicamente el documento de 2023, que no es el requerido, por lo que ningún documento requerido aparece. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
- **caso-09** (procedimiento): humano `correcta`, juez `incorrecta`. Juez: Menciona la constancia de inscripción y la habilitación bromatológica, pero omite el circuito (solicitud del comprador, evaluación de Calidad, carga por Administración) y el plazo de 5 días hábiles, que son elementos clave; además presenta el alta como inmediata con esos dos documentos. Cita el documento requerido, por lo que la fuente es correcta. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
- **caso-10** (sin_respuesta): humano `correcta`, juez `parcial`. Juez: Dice correctamente que no hay responsable definido para la presentación, pero agrega que Ernesto Saldías tiene la tarea de hablarlo con Claudio Mansilla, un dato que no está en la referencia y que sugiere una asignación de responsabilidad sobre el tema que la referencia descarta. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
- **caso-13** (dato): humano `correcta`, juez `parcial`. Juez: Da el monto exacto de $ 25.000 y aclara que se suma al importe del cheque, pero luego afirma que es una decisión puntual del caso y que los documentos no fijan un monto general, lo que contradice la referencia que presenta el gasto como regla aplicable al cheque rechazado; además cita el documento requerido, por lo que la fuente es correcta. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
