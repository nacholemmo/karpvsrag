# Tacuarí

Sistema de gestión que la Empresa usa desde enero de 2025 y que reemplazó al sistema Fénix. Todos los comprobantes de venta se emiten desde Tacuarí, módulo Ventas [fuente: manual-facturacion.md]. Cómo emitir una factura paso a paso está en [emisión de factura en Tacuarí](../proceso/emision-de-factura-en-tacuari.md) [fuente: instructivo-facturacion-tacuari.md].

## Uso en compras
- Todas las órdenes de compra se emiten y aprueban en el módulo de Compras de Tacuarí. No se reconocen compras hechas fuera del sistema, salvo caja chica [fuente: politica-compras.md].
- Solo se emite orden de compra a proveedores dados de alta en Tacuarí; el alta la aprueba el Jefe de Compras en la ficha del proveedor [fuente: politica-compras.md].
- Las cotizaciones se adjuntan a la orden de compra en Tacuarí [fuente: politica-compras.md].
- Antes (reemplazado): las órdenes de compra se cargaban en [Fénix](fenix.md) [fuente: manual-compras-2023.md].
- Ver [política de compras](../politica/compras.md) y [circuito de una compra](../proceso/circuito-de-compras.md).

## Uso en facturación
- Contexto: a partir de enero de 2025 la Empresa opera con Tacuarí, que reemplazó al anterior sistema Fénix [fuente: manual-facturacion.md].
- Ruta para emitir una factura: **Ventas > Comprobantes > Nueva factura**; consultas en **Ventas > Comprobantes > Consultar** [fuente: instructivo-facturacion-tacuari.md].
- Todos los comprobantes se emiten desde Tacuarí, módulo Ventas, con autorización electrónica de ARCA (ex AFIP) [fuente: manual-facturacion.md]. Al confirmar con F8 se envía el comprobante a ARCA [fuente: instructivo-facturacion-tacuari.md].
- Punto de venta de facturación electrónica: **0004**. Los puntos de venta del sistema Fénix quedan inactivos [fuente: manual-facturacion.md]. El punto de venta viene cargado por defecto en Nueva factura y no se cambia [fuente: instructivo-facturacion-tacuari.md].
- Tacuarí determina el tipo de comprobante según la condición frente al IVA registrada en la ficha del cliente. El Sector no modifica manualmente el tipo de comprobante [fuente: manual-facturacion.md] [fuente: instructivo-facturacion-tacuari.md].
- Sin razón social, CUIT, condición fiscal, domicilios y correo electrónico en la ficha, Tacuarí no permite la emisión [fuente: manual-facturacion.md].
- Al traer un pedido, Tacuarí carga cliente, condición de pago de la ficha, lista de precios e ítems con cantidades preparadas [fuente: instructivo-facturacion-tacuari.md]. Leyenda "Preparación incompleta" en naranja: el pedido no se factura [fuente: instructivo-facturacion-tacuari.md].
- Con CAE asignado, Tacuarí envía la factura en PDF al correo registrado en la ficha del cliente e impacta la deuda en la cuenta corriente [fuente: manual-facturacion.md] [fuente: instructivo-facturacion-tacuari.md].
- Comprobante sin CAE no es válido. Un comprobante rechazado por ARCA queda en estado "Rechazado" en Consultar y no se borra; se escala a Damián Quiroga Vela [fuente: instructivo-facturacion-tacuari.md].
- El pedido se registra en Tacuarí por el área comercial; validado, pasa a Lapacho para su preparación [fuente: manual-facturacion.md].
- Cada remito se emite desde Tacuarí, vinculado al pedido y a la factura [fuente: manual-facturacion.md].
- Las notas de crédito y débito se vinculan en Tacuarí al comprobante que corrige [fuente: manual-facturacion.md].
- La lista de precios vigente se carga en Tacuarí [fuente: manual-facturacion.md].
- Los precios especiales deben estar cargados en Tacuarí como condición especial del cliente o como descuento autorizado en el pedido [fuente: manual-facturacion.md].
- Los reclamos y solicitudes de duplicado se canalizan por correo, no por Tacuarí [fuente: manual-facturacion.md].

## Vigencia de la operatoria
- Fénix queda reemplazado para la emisión de comprobantes desde enero de 2025 [fuente: manual-facturacion.md]. Ver [sistema Fénix](fenix.md).
- ⚠ Sobre la emisión de notas de crédito, ver la contradicción en [emisión de notas de crédito](../proceso/emision-de-notas-de-credito.md).

## Relacionado
- [Emisión de factura en Tacuarí (paso a paso)](../proceso/emision-de-factura-en-tacuari.md)
- [Facturación diaria](../proceso/facturacion-diaria.md)
- [Conciliación de remitos](../proceso/conciliacion-de-remitos.md)
- [Duplicados y reenvíos](../proceso/duplicados-y-reenvios.md)
- [Facturación y comprobantes](../politica/facturacion-y-comprobantes.md)
- [Política de compras](../politica/compras.md)
- [Sistema Fénix](fenix.md)
