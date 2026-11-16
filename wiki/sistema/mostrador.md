# Sistema Mostrador

Sistema donde se registran y siguen los reclamos de clientes; cada reclamo recibe un número REC- que se informa al cliente. Este resumen cubre el uso del sistema; las reglas de fondo (plazos, resolución, escalamiento) están en el [procedimiento de reclamos](../proceso/procedimiento-de-reclamos.md).

## Acceso y perfiles
- Se ingresa desde el escritorio o el celular (vendedores) con el mismo usuario de Tacuarí [fuente: instructivo-mostrador.md].
- Sin usuario o con el mensaje "Sin permisos para este módulo": pedir el alta a Julieta Acosta, que administra Mostrador y define los perfiles [fuente: instructivo-mostrador.md].
- Perfil Carga (Vendedores, Televentas): crear y ver los propios [fuente: instructivo-mostrador.md].
- Perfil Gestión (Atención al Cliente): asignar, comentar, cambiar estado y cerrar [fuente: instructivo-mostrador.md].
- Perfil Consulta (Depósito, Distribución, Calidad, Facturación): ver y comentar los de su área [fuente: instructivo-mostrador.md].
- Perfil Administrador (Coordinadora de Atención al Cliente): todo, más usuarios y reportes [fuente: instructivo-mostrador.md].

## Bandeja (pantalla principal)
- Al entrar se ve la Bandeja [fuente: instructivo-mostrador.md].
- Columnas: N° de reclamo, Cliente, sucursal, tipo, prioridad, estado, asignado a y días abiertos [fuente: instructivo-mostrador.md].
- El N° de reclamo lo asigna el sistema al guardar, empieza con REC- y sigue la numeración correlativa [fuente: instructivo-mostrador.md].

## Cargar un reclamo nuevo
Botón "+ Nuevo reclamo" (arriba a la derecha) [fuente: instructivo-mostrador.md].

Campos:
- Cliente: se busca por código, razón social o CUIT. Si no aparece, no se carga a mano [fuente: instructivo-mostrador.md].
- Sucursal: obligatoria para cuentas clave (por ejemplo, Supermercados Hermanos Lutz) [fuente: instructivo-mostrador.md].
- Contacto: nombre y teléfono de quien reclama [fuente: instructivo-mostrador.md].
- Factura / remito: número del comprobante; revisar que sea el correcto, es el error más común [fuente: instructivo-mostrador.md].
- Artículos reclamados y cantidad [fuente: instructivo-mostrador.md].
- Canal de ingreso: teléfono, correo, vendedor o Televentas [fuente: instructivo-mostrador.md].
- Tipo: faltante, mercadería vencida, mercadería dañada, falla de cadena de frío, error de preparación, otro [fuente: instructivo-mostrador.md].
- Descripción: qué pasó, en palabras simples [fuente: instructivo-mostrador.md].
- Adjuntos: fotos, remito observado, lectura de temperatura si la hay [fuente: instructivo-mostrador.md].
- Prioridad: normal o alta [fuente: instructivo-mostrador.md].

**Regla de prioridad:** los reclamos por falla de cadena de frío se cargan siempre con prioridad alta, aunque el cliente no lo pida; avisa a Calidad en el momento. No se baja [fuente: instructivo-mostrador.md].

Al tocar "Guardar" el sistema muestra el número REC- asignado; anotarlo o comunicarlo al cliente en ese momento [fuente: instructivo-mostrador.md].

## Estados
- Nuevo → En análisis → Pendiente de información (si falta un dato del cliente) → Resuelto (solución definida y comunicada) → Cerrado (solución ejecutada) [fuente: instructivo-mostrador.md].
- También puede quedar Rechazado [fuente: instructivo-mostrador.md].
- Solo el perfil Gestión o Administrador cambia estados [fuente: instructivo-mostrador.md].

## Asignar y comentar
- Atención al Cliente usa "Asignar" para derivar el reclamo al área que responde: Depósito, Distribución, Calidad o Facturación [fuente: instructivo-mostrador.md].
- Las respuestas van en "Comentarios", nunca por mail aparte [fuente: instructivo-mostrador.md].

## Resolver y cerrar
1. Con la información de las áreas, Atención al Cliente define la solución según el procedimiento y la carga en el campo "Resolución" (reposición, nota de crédito, rechazo) [fuente: instructivo-mostrador.md].
2. Si corresponde nota de crédito, se pide a Facturación citando el número REC-. Mostrador no emite comprobantes [fuente: instructivo-mostrador.md]. Circuito de NC: ver [emisión de notas de crédito](../proceso/emision-de-notas-de-credito.md).
3. Se comunica al cliente y se pasa a Resuelto [fuente: instructivo-mostrador.md].
4. Cuando la reposición se entregó o la nota de crédito está emitida, se pasa a Cerrado y se completa el campo "Causa" [fuente: instructivo-mostrador.md].

## Relación con el procedimiento
- Si hay diferencias entre el instructivo de Mostrador y el Procedimiento de Reclamos de Clientes (v2), vale el procedimiento [fuente: instructivo-mostrador.md].
- Plazos para reclamar, de respuesta y de resolución, y quién decide reposición o nota de crédito: ver [procedimiento de reclamos](../proceso/procedimiento-de-reclamos.md) [fuente: instructivo-mostrador.md].

## Responsables
- Dudas sobre el uso: Tomás Vidal, Analista de Atención al Cliente [fuente: instructivo-mostrador.md].
- Usuarios, permisos y listas: Julieta Acosta, Coordinadora de Atención al Cliente [fuente: instructivo-mostrador.md].
- Documento preparado por Tomás Vidal y revisado por Julieta Acosta, fecha 20/05/2025 [fuente: instructivo-mostrador.md].

## Huecos y puntos no definidos
- No definido en la documentación: qué hacer cuando el cliente no aparece en la búsqueda, dado que el instructivo indica no cargarlo a mano [fuente: instructivo-mostrador.md].
- No definido en la documentación: qué hacer con los reclamos por errores de facturación en Mostrador (el procedimiento los tramita por un circuito aparte) [fuente: instructivo-mostrador.md] [fuente: procedimiento-reclamos-v2.md].

## Relacionado
- [Procedimiento de reclamos de clientes](../proceso/procedimiento-de-reclamos.md): reglas de fondo, plazos y escalamiento a Gerencia Comercial.
- [Emisión de notas de crédito a clientes](../proceso/emision-de-notas-de-credito.md): NC con número REC- de Mostrador.
- [Sistema Tacuarí](tacuari.md): mismo usuario de acceso.
- [Responsable de Calidad](../rol/responsable-de-calidad.md): recibe avisos de reclamos por cadena de frío.
- [Índice](../index.md)
