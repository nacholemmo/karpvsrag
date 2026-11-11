# ESTADO

**Fase actual:** 1 (Corpus) cerrada. Falta el OK del usuario para empezar la fase 2 (Evals).

## Hecho (fase 1)
- Andamiaje del repo: git, `.gitignore`, `.env.example`, licencia MIT, Python 3.12 y `requirements.txt` pinneado.
- Diseño en `diseno/`:
  - `empresa.md`: biblia de Distribuidora Quebracho Azul S.A.;
  - `catalogo.csv`: los 50 documentos;
  - `huecos.csv`: 8 huecos.
- **Corpus:** 50 documentos en `corpus/`, escritos en 5 tandas de 10 por subagentes. Suman unas 52.000 palabras, ~78,5k tokens estimados (chars/4; la medición exacta queda para la fase 2 con `count_tokens`).
- **`hechos.csv`:** 225 hechos, con 5 contradicciones (C1-C5), 15 procesos con versión vieja y nueva (V1-V15) y 18 cruces (X1-X18). De H213 en adelante son agregados posteriores al diseño.
- **Validador:** `scripts/validar_hechos.py` da OK, con 225/225 hechos y un solo aviso esperado (C4 cita la Política de Calidad por las temperaturas). Tiene 15 tests, que pasan.
- **Revisión independiente** con un subagente. Se corrigieron:
  - C2, que era en realidad una versión;
  - matices en C1 y C4 que indicaban qué documento prevalecía;
  - dos contradicciones accidentales (donación, desbloqueo);
  - el hueco H6, que quedaba parcialmente respondido;
  - hechos superados sin marcar (ahora V13-V15);
  - marcas reales (WhatsApp, Excel) y un apellido que coincidía con una empresa real de alimentos (Ledesma, cambiado a Lescano).

  Una segunda verificación independiente confirmó las correcciones. Lo último que marcó (punto 7.7 del Manual de Depósito y un KeyError del validador) también quedó corregido.

## Pendiente / notas para la fase 2
- Medir los tokens reales del corpus con la API, cuando haya clave.
- Las preguntas de "contradicción o versión" salen de los grupos C y V. Las de "sin respuesta" salen de `diseno/huecos.csv` (respetar `que_no_dice`).
- Detalle menor conocido: en C2 la minuta hace "mandar" al remito escaneado, lo que podría leerse como otro punto de partida del plazo. No se consideró bloqueante.

## Próximos pasos
Plan de la fase 2 (50 preguntas, juez con rúbrica, muestra de 15 para revisión manual). Antes de implementarlo, esperar la aprobación del usuario.
