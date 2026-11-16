# Emisión de factura en Tacuarí (paso a paso)

Procedimiento operativo para emitir una factura de venta en Tacuarí a partir de un pedido ya preparado: entrada al módulo, controles de cabecera e ítems, confirmación con F8, verificación del CAE y tratamiento de comprobantes rechazados. Lo usan facturistas, reemplazos y personal de Administración que da una mano en el cierre [fuente: instructivo-facturacion-tacuari.md]. Las reglas de fondo están en el Manual de Facturación [fuente: instructivo-facturacion-tacuari.md], ver [Facturación y comprobantes](../politica/facturacion-y-comprobantes.md).

## Paso 1. Entrar al módulo de comprobantes
- Ruta: **Ventas > Comprobantes > Nueva factura** [fuente: instructivo-facturacion-tacuari.md].
- El punto de venta ya viene cargado por defecto; no se cambia [fuente: instructivo-facturacion-tacuari.md]. Punto de venta de facturación electrónica: 0004 [fuente: manual-facturacion.md].

## Paso 2. Traer el pedido
- En el campo **Pedido** se escribe el número de pedido que figura en la hoja de preparación y se aprieta **Enter** [fuente: instructivo-facturacion-tacuari.md].
- Tacuarí trae solo: el cliente, la condición de pago de su ficha, la lista de precios y los ítems con las cantidades **preparadas** (no las pedidas) [fuente: instructivo-facturacion-tacuari.md].
- Leyenda verde "Pedido preparado - listo para facturar": se puede facturar [fuente: instructivo-facturacion-tacuari.md].
- Leyenda naranja "Preparación incompleta": **no facturar**; el depósito todavía no cerró el pedido. Esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md].

## Paso 3. Revisar la cabecera
1. **Tipo de comprobante:** lo pone Tacuarí según la condición frente al IVA del cliente (A o B). No se cambia a mano; si parece mal, frenar y avisar [fuente: instructivo-facturacion-tacuari.md].
2. **Fecha:** la del día. No se factura con fecha atrasada ni adelantada [fuente: instructivo-facturacion-tacuari.md].
3. **Condición de pago:** debe coincidir con la de la ficha del cliente. Si el pedido trae otra, consultar con Créditos antes de seguir [fuente: instructivo-facturacion-tacuari.md]. Ver [Créditos y cobranzas](../politica/creditos-y-cobranzas.md).
4. **Mail del cliente:** a ese correo se envía el PDF [fuente: instructivo-facturacion-tacuari.md].

## Paso 4. Revisar los ítems
- Cantidad en cero por falta de stock: la línea aparece en rojo. Se deja así; Tacuarí no la factura y queda registrada como faltante [fuente: instructivo-facturacion-tacuari.md]. Coincide con facturar lo efectivamente preparado [fuente: manual-facturacion.md].
- No modificar precios ni descuentos. Si un precio parece mal, no emitir: consultar con el vendedor o con Damián Quiroga Vela [fuente: instructivo-facturacion-tacuari.md].
- Ítem sin precio (aparece "s/p"): no emitir [fuente: instructivo-facturacion-tacuari.md].

## Paso 5. Confirmar el comprobante
- Apretar **F8** para confirmar. Tacuarí pide una confirmación: "¿Confirma la emisión del comprobante?" con botones Sí / No. Elegir **Sí** [fuente: instructivo-facturacion-tacuari.md].
- En ese momento el sistema envía el comprobante a ARCA para su autorización [fuente: instructivo-facturacion-tacuari.md].
- No cerrar la pantalla ni apretar F8 de nuevo: puede generarse un duplicado [fuente: instructivo-facturacion-tacuari.md].

## Paso 6. Verificar el CAE
- Si sale bien, la pantalla muestra número de factura, CAE (código de autorización electrónica que da ARCA) y fecha de vencimiento del CAE [fuente: instructivo-facturacion-tacuari.md].
- **Sin CAE la factura no es válida** [fuente: instructivo-facturacion-tacuari.md].
- Con CAE asignado, Tacuarí envía el PDF al mail del cliente e impacta la deuda en la cuenta corriente [fuente: instructivo-facturacion-tacuari.md].
- Para imprimir: **Imprimir**. La copia en papel va con el remito [fuente: instructivo-facturacion-tacuari.md]. Excepción: si el cliente pidió no recibir papel, no se imprime [fuente: manual-facturacion.md].

## Paso 7. Si el CAE viene rechazado
- Aparece un recuadro rojo "Comprobante rechazado" con el motivo [fuente: instructivo-facturacion-tacuari.md].
1. **No volver a apretar F8.** Leer primero el motivo [fuente: instructivo-facturacion-tacuari.md].
2. Capturar la pantalla o copiar el mensaje completo [fuente: instructivo-facturacion-tacuari.md].
3. Escalar a **Damián Quiroga Vela**: por mail con la captura y por teléfono si es urgente o si hay varios rechazos seguidos. Él decide si se corrige y se reintenta, o si hay que esperar [fuente: instructivo-facturacion-tacuari.md].
4. El comprobante queda en estado "Rechazado" en **Ventas > Comprobantes > Consultar**. No borrarlo [fuente: instructivo-facturacion-tacuari.md].
- No definido en la documentación: plazo para que Damián responda ante un rechazo, y criterios para decidir entre corregir y reintentar o esperar [fuente: instructivo-facturacion-tacuari.md].

## Paso 8. Siguiente pedido
- Apretar **Esc** para cerrar el comprobante emitido; se vuelve a la pantalla vacía de Nueva factura y se arranca desde el paso 2 [fuente: instructivo-facturacion-tacuari.md].

## Errores comunes
| Lo que pasa | Por qué | Qué hacer |
|---|---|---|
| No aparece el pedido | No está cerrada la preparación | Esperar o consultar con el depósito [fuente: instructivo-facturacion-tacuari.md] |
| Sale Factura B a un cliente que siempre fue A | Ficha del cliente desactualizada | No emitir, avisar [fuente: instructivo-facturacion-tacuari.md]. Sin datos fiscales completos Tacuarí no permite emitir [fuente: manual-facturacion.md] |
| Apretó F8 dos veces | Puede generar un comprobante duplicado | Avisar enseguida a Damián, no anular nada por cuenta propia [fuente: instructivo-facturacion-tacuari.md] |
| Pantalla congelada después de F8 | Esperando respuesta de ARCA | Esperar; si no responde, consultar en "Consultar" antes de reintentar [fuente: instructivo-facturacion-tacuari.md] |

- No definido en la documentación: cuánto tiempo esperar ante una pantalla congelada después de F8 antes de considerar que no responde [fuente: instructivo-facturacion-tacuari.md].

## Relacionado
- [Facturación diaria](facturacion-diaria.md): corte de las 18:00 hs y lotes.
- [Tacuarí](../sistema/tacuari.md)
- [Emisión de notas de crédito](emision-de-notas-de-credito.md)
- [Duplicados y reenvíos](duplicados-y-reenvios.md)
- [Jefe de Facturación](../rol/jefe-de-facturacion.md)
