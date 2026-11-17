# Facturación diaria

Cómo se origina, corta, procesa y envía la factura de cada venta, y cómo se tramitan duplicados y reenvíos. Corte diario de facturación a las 18:00 hs; facturación por lotes con control previo. Manual MAN-FAC-01, edición 03/02/2025 [fuente: manual-facturacion.md].

## Comprobantes
- Factura A: clientes responsables inscriptos. Factura B: consumidores finales, monotributistas y exentos. Ambas por venta de mercadería [fuente: manual-facturacion.md].
- La letra (A o B) depende de la condición frente al IVA cargada en la ficha del cliente. Si el cliente cambió de condición y no se avisó, o no envió la constancia, puede recibir una letra distinta a la habitual. Se corrige enviando la documentación al vendedor: con la ficha actualizada, las facturas siguientes salen bien. Las ya emitidas se corrigen con nota de crédito y refacturación, decisión que toma Facturación [fuente: faq-facturacion-clientes.md].
- Nota de crédito A/B: anulaciones, devoluciones, bonificaciones y descuentos posteriores. Nota de débito A/B: intereses y diferencias de precio a favor de la Empresa [fuente: manual-facturacion.md].
- Remito: acompaña el traslado; no es comprobante fiscal de venta [fuente: manual-facturacion.md].
- Punto de venta 0004 [fuente: manual-facturacion.md].
- Validez: la factura electrónica es válida sin firma ni sello [fuente: faq-facturacion-clientes.md].

## Pasos del ciclo diario
1. **Origen.** La factura se origina en el pedido registrado en Tacuarí por el área comercial; validado, pasa a Lapacho para su preparación [fuente: manual-facturacion.md].
2. **Corte.** Corte de facturación diaria a las **18:00 hs**. Los pedidos preparados y confirmados hasta ese horario se facturan en el día. Lo que ingresa después del corte se factura al día siguiente, en el primer lote de la jornada [fuente: manual-facturacion.md]. Un pedido de hoy que aparece facturado con fecha de mañana entró después de ese corte [fuente: faq-facturacion-clientes.md].
3. **Lotes.** La facturación se procesa por lotes según el avance de la preparación en el depósito. Cada lote se revisa con el reporte de control de Tacuarí antes de la emisión definitiva. Supervisión de lotes: Jefe de Facturación [fuente: manual-facturacion.md].
4. **Diferencias de preparación.** Si la cantidad preparada difiere de la pedida por falta de stock, se factura lo efectivamente preparado y el faltante se informa al vendedor [fuente: manual-facturacion.md].
5. **Envío.** Tacuarí envía la factura en PDF al correo de la ficha del cliente, al emitirse. Una copia impresa acompaña al remito, salvo que el cliente haya pedido no recibir papel [fuente: manual-facturacion.md] [fuente: faq-facturacion-clientes.md].

Nota: el corte de **16:00 hs** de [Armado de pedidos](armado-de-pedidos.md) es el corte de preparación en depósito; el corte de **18:00 hs** de este proceso es el de facturación. Ambos figuran en documentos distintos [fuente: manual-deposito.md] [fuente: manual-facturacion.md].

Para la operación de clic a clic (módulo, F8, verificación de CAE, rechazos), ver [Emisión de factura en Tacuarí (paso a paso)](emision-de-factura-tacuari.md) [fuente: instructivo-facturacion-tacuari.md].

## Precios
- La lista de precios vigente se carga en Tacuarí y se actualiza el primer lunes de cada mes. La Gerencia Comercial remite la lista aprobada al Sector con la anticipación necesaria [fuente: manual-facturacion.md].
- Excepción de noviembre de 2025: la actualización se carga el **segundo lunes de noviembre**, por el feriado. La semana del feriado se factura con la lista de octubre y no se carga nada antes, aunque llegue el archivo [fuente: mail-cambio-lista-precios.md]. Detalle en [Actualización de la lista de precios](actualizacion-lista-de-precios.md).
- Los vendedores y Televentas no confirman precios nuevos a clientes hasta ese lunes [fuente: mail-cambio-lista-precios.md].
- No definido en la documentación: la anticipación con la que la Gerencia Comercial debe remitir la lista aprobada [fuente: manual-facturacion.md].
- Pedidos registrados antes de la actualización se facturan con la lista vigente al momento de su registro, si se facturan dentro del ciclo habitual [fuente: manual-facturacion.md].
- Precios especiales: solo si están cargados en Tacuarí como condición especial del cliente o como descuento autorizado en el pedido. El Sector no modifica precios al facturar [fuente: manual-facturacion.md]. Ante un precio que parezca erróneo o un ítem "s/p", no emitir y consultar con el vendedor o con Damián [fuente: instructivo-facturacion-tacuari.md].
- Si el cliente dice que el precio facturado no es el que le pasó el vendedor (puede haberse usado otra lista, o faltar cargar un descuento prometido): anotar el número de factura y lo que dice el cliente, consultar con el vendedor, y no confirmar ninguna corrección hasta que se revise [fuente: faq-facturacion-clientes.md].

## Clientes institucionales
- Comedores escolares y similares: facturación quincenal. Las entregas del período se documentan con remito y se facturan en forma consolidada al cierre de cada quincena, con el detalle de los remitos incluidos [fuente: manual-facturacion.md].
- Con cada entrega reciben el remito; la factura llega después, agrupando varias entregas. Ante dudas sobre qué remitos incluye, se pide el detalle a Facturación [fuente: faq-facturacion-clientes.md].
- Su conciliación de remitos se hace igual que el resto: ver [Conciliación de remitos](conciliacion-de-remitos.md) [fuente: manual-facturacion.md].

## Duplicados y reenvíos
- **Duplicado:** copia de un comprobante ya emitido, entregada a pedido del cliente. **Reenvío:** nuevo envío electrónico del comprobante. Ninguno implica emitir un comprobante nuevo [fuente: manual-facturacion.md].
- Pueden solicitarlos: el cliente, el vendedor de la cuenta y el personal de Atención al Cliente o de Cobranzas [fuente: manual-facturacion.md].
- Canal: correo electrónico a la casilla del Sector Facturación, indicando el número completo del comprobante (punto de venta y número) o, en su defecto, la fecha aproximada y el importe. No se tramitan pedidos verbales [fuente: manual-facturacion.md] [fuente: faq-facturacion-clientes.md].
- Los duplicados los envía Rocío Almirón. Si el pedido llega antes de las 15:00, el duplicado sale ese mismo día. Si llega más tarde, se avisa al cliente que puede demorar un poco más [fuente: faq-facturacion-clientes.md].
- Entrega: preferentemente reenviando el PDF. Si se necesita copia impresa, se imprime con la leyenda "DUPLICADO" [fuente: manual-facturacion.md]. La copia impresa sale de Tacuarí con esa leyenda y va con el próximo reparto o por el vendedor [fuente: faq-facturacion-clientes.md].
- Si la dirección de correo registrada es incorrecta, se actualiza la ficha antes del reenvío, previa confirmación del vendedor o de Atención al Cliente. El Sector no envía comprobantes a otras direcciones [fuente: manual-facturacion.md].
- Factura no recibida por mail: confirmar la dirección donde el cliente la espera y compararla con la de la ficha (suele estar vieja o mal escrita). Si hay que cambiarla, pedir la confirmación al vendedor de la cuenta y avisar a Facturación antes del reenvío. Si la dirección es correcta, revisar la carpeta de correo no deseado; si no aparece, pedir el reenvío [fuente: faq-facturacion-clientes.md].
- No se envía a otro mail "por esta vez": solo a la dirección registrada en la ficha. Si el cliente la quiere en otro lugar, se actualiza la ficha [fuente: faq-facturacion-clientes.md].
- Circuito completo de duplicados: sección 5 del Manual de Facturación [fuente: faq-facturacion-clientes.md].

## Anulaciones y correcciones
- Un comprobante electrónico autorizado no se elimina ni modifica; la corrección se hace con nota de crédito o débito. Facturación no "borra" una factura mal hecha: emite nota de crédito (y, si corresponde, factura nueva) [fuente: manual-facturacion.md] [fuente: faq-facturacion-clientes.md].
- Factura emitida con error (cliente equivocado, mercadería no despachada, duplicación de pedido): anulable con nota de crédito por el total dentro de los **15 días corridos** desde su emisión [fuente: manual-facturacion.md].
- Vencido ese plazo, la corrección se trata como nota de crédito por devolución o por diferencia, con el circuito de aprobación correspondiente [fuente: manual-facturacion.md].
- Las notas de crédito por devoluciones y diferencias se rigen por PR-FAC-03 (ver [Emisión de notas de crédito](emision-notas-de-credito.md)) [fuente: manual-facturacion.md].
- Notas de débito por intereses: se generan a pedido de Créditos y Cobranzas [fuente: manual-facturacion.md].
- Diferencias entre lo facturado y lo conformado: ver [Conciliación de remitos](conciliacion-de-remitos.md) [fuente: manual-facturacion.md].
- Pedido de F8 duplicado: el instructivo indica avisar de inmediato a Damián y no anular nada por cuenta propia [fuente: instructivo-facturacion-tacuari.md].
- Reclamos de clientes por errores de facturación (cantidades, precios, productos no recibidos): no siguen el circuito general de reclamos. Se registran con todos los datos (número de comprobante, qué dice el cliente que está mal, quién lo atendió) y se derivan a Facturación, sin comprometer al cliente un plazo de respuesta. [fuente: faq-facturacion-clientes.md]. Ver [Procedimiento de reclamos](procedimiento-de-reclamos.md).
  - No definido en la documentación: el circuito aparte para reclamos por errores de facturación; "todavía no está documentado" y se está armando con Administración [fuente: faq-facturacion-clientes.md].

## Responsabilidades
| Rol | Responsabilidad |
|---|---|
| Jefe de Facturación | Responsable del proceso; supervisión de lotes; contingencias; actualización del Manual [fuente: manual-facturacion.md]; Damián Quiroga Vela, autor de la FAQ, último escalamiento de consultas [fuente: faq-facturacion-clientes.md] |
| Facturista | Emisión de comprobantes, conciliación de remitos, duplicados y reenvíos [fuente: manual-facturacion.md]; emisión paso a paso y escalamiento de rechazos [fuente: instructivo-facturacion-tacuari.md] |
| Rocío Almirón | Envío de duplicados; primera consulta por la casilla de Facturación [fuente: faq-facturacion-clientes.md]; carga de la lista de precios en Tacuarí (noviembre de 2025) [fuente: mail-cambio-lista-precios.md] |
| Comercial | Registro correcto de pedidos; envío de lista de precios; condiciones especiales [fuente: manual-facturacion.md]; aumento y archivo de la lista de noviembre de 2025 [fuente: mail-cambio-lista-precios.md] |
| Depósito y Distribución | Preparación conforme a pedido; retorno de remitos firmados [fuente: manual-facturacion.md] |
| Créditos y Cobranzas | Solicitud de notas de débito por intereses; imputación de comprobantes [fuente: manual-facturacion.md]; consultado si la condición de pago del pedido no coincide con la ficha [fuente: instructivo-facturacion-tacuari.md] |
| Vendedor de la cuenta | Confirma cambios de mail y de condición frente al IVA; recibe la documentación del cliente; consulta por precios [fuente: faq-facturacion-clientes.md] |

## Relacionado
- [Sistema Tacuarí](../sistema/tacuari.md)
- [Emisión de factura en Tacuarí (paso a paso)](emision-de-factura-tacuari.md)
- [Actualización de la lista de precios](actualizacion-lista-de-precios.md)
- [Armado de pedidos](armado-de-pedidos.md)
- [Conciliación de remitos](conciliacion-de-remitos.md)
- [Emisión de notas de crédito](emision-notas-de-credito.md)
- [Procedimiento de reclamos](procedimiento-de-reclamos.md)
- [Pedido mínimo](../politica/pedido-minimo.md)
