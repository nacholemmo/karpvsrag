# Lapacho (sistema de gestión de almacén)

Sistema de gestión de almacén del depósito central. Desde 2024 reemplazó a las planillas en papel para registrar recepciones, ubicaciones, preparación e inventarios. Según el Manual de Depósito de 2025, es el registro de todo movimiento de mercadería [fuente: manual-deposito.md].

## Usos según el Manual de Depósito 2025
- Todo movimiento de mercadería se registra en Lapacho en el momento en que ocurre, con el usuario de quien lo realiza [fuente: manual-deposito.md].
- Las planillas en papel solo se usan si el sistema cae; su contenido se carga en Lapacho apenas se restablece el servicio [fuente: manual-deposito.md].
- Recepción registra en Lapacho las cantidades efectivamente recibidas, con lote y vencimiento [fuente: manual-deposito.md]. Ver [Recepción de mercadería](../proceso/recepcion-de-mercaderia.md).
- Toda la mercadería almacenada tiene una ubicación registrada en Lapacho [fuente: manual-deposito.md].
- Lapacho asigna la mercadería a cada pedido según la fecha de vencimiento de los lotes disponibles (FEFO) [fuente: manual-deposito.md].
- Lapacho genera las órdenes de preparación a partir de los pedidos transferidos desde Tacuarí [fuente: manual-deposito.md]. Ver [Armado de pedidos](../proceso/armado-de-pedidos.md).
- Lapacho emite un reporte de productos próximos a vencer, que revisa el supervisor de turno; los productos vencidos se bloquean en Lapacho [fuente: manual-deposito.md].
- Las faltantes generan una alerta en Lapacho que el supervisor revisa antes del cierre del turno [fuente: manual-deposito.md].
- La liberación de un pedido controlado en Lapacho habilita su facturación en Tacuarí [fuente: manual-deposito.md].
- Los productos de no conformidad se bloquean en Lapacho y no pueden ser asignados a pedidos [fuente: manual-deposito.md]. Ver [Política de calidad e inocuidad](../politica/calidad-e-inocuidad.md).
- Los conteos de inventario general y cíclico se registran en Lapacho; los ajustes se registran con motivo y usuario [fuente: manual-deposito.md].
- Ante un retiro de lote, el Jefe de Depósito lo bloquea de inmediato en Lapacho [fuente: manual-deposito.md].

## Inventario general de junio de 2025
- El inventario general del 30/06/2025 se hizo con las terminales de Lapacho y el stock teórico de Tacuarí [fuente: acta-inventario-2025.md].
- Los ajustes se registraron en Lapacho con el motivo y el usuario responsable de cada uno [fuente: acta-inventario-2025.md].
- Hallazgo: mercadería vencida separada en el sector de no conforme sin la baja registrada en Lapacho (lácteos y refrigerados) [fuente: acta-inventario-2025.md]. Ver [Inventario general](../proceso/inventario-general.md).
- Acción: incorporar a los conteos cíclicos las ubicaciones de aceites y de bebidas [fuente: acta-inventario-2025.md].
- Acción: revisar el circuito de baja de mercadería no conforme para que el registro sea en el mismo momento de la separación [fuente: acta-inventario-2025.md].

## Relación con Tacuarí
- Tacuarí es el sistema de gestión de la Empresa y se integra con Lapacho. Los pedidos de Tacuarí se transfieren a Lapacho [fuente: manual-deposito.md].
- No definido en la documentación: el detalle de la integración entre Lapacho y Tacuarí (frecuencia, datos transferidos y forma de la transferencia) [fuente: manual-deposito.md].

## Relación con Fénix
- Hasta la edición 2025 del manual, el registro oficial de stock estaba en Fénix [fuente: manual-deposito-2023.md]. Valor vigente: el registro de movimientos y stock del depósito se hace en Lapacho [fuente: manual-deposito.md]. Ver [Fénix](fenix.md).

## Relacionado
- [Fénix](fenix.md)
- [Tacuarí](tacuari.md)
- [Inventario general](../proceso/inventario-general.md)
- [Recepción de mercadería](../proceso/recepcion-de-mercaderia.md)
- [Armado de pedidos](../proceso/armado-de-pedidos.md)
- [Política de calidad e inocuidad](../politica/calidad-e-inocuidad.md)
