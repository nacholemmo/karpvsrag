# Lapacho (sistema de gestión de almacén)

Sistema de gestión de almacén del depósito central. Desde 2024 reemplazó a las planillas en papel para registrar recepciones, ubicaciones, preparación e inventarios. Se integra con Tacuarí [fuente: manual-deposito.md]. Es la base de los inventarios generales y conteos cíclicos.

## Qué registra y controla
- Todo movimiento de mercadería, en el momento en que ocurre, con el usuario que lo realiza [fuente: manual-deposito.md].
- Recepciones: cantidades efectivamente recibidas, con lote y vencimiento [fuente: manual-deposito.md].
- Ubicaciones: toda mercadería almacenada tiene una ubicación registrada en Lapacho [fuente: manual-deposito.md].
- Bloqueo de vencidos: los productos vencidos se bloquean en Lapacho y se retiran a la zona de cuarentena [fuente: manual-deposito.md].
- Reporte de productos próximos a vencer, que revisa el supervisor de turno [fuente: manual-deposito.md].
- Mercadería no conforme: se bloquea en Lapacho y, desde ese momento, no puede ser asignada a ningún pedido [fuente: manual-deposito.md].
- Pedidos: los pedidos de Tacuarí se transfieren a Lapacho, que genera las órdenes de preparación y asigna lotes según FEFO [fuente: manual-deposito.md].
- Liberación de pedidos: el controlador de expedición libera los pedidos controlados en Lapacho, lo que habilita su facturación en Tacuarí [fuente: manual-deposito.md].
- Faltantes: genera una alerta que el supervisor revisa antes del cierre del turno [fuente: manual-deposito.md].
- Inventarios: los conteos se registran en Lapacho; los conteos cíclicos se hacen sobre las ubicaciones que indica Lapacho; los ajustes se registran con motivo y usuario [fuente: manual-deposito.md] [fuente: acta-inventario-2025.md].
- Trazabilidad por lote: junto con Tacuarí, identifica los clientes que recibieron un lote retirado [fuente: manual-deposito.md].

## Inventario de junio 2025: puntos de atención
- Las terminales de Lapacho fueron la base del inventario general del 30/06/2025 [fuente: acta-inventario-2025.md]. Ver [inventario general](../proceso/inventario-general.md).
- Hallazgo: mercadería vencida separada físicamente en Lácteos y refrigerados sin la baja registrada en Lapacho. Causa identificada: bajas no registradas [fuente: acta-inventario-2025.md].
- Acción: revisar el circuito de baja de mercadería no conforme para que el registro sea en el mismo momento de la separación [fuente: acta-inventario-2025.md].
- Acción: incorporar a los conteos cíclicos las ubicaciones de aceites y de bebidas [fuente: acta-inventario-2025.md].

## Contingencia
- Si Lapacho no está disponible, se usa la planilla de contingencia; su contenido se carga en Lapacho apenas se restablece el servicio [fuente: manual-deposito.md].
- No definido en la documentación: el formato y el procedimiento de la planilla de contingencia [fuente: manual-deposito.md].

## Relacionado
- [Operación del depósito central](../proceso/operacion-deposito.md)
- [Inventario general (resultados junio 2025)](../proceso/inventario-general.md)
- [Índice](../index.md)
