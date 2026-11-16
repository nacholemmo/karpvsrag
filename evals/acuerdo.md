# Acuerdo humano vs. juez (muestra de 15), versión 2

**Contexto, para leer los números con cuidado:**
- **v1** (`evals/acuerdo_v1.md`): rúbrica original. Veredicto: 11/15 (73%), kappa 0,49.
- **v2** (este archivo): se corrigieron las referencias de P01 y P22 y se ajustó la rúbrica en dos puntos (omitir sin errar es `parcial`; la información extra que no contradice no penaliza), mirando los desacuerdos de estas mismas 15. Por eso el acuerdo de v2 está algo inflado.
- El juez no es determinista: caso-11 coincidía en v1 y discrepa en v2 sin que cambiara su pregunta.
- Las etiquetas de fuente, y el veredicto de caso-07, los marcó Claude con la regla de la rúbrica, a pedido del usuario. El acuerdo de fuente no es una medición humana independiente.

Juez: claude-haiku-5-5. Casos: 15.

### Veredicto (humano vs. juez)

Acuerdo: 12/15 (80%). Kappa de Cohen: 0.58.

| humano \ juez | correcta | parcial | incorrecta |
|---|---|---|---|
| correcta | 9 | 2 | 1 |
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
| caso-09 (sint-1) | parcial | correcta | parcial |
| caso-12 (sint-3) | incorrecta | incorrecta | incorrecta |
| caso-15 (sint-2) | correcta | correcta | correcta |

### Desacuerdos de veredicto

- **caso-02** (contradiccion_version/version): humano `correcta`, juez `incorrecta`. Juez: La respuesta da solo el valor viejo de 24 horas, sin aclarar que fue reemplazado, cuando el valor vigente es 48 horas hábiles; además cita únicamente el documento de 2023 y no el documento v2 requerido. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
- **caso-09** (procedimiento): humano `correcta`, juez `parcial`. Juez: La respuesta menciona la constancia de inscripción y la habilitación bromatológica, pero omite el circuito (comprador, Calidad, Administración) y el plazo de 5 días hábiles, que son elementos clave de la referencia. No afirma nada falso, por lo que es parcial; la fuente citada es el documento requerido. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
- **caso-11** (cruce): humano `correcta`, juez `parcial`. Juez: Acierta los dos elementos clave (hasta $ 350.000 y Jefe de Facturación) y cita la circular requerida, pero no identifica como aprobador superior vigente a la Gerente de Administración y Finanzas según la referencia; además afirma que el documento no dice cuál es ese nivel y agrega un Gerente Comercial para casos de más de $ 500.000 que no figura en la referencia. Notas: fuente marcada por Claude con la regla de la rúbrica, a pedido del usuario
