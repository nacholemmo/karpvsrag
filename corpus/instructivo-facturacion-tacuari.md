# Instructivo: cómo emitir una factura en Tacuarí

**Sector:** Facturación
**Preparó:** Rocío Almirón
**Fecha:** 10/03/2025
**Para quién es:** facturistas, reemplazos en vacaciones y cualquiera de Administración que tenga que dar una mano en el cierre.

Este instructivo cuenta, paso a paso y con lo que se ve en pantalla, cómo se emite una factura de venta en Tacuarí a partir de un pedido ya preparado. No explica las reglas de facturación (qué tipo de comprobante corresponde, horarios de corte, conciliación de remitos): para eso está el Manual de Facturación. Acá es solo el "dónde hago clic".

Antes de arrancar, tené a mano tu usuario y contraseña de Tacuarí con perfil de Facturación. Si al entrar no ves el menú **Ventas**, tu usuario no tiene el permiso: pedíselo a Damián.

---

## Paso 1. Entrar al módulo de comprobantes

Desde la pantalla principal, andá a **Ventas > Comprobantes > Nueva factura**.

[captura: menú superior de Tacuarí con "Ventas" desplegado y la opción "Nueva factura" resaltada]

Se abre la pantalla de carga del comprobante, con la cabecera arriba y la grilla de ítems abajo. El punto de venta ya viene cargado por defecto; no lo cambies.

[captura: pantalla de comprobantes vacía, con los campos Cliente, Fecha, Pedido y Condición de pago]

## Paso 2. Traer el pedido

En el campo **Pedido**, escribí el número de pedido que figura en la hoja de preparación y apretá **Enter**. Tacuarí trae solo:

- el cliente,
- la condición de pago de su ficha,
- la lista de precios,
- los ítems con las cantidades **preparadas** (no las pedidas).

[captura: cabecera completa con los datos del cliente y la leyenda "Pedido preparado - listo para facturar" en verde]

Si en lugar de la leyenda verde aparece una en naranja que dice "Preparación incompleta", el depósito todavía no cerró el pedido. No factures: esperá o consultá con el depósito.

> **Tip:** también podés buscar el pedido por cliente. Dejá el campo Pedido vacío, poné el cursor en **Cliente** y empezá a escribir la razón social. Te aparece la lista de pedidos pendientes de ese cliente; elegí con las flechas y **Enter**.

## Paso 3. Revisar la cabecera

Antes de tocar nada en los ítems, mirá:

1. **Tipo de comprobante.** Lo pone Tacuarí según la condición frente al IVA del cliente (A o B). No se cambia a mano. Si te parece que está mal, frená y avisá: lo que hay que corregir es la ficha del cliente, no la factura.
2. **Fecha.** Es la del día. No se factura con fecha atrasada ni adelantada.
3. **Condición de pago.** Tiene que coincidir con la que el cliente tiene en su ficha. Si el pedido trae otra, consultá con Créditos antes de seguir.
4. **Mail del cliente.** Aparece en gris debajo de la razón social. A ese mail se va a mandar el PDF. Si ves algo raro (un mail incompleto, uno que dice "sin mail"), anotalo y avisá a Atención al Cliente después de emitir.

[captura: zoom de la cabecera con los cuatro puntos marcados con números]

## Paso 4. Revisar los ítems

En la grilla de abajo vas a ver cada producto con código, descripción, cantidad, precio unitario, descuento e importe. Movete con **Tab** entre columnas.

- Si una cantidad está en cero porque faltó stock, la línea aparece en rojo. Dejala así: Tacuarí no la factura y queda registrada como faltante.
- No modifiques precios ni descuentos. Si un precio te parece mal, no emitas: consultá con el vendedor o con Damián.
- Si un ítem no tiene precio (aparece "s/p"), tampoco emitas. Es casi siempre un producto nuevo que todavía no está en la lista.

[captura: grilla de ítems con una línea en rojo por faltante y el total al pie]

Al pie de la grilla vas a ver el subtotal, los impuestos discriminados (si es A) y el total.

## Paso 5. Confirmar el comprobante

Cuando todo está bien, apretá **F8** para confirmar. Tacuarí te pide una confirmación más:

[captura: ventana emergente "¿Confirma la emisión del comprobante?" con botones Sí / No]

Elegí **Sí**. En ese momento el sistema envía el comprobante a ARCA para que lo autorice. Tarda unos segundos; no cierres la pantalla ni apretes **F8** de nuevo, porque podés generar un duplicado.

## Paso 6. Verificar el CAE

Si todo salió bien, la pantalla muestra el número de factura y el CAE, que es el código de autorización electrónica que da ARCA. Sin CAE la factura no es válida.

[captura: pantalla de comprobante emitido, con número de factura, CAE y fecha de vencimiento del CAE en un recuadro verde]

Con el CAE asignado, Tacuarí hace solo tres cosas:

- manda el PDF al mail del cliente,
- deja la factura lista para imprimir junto con el remito,
- impacta la deuda en la cuenta corriente del cliente.

Para imprimir, apretá el botón **Imprimir** o andá a **Ventas > Comprobantes > Consultar**, buscá la factura y elegí **Reimprimir**. La copia en papel va con el remito, salvo que el cliente haya pedido no recibir papel (en ese caso la ficha lo dice y el botón Imprimir aparece deshabilitado).

## Paso 7. Si el CAE viene rechazado

A veces ARCA no autoriza el comprobante. En la pantalla aparece un recuadro rojo con la leyenda "Comprobante rechazado" y un mensaje con el motivo.

[captura: recuadro rojo de rechazo con el código de error y la descripción]

Qué hacer:

1. **No vuelvas a apretar F8.** Primero leé el motivo.
2. Sacá una captura de la pantalla o copiá el mensaje completo.
3. Si el motivo es claro y es un dato del cliente (por ejemplo, un CUIT mal cargado), no lo corrijas vos en la ficha: avisá.
4. Escalalo a Damián Quiroga Vela, por mail con la captura y por teléfono si es urgente o si hay varios rechazos seguidos. Él decide si se corrige y se reintenta, o si hay que esperar.
5. El comprobante rechazado queda en estado "Rechazado" en **Ventas > Comprobantes > Consultar**. No lo borres.

Si los rechazos son de todos los comprobantes y no de uno solo, probablemente el problema sea del servicio de ARCA o de la conexión. Igual se avisa a Damián, que es quien define cómo seguimos.

## Paso 8. Siguiente pedido

Apretá **Esc** para cerrar el comprobante emitido. Volvés a la pantalla vacía de **Nueva factura** y arrancás de nuevo desde el paso 2.

---

## Errores comunes

| Lo que pasa | Por qué | Qué hacer |
|---|---|---|
| No aparece el pedido | No está cerrada la preparación | Esperar o consultar con el depósito |
| Sale Factura B a un cliente que siempre fue A | Ficha del cliente desactualizada | No emitir, avisar |
| Apreté F8 dos veces | Puede generar un comprobante duplicado | Avisar enseguida a Damián, no anular nada por tu cuenta |
| El PDF no le llegó al cliente | Mail mal cargado en la ficha | Pedir reenvío según el Manual de Facturación |
| Pantalla congelada después de F8 | Esperando respuesta de ARCA | Esperar; si no responde, consultar en "Consultar" antes de reintentar |

Cualquier duda que no esté acá, preguntame a mí o a Damián. Este instructivo lo vamos a ir actualizando a medida que nos acostumbremos al sistema nuevo.
