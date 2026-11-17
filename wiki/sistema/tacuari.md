# Tacuarí

Sistema de gestión de la Empresa desde enero de 2025, que reemplazó a Fénix. Desde el módulo Ventas se emiten todos los comprobantes electrónicos (con autorización de ARCA, ex AFIP), y determina el tipo de comprobante según la condición frente al IVA de la ficha del cliente [fuente: manual-facturacion.md].

## Uso en facturación
- Todos los comprobantes se emiten desde Tacuarí, módulo Ventas, con autorización electrónica de ARCA (ex AFIP) [fuente: manual-facturacion.md].
- Ruta de emisión de factura: **Ventas > Comprobantes > Nueva factura**; consulta de comprobantes en **Ventas > Comprobantes > Consultar** [fuente: instructivo-facturacion-tacuari.md].
- Punto de venta vigente para la facturación electrónica: **0004**. Los puntos de venta del sistema Fénix quedan inactivos [fuente: manual-facturacion.md].
- El tipo de comprobante (Factura A/B, Nota de crédito A/B, Nota de débito A/B) lo determina Tacuarí según la condición frente al IVA de la ficha del cliente; el Sector no lo modifica manualmente [fuente: manual-facturacion.md]. Lo mismo para la factura: no se cambia a mano [fuente: instructivo-facturacion-tacuari.md].
- Sin razón social, CUIT, condición fiscal, domicilios y correo electrónico en la ficha, Tacuarí no permite la emisión [fuente: manual-facturacion.md].
- Tacuarí envía la factura en PDF al correo registrado en la ficha del cliente [fuente: manual-facturacion.md]. Con el CAE asignado, también impacta la deuda en la cuenta corriente [fuente: instructivo-facturacion-tacuari.md].
- Al traer un pedido, Tacuarí toma cliente, condición de pago, lista de precios e ítems con las cantidades preparadas [fuente: instructivo-facturacion-tacuari.md].
- Confirmación de comprobante con **F8** y ventana de confirmación; al confirmar, el comprobante se envía a ARCA [fuente: instructivo-facturacion-tacuari.md].
- Comprobante sin CAE no es válido. Si ARCA rechaza, Tacuarí muestra "Comprobante rechazado" con el motivo y el comprobante queda en estado "Rechazado" [fuente: instructivo-facturacion-tacuari.md].
- Los comprobantes electrónicos autorizados no pueden eliminarse ni modificarse; las correcciones se hacen con notas de crédito o débito, vinculadas en Tacuarí al comprobante que corrigen [fuente: manual-facturacion.md].
- Los pedidos se registran en Tacuarí por el área comercial; validados, pasan a Lapacho para su preparación [fuente: manual-facturacion.md].
- Los remitos los emite Tacuarí, vinculados al pedido y a la factura [fuente: manual-facturacion.md].
- La liberación de pedidos preparados en Lapacho habilita la facturación en Tacuarí [fuente: manual-deposito.md].

## Excepciones
- No está permitida la emisión de comprobantes manuales, salvo contingencia declarada por el Jefe de Facturación [fuente: manual-facturacion.md].
- No definido en la documentación: procedimiento de contingencia (cómo se declara, cómo se registran los comprobantes emitidos en contingencia y cómo se regularizan) [fuente: manual-facturacion.md].
- Si el comprobante no responde tras F8, el instructivo indica esperar y consultar en "Consultar" antes de reintentar; no define un procedimiento de contingencia [fuente: instructivo-facturacion-tacuari.md].

## Cambios respecto de Fénix
- Valor vigente: comprobantes y notas de crédito se emiten en Tacuarí [fuente: manual-facturacion.md]. Antes (reemplazado): comprobantes y notas de crédito se emitían en Fénix [fuente: procedimiento-notas-credito-2023.md].

## Relacionado
- [Sistema Fénix](fenix.md): sistema anterior, reemplazado por Tacuarí en enero de 2025.
- [Sistema Lapacho](lapacho.md): depósito; integración con Tacuarí.
- [Facturación diaria](../proceso/facturacion-diaria.md)
- [Emisión de factura en Tacuarí (paso a paso)](../proceso/emision-de-factura-tacuari.md)
- [Conciliación de remitos](../proceso/conciliacion-de-remitos.md)
- [Emisión de notas de crédito](../proceso/emision-notas-de-credito.md)
