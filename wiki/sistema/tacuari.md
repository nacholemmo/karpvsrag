# Sistema Tacuarí

Sistema de gestión de la Empresa desde enero de 2025, que reemplazó a Fénix. Emite todos los comprobantes desde el módulo Ventas, con autorización electrónica de ARCA (ex AFIP) [fuente: manual-facturacion.md]. Cómo emitir una factura paso a paso está en [Emisión de una factura en Tacuarí](../proceso/emision-de-factura-en-tacuari.md) [fuente: instructivo-facturacion-tacuari.md]. La lista de precios se carga en este sistema; la de noviembre de 2025 se carga el segundo lunes de noviembre [fuente: mail-cambio-lista-precios.md]. Ver [Actualización de lista de precios](../proceso/actualizacion-lista-de-precios.md).

## Datos de la ficha de cliente
- Campo "Zona de reparto": se carga en el alta del cliente. Si el cliente se muda, el vendedor debe avisar para corregirla [fuente: zonas-reparto.md]. Ver [Zonas de reparto](../proceso/zonas-de-reparto.md).

## Uso en facturación
- Módulo Ventas: emisión de facturas, notas de crédito y débito, remitos [fuente: manual-facturacion.md]. Ruta de emisión de factura: Ventas > Comprobantes > Nueva factura [fuente: instructivo-facturacion-tacuari.md].
- Punto de venta de facturación electrónica: 0004 [fuente: manual-facturacion.md]. Está precargado en la pantalla de Nueva factura y no se cambia [fuente: instructivo-facturacion-tacuari.md].
- Determina el tipo de comprobante (A o B) según la condición frente al IVA de la ficha del cliente; no se cambia a mano [fuente: manual-facturacion.md] [fuente: instructivo-facturacion-tacuari.md].
- Bloquea la emisión si la ficha no tiene razón social, CUIT, condición fiscal, domicilios y correo electrónico [fuente: manual-facturacion.md].
- Al traer un pedido por número, carga cliente, condición de pago de la ficha, lista de precios e ítems con cantidades preparadas [fuente: instructivo-facturacion-tacuari.md]. Solo factura pedidos con leyenda "Pedido preparado - listo para facturar" [fuente: instructivo-facturacion-tacuari.md].
- Recibe pedidos del área comercial, que pasan a [Lapacho](lapacho.md) para preparación [fuente: manual-facturacion.md].
- Genera el reporte de control de cada lote antes de la emisión definitiva [fuente: manual-facturacion.md].
- Al confirmar (F8 y "Sí"), envía el comprobante a ARCA para autorización; con CAE asignado envía el PDF al correo de la ficha e impacta la cuenta corriente [fuente: instructivo-facturacion-tacuari.md] [fuente: manual-facturacion.md].
- Comprobantes rechazados por ARCA quedan en estado "Rechazado" en Ventas > Comprobantes > Consultar; no se borran [fuente: instructivo-facturacion-tacuari.md].
- Gestiona los reenvíos del PDF [fuente: manual-facturacion.md].
- Registra precios especiales (condición especial del cliente o descuento autorizado en el pedido) y la lista de precios vigente. Regla general: la lista se actualiza el primer lunes de cada mes [fuente: manual-facturacion.md]. Excepción de noviembre de 2025: la carga se hace el segundo lunes de noviembre, no el primero, por el feriado [fuente: mail-cambio-lista-precios.md]. Ítems sin precio ("s/p") no se emiten [fuente: instructivo-facturacion-tacuari.md].
- Vincula cada NC o ND al comprobante que corrige [fuente: manual-facturacion.md].

## Versiones
- Sistema vigente desde enero de 2025 [fuente: manual-facturacion.md].
- Antes (reemplazado): Fénix. Sus puntos de venta quedan inactivos [fuente: manual-facturacion.md].
- ⚠ Contradicción: el [procedimiento PR-FAC-03 (rev. 00, 14/06/2023)](../proceso/emision-de-notas-de-credito.md) indica emitir las NC en Fénix [fuente: procedimiento-notas-credito-2023.md]; el Manual MAN-FAC-01 indica Tacuarí para todos los comprobantes [fuente: manual-facturacion.md]. Ver detalle en [Facturación](../proceso/facturacion.md).

## No definido en la documentación
- Ver huecos de [Facturación](../proceso/facturacion.md): criterios de contingencia declarada y registros de control [fuente: manual-facturacion.md].
- Ver huecos de [Emisión de una factura en Tacuarí](../proceso/emision-de-factura-en-tacuari.md): rol de Damián Quiroga Vela, plazos para reintentar comprobantes rechazados, tiempo de espera de ARCA [fuente: instructivo-facturacion-tacuari.md].
- No definido en la documentación: el porcentaje de aumento por categoría de la lista de noviembre de 2025 [fuente: mail-cambio-lista-precios.md].

## Relacionado
- [Emisión de una factura en Tacuarí](../proceso/emision-de-factura-en-tacuari.md)
- [Facturación: ciclo, remitos, duplicados y anulaciones](../proceso/facturacion.md)
- [Actualización de lista de precios (noviembre 2025)](../proceso/actualizacion-lista-de-precios.md)
- [Zonas de reparto](../proceso/zonas-de-reparto.md)
- [Sistema Lapacho](lapacho.md)
- [Índice](../index.md)
