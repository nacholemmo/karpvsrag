# Sistema Mostrador

Sistema donde se registran y siguen los reclamos de clientes; cada reclamo recibe un número REC-. Las reglas de fondo (plazos, respuesta, resolución y quién decide) están en el procedimiento de reclamos; si el instructivo difiere, vale el procedimiento [fuente: instructivo-mostrador.md].

## Acceso y perfiles
- Se ingresa desde el escritorio o el celular (vendedores), con el mismo usuario de Tacuarí [fuente: instructivo-mostrador.md].
- Si no hay usuario o aparece "Sin permisos para este módulo", se pide el alta a Julieta Acosta, que administra Mostrador y define los perfiles [fuente: instructivo-mostrador.md].
- Perfiles:
  - Carga (Vendedores, Televentas): crear y ver los propios [fuente: instructivo-mostrador.md].
  - Gestión (Atención al Cliente): asignar, comentar, cambiar estado y cerrar [fuente: instructivo-mostrador.md].
  - Consulta (Depósito, Distribución, Calidad, Facturación): ver y comentar los de su área [fuente: instructivo-mostrador.md].
  - Administrador (Coordinadora de Atención al Cliente): todo, más usuarios y reportes [fuente: instructivo-mostrador.md].

## Bandeja
- Pantalla principal al entrar. Columnas: N° de reclamo, Cliente, sucursal, tipo, prioridad, estado, asignado a y días abiertos [fuente: instructivo-mostrador.md].
- El N° de reclamo lo asigna el sistema al guardar, empieza con REC- y es el número que se informa al cliente [fuente: instructivo-mostrador.md].

## Cargar un reclamo nuevo
Botón "+ Nuevo reclamo" (arriba a la derecha) [fuente: instructivo-mostrador.md].

- Datos del cliente [fuente: instructivo-mostrador.md]:
  - Cliente: se busca por código, razón social o CUIT. Si no aparece, no se carga a mano.
  - Sucursal: obligatoria para cuentas clave (por ejemplo, Supermercados Hermanos Lutz).
  - Contacto: nombre y teléfono de quien reclama.
- Datos de la entrega [fuente: instructivo-mostrador.md]:
  - Factura / remito: número del comprobante; revisar que sea el correcto (es el error más común).
  - Artículos reclamados y cantidad.
- Datos del reclamo [fuente: instructivo-mostrador.md]:
  - Canal de ingreso: teléfono, correo, vendedor o Televentas.
  - Tipo: faltante, mercadería vencida, mercadería dañada, falla de cadena de frío, error de preparación, otro.
  - Descripción, en palabras simples.
  - Adjuntos: fotos, remito observado, lectura de temperatura si la hay.
  - Prioridad: normal o alta.
- Regla de prioridad: los reclamos por falla de cadena de frío se cargan siempre con prioridad alta, aunque el cliente no lo pida; esto avisa a Calidad en el momento. No se baja [fuente: instructivo-mostrador.md].
- Al tocar "Guardar" el sistema muestra el número REC- asignado, que se anota o se envía al cliente en ese momento [fuente: instructivo-mostrador.md].

## Estados
- Nuevo → En análisis → Pendiente de información (si falta un dato del cliente) → Resuelto (solución definida y comunicada) → Cerrado (solución ejecutada). También puede quedar Rechazado [fuente: instructivo-mostrador.md].
- Solo los perfiles Gestión o Administrador cambian estados [fuente: instructivo-mostrador.md].

## Asignar y comentar
- Atención al Cliente usa "Asignar" para derivar el reclamo al área que responde: Depósito, Distribución, Calidad o Facturación [fuente: instructivo-mostrador.md].
- Las respuestas van en "Comentarios", nunca por mail aparte [fuente: instructivo-mostrador.md].

## Resolver y cerrar
1. Atención al Cliente define la solución según el procedimiento y la carga en el campo "Resolución" (reposición, nota de crédito, rechazo) [fuente: instructivo-mostrador.md].
2. Si corresponde nota de crédito, se pide a Facturación citando el número REC-. Mostrador no emite comprobantes [fuente: instructivo-mostrador.md]. Ver [Emisión de notas de crédito](../proceso/emision-notas-de-credito.md).
3. Se comunica al cliente y se pasa a Resuelto [fuente: instructivo-mostrador.md].
4. Cuando la reposición se entregó o la nota de crédito está emitida, se pasa a Cerrado y se completa el campo "Causa" [fuente: instructivo-mostrador.md].
- No definido en la documentación: la lista de valores posibles del campo "Causa" [fuente: instructivo-mostrador.md].

## Consultas
- Dudas sobre el uso: Tomás Vidal (Analista de Atención al Cliente) [fuente: instructivo-mostrador.md].
- Usuarios, permisos y listas: Julieta Acosta (Coordinadora de Atención al Cliente) [fuente: instructivo-mostrador.md].
- Instructivo preparado por Tomás Vidal y revisado por Julieta Acosta, fechado 20/05/2025; área: Atención al Cliente, Gerencia Comercial [fuente: instructivo-mostrador.md].

## Relacionado
- [Procedimiento de reclamos](../proceso/procedimiento-de-reclamos.md): reglas de plazos, análisis, resolución y escalamiento que se aplican en Mostrador.
- [Emisión de notas de crédito](../proceso/emision-notas-de-credito.md)
- [Sistema Tacuarí](tacuari.md)
- [Responsable de Calidad](../rol/responsable-de-calidad.md)
