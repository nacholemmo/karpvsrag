# Emisión de factura en Tacuarí (paso a paso)

Procedimiento de clic a clic para emitir una factura de venta en Tacuarí a partir de un pedido ya preparado: entrada al módulo, cabecera, ítems, confirmación con F8, verificación del CAE y manejo de rechazos. Instructivo preparado por Rocío Almirón, fecha 10/03/2025 [fuente: instructivo-facturacion-tacuari.md]. Las reglas de facturación están en el manual, ver [Facturación diaria](facturacion-diaria.md) [fuente: instructivo-facturacion-tacuari.md].

Destinatarios: facturistas, reemplazos en vacaciones y personal de Administración que colabore en el cierre [fuente: instructivo-facturacion-tacuari.md].

## Paso 1. Entrar al módulo de comprobantes
- Ruta: **Ventas > Comprobantes > Nueva factura** [fuente: instructivo-facturacion-tacuari.md].
- El punto de venta viene cargado por defecto; no se cambia [fuente: instructivo-facturacion-tacuari.md]. Punto de venta vigente: 0004 [fuente: manual-facturacion.md].

## Paso 2. Traer el pedido
- En el campo **Pedido** se escribe el número de pedido de la hoja de preparación y se apreta **Enter**. Tacuarí trae: cliente, condición de pago de la ficha, lista de precios e ítems con las cantidades **preparadas** (no las pedidas) [fuente: instructivo-facturacion-tacuari.md].
- Leyenda verde **"Pedido preparado - listo para facturar"**: se puede facturar [fuente: instructivo-facturacion-tacuari.md].
- Leyenda naranja **"Preparación incompleta"**: el depósito no cerró el pedido. No facturar; esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md]. La liberación del pedido en Lapacho es la que habilita la facturación [fuente: manual-deposito.md].

## Paso 3. Revisar la cabecera
1. **Tipo de comprobante:** lo pone Tacuarí según la condición frente al IVA del cliente (A o B). No se cambia a mano; si parece incorrecto, frenar y avisar [fuente: instructivo-facturacion-tacuari.md].
2. **Fecha:** la del día. No se factura con fecha atrasada ni adelantada [fuente: instructivo-facturacion-tacuari.md].
3. **Condición de pago:** debe coincidir con la de la ficha del cliente. Si el pedido trae otra, consultar con Créditos antes de seguir [fuente: instructivo-facturacion-tacuari.md].
4. **Mail del cliente:** a ese correo se envía el PDF [fuente: instructivo-facturacion-tacuari.md]. Sin correo en la ficha, Tacuarí no permite la emisión [fuente: manual-facturacion.md].

## Paso 4. Revisar los ítems
- Cantidad en cero por falta de stock: la línea aparece en rojo. Dejarla así; Tacuarí no la factura y queda registrada como faltante [fuente: instructivo-facturacion-tacuari.md]. Se factura lo efectivamente preparado y el faltante se informa al vendedor [fuente: manual-facturacion.md].
- No modificar precios ni descuentos. Si un precio parece mal, no emitir: consultar con el vendedor o con Damián [fuente: instructivo-facturacion-tacuari.md]. El Sector no modifica precios al facturar [fuente: manual-facturacion.md].
- Ítem sin precio (aparece "s/p"): no emitir [fuente: instructivo-facturacion-tacuari.md].

## Paso 5. Confirmar el comprobante
- Apretar **F8** para confirmar. Tacuarí pide una confirmación adicional: ventana "¿Confirma la emisión del comprobante?" con Sí / No. Elegir **Sí** [fuente: instructivo-facturacion-tacuari.md].
- En ese momento el sistema envía el comprobante a ARCA para autorización [fuente: instructivo-facturacion-tacuari.md].
- No cerrar la pantalla ni apretar F8 de nuevo: puede generarse un duplicado [fuente: instructivo-facturacion-tacuari.md].

## Paso 6. Verificar el CAE
- Si sale bien, la pantalla muestra número de factura y CAE (código de autorización electrónica de ARCA). **Sin CAE la factura no es válida** [fuente: instructivo-facturacion-tacuari.md].
- Con el CAE asignado, Tacuarí envía el PDF al mail del cliente e impacta la deuda en la cuenta corriente [fuente: instructivo-facturacion-tacuari.md].
- Para imprimir: botón **Imprimir**; la copia en papel va con el remito [fuente: instructivo-facturacion-tacuari.md].

## Paso 7. Si el CAE viene rechazado
- Aparece un recuadro rojo "Comprobante rechazado" con el motivo [fuente: instructivo-facturacion-tacuari.md].
1. No volver a apretar F8; leer primero el motivo [fuente: instructivo-facturacion-tacuari.md].
2. Capturar la pantalla o copiar el mensaje completo [fuente: instructivo-facturacion-tacuari.md].
3. Escalar a **Damián Quiroga Vela**, por mail con la captura y por teléfono si es urgente o hay varios rechazos seguidos. Él decide si se corrige y se reintenta o si hay que esperar [fuente: instructivo-facturacion-tacuari.md].
4. El comprobante queda en estado "Rechazado" en **Ventas > Comprobantes > Consultar**. No borrarlo [fuente: instructivo-facturacion-tacuari.md].

## Paso 8. Siguiente pedido
- Apretar **Esc** para cerrar el comprobante emitido; se vuelve a **Nueva factura** y se arranca desde el paso 2 [fuente: instructivo-facturacion-tacuari.md].

## Errores comunes
| Lo que pasa | Por qué | Qué hacer |
|---|---|---|
| No aparece el pedido | No está cerrada la preparación | Esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md] |
| Sale Factura B a un cliente que siempre fue A | Ficha del cliente desactualizada | No emitir, avisar [fuente: instructivo-facturacion-tacuari.md] |
| Se apretó F8 dos veces | Puede generar un comprobante duplicado | Avisar enseguida a Damián, no anular nada por cuenta propia [fuente: instructivo-facturacion-tacuari.md] |
| Pantalla congelada después de F8 | Esperando respuesta de ARCA | Esperar; si no responde, consultar en "Consultar" antes de reintentar [fuente: instructivo-facturacion-tacuari.md] |

## Huecos
- No definido en la documentación: procedimiento de contingencia para emisión (cómo se declara y cómo se regulariza) [fuente: manual-facturacion.md]. El instructivo no lo define; para el caso de pantalla congelada indica solo consultar en "Consultar" [fuente: instructivo-facturacion-tacuari.md].

## Relacionado
- [Sistema Tacuarí](../sistema/tacuari.md)
- [Facturación diaria](facturacion-diaria.md)
- [Armado de pedidos](armado-de-pedidos.md)
- [Emisión de notas de crédito](emision-notas-de-credito.md)
- [Conciliación de remitos](conciliacion-de-remitos.md)
