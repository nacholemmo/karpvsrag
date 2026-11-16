# Emisión de una factura en Tacuarí (paso a paso)

Instructivo de Facturación (preparado por Rocío Almirón, 10/03/2025) que describe cómo emitir una factura de venta en Tacuarí a partir de un pedido ya preparado, con los pasos de cabecera, ítems, confirmación, verificación del CAE y manejo de rechazos. Las reglas de fondo están en el [Manual de Facturación](facturacion.md).

## Pasos
1. **Entrar al módulo.** Ventas > Comprobantes > Nueva factura. El punto de venta viene cargado por defecto; no se cambia [fuente: instructivo-facturacion-tacuari.md].
2. **Traer el pedido.** Escribir el número de pedido de la hoja de preparación y apretar Enter. Tacuarí trae cliente, condición de pago de la ficha, lista de precios e ítems con las cantidades **preparadas** (no las pedidas) [fuente: instructivo-facturacion-tacuari.md].
   - Leyenda verde "Pedido preparado - listo para facturar": se puede facturar [fuente: instructivo-facturacion-tacuari.md].
   - Leyenda naranja "Preparación incompleta": **no facturar**; esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md].
3. **Revisar la cabecera** (cuatro puntos) [fuente: instructivo-facturacion-tacuari.md]:
   1. Tipo de comprobante: lo pone Tacuarí según la condición frente al IVA (A o B); no se cambia a mano. Si parece mal, frenar y avisar [fuente: instructivo-facturacion-tacuari.md].
   2. Fecha: la del día; no se factura con fecha atrasada ni adelantada [fuente: instructivo-facturacion-tacuari.md].
   3. Condición de pago: debe coincidir con la ficha del cliente. Si el pedido trae otra, consultar con Créditos antes de seguir [fuente: instructivo-facturacion-tacuari.md].
   4. Mail del cliente: a ese correo se envía el PDF [fuente: instructivo-facturacion-tacuari.md].
4. **Revisar los ítems** [fuente: instructivo-facturacion-tacuari.md]:
   - Cantidad en cero por faltante de stock: la línea aparece en rojo; se deja así. Tacuarí no la factura y queda registrada como faltante [fuente: instructivo-facturacion-tacuari.md]. Coincide con el [Manual de Facturación](facturacion.md): se factura lo efectivamente preparado y el faltante se informa al vendedor [fuente: manual-facturacion.md].
   - No modificar precios ni descuentos. Si un precio parece mal, no emitir: consultar con el vendedor o con Damián [fuente: instructivo-facturacion-tacuari.md].
   - Ítem con precio "s/p": tampoco se emite [fuente: instructivo-facturacion-tacuari.md].
5. **Confirmar.** Apretar **F8**; Tacuarí pide confirmación ("¿Confirma la emisión del comprobante?"): elegir **Sí**. En ese momento el sistema envía el comprobante a ARCA para autorización. No cerrar la pantalla ni volver a apretar F8 (riesgo de duplicado) [fuente: instructivo-facturacion-tacuari.md].
6. **Verificar el CAE.** La pantalla muestra número de factura y CAE (código de autorización electrónica de ARCA). **Sin CAE la factura no es válida** [fuente: instructivo-facturacion-tacuari.md].
   - Con CAE asignado, Tacuarí envía el PDF al mail del cliente e impacta la deuda en la cuenta corriente [fuente: instructivo-facturacion-tacuari.md].
   - Imprimir con **Imprimir**; la copia en papel va con el remito [fuente: instructivo-facturacion-tacuari.md]. El Manual aclara que la copia impresa va junto al remito salvo que el cliente pida no recibir papel [fuente: manual-facturacion.md].
7. **Si el CAE viene rechazado** (recuadro rojo "Comprobante rechazado" con motivo) [fuente: instructivo-facturacion-tacuari.md]:
   1. No volver a apretar F8; leer el motivo.
   2. Capturar la pantalla o copiar el mensaje completo.
   3. Escalar a **Damián Quiroga Vela**, por mail con la captura y por teléfono si es urgente o hay varios rechazos seguidos. Él decide si se corrige y reintenta o si hay que esperar [fuente: instructivo-facturacion-tacuari.md].
   4. El comprobante queda en estado "Rechazado" en Ventas > Comprobantes > Consultar. **No borrarlo** [fuente: instructivo-facturacion-tacuari.md].
8. **Siguiente pedido.** Apretar **Esc** para cerrar el comprobante emitido y volver a Nueva factura; arrancar desde el paso 2 [fuente: instructivo-facturacion-tacuari.md].

## Errores comunes
- No aparece el pedido: la preparación no está cerrada. Esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md].
- Sale Factura B a un cliente que siempre fue A: ficha desactualizada. No emitir; avisar [fuente: instructivo-facturacion-tacuari.md]. Ver condición IVA en [Sistema Tacuarí](../sistema/tacuari.md) [fuente: manual-facturacion.md].
- F8 apretado dos veces: puede generar un comprobante duplicado. Avisar enseguida a Damián Quiroga Vela; no anular nada por cuenta propia [fuente: instructivo-facturacion-tacuari.md].
- Pantalla congelada después de F8: esperando respuesta de ARCA. Esperar; si no responde, consultar en "Consultar" antes de reintentar [fuente: instructivo-facturacion-tacuari.md].

## Huecos
- No definido en la documentación: el rol de Damián Quiroga Vela (figura como a quien escalar precios dudosos y rechazos de CAE, pero el cargo no se especifica) [fuente: instructivo-facturacion-tacuari.md].
- No definido en la documentación: plazos para reintentar un comprobante rechazado y criterios para decidir su corrección [fuente: instructivo-facturacion-tacuari.md].
- No definido en la documentación: tiempo de espera máximo de la respuesta de ARCA antes de considerar la pantalla congelada como problema [fuente: instructivo-facturacion-tacuari.md].

## Relacionado
- [Facturación: ciclo, remitos, duplicados y anulaciones](facturacion.md)
- [Sistema Tacuarí](../sistema/tacuari.md)
- [Emisión de notas de crédito (PR-FAC-03)](emision-de-notas-de-credito.md)
- [Índice](../index.md)
