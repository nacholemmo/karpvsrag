# Lapacho

Sistema de gestión de almacén del depósito, implementado durante 2024. Registra recepciones, ubicaciones, preparación e inventarios, y se integra con Tacuarí. Según el Manual de Depósito de 13/01/2025, reemplazó a las planillas en papel para la registración. En el inventario general de 30/06/2025 se usaron sus terminales y los ajustes se registraron en él.

## Usos
- Registro de cada movimiento de mercadería en el momento en que ocurre, con el usuario que lo realiza [fuente: manual-deposito.md]
- Recepción: revisión de órdenes de compra abiertas y programación de entregas; confirmación de la recepción con asignación de ubicación sugerida; registro de rechazos y de faltantes [fuente: instructivo-recepcion-mercaderia.md]
- Registro de cantidades recibidas, con lote y vencimiento [fuente: manual-deposito.md]
- Toda mercadería almacenada tiene una ubicación registrada en Lapacho [fuente: manual-deposito.md]
- Asignación de lotes por vencimiento (FEFO) y órdenes de preparación generadas desde pedidos de Tacuarí [fuente: manual-deposito.md]
- Reporte de productos próximos a vencer, revisado por el supervisor de turno [fuente: manual-deposito.md]
- Bloqueo de vencidos, de lotes con mercadería no conforme y de lotes retirados por alerta sanitaria [fuente: manual-deposito.md]
- Liberación de pedidos controlados, que habilita su facturación en Tacuarí [fuente: manual-deposito.md]
- Alerta de faltantes de preparación que el supervisor revisa antes del cierre del turno [fuente: manual-deposito.md]
- Conteos e inventarios, con ajustes y motivo [fuente: manual-deposito.md]

## Inventario y ajustes (junio 2025)
- El inventario general del 30/06/2025 se hizo con las terminales de Lapacho [fuente: acta-inventario-2025.md]
- Los ajustes del inventario se registraron en Lapacho con el motivo y el usuario responsable de cada uno [fuente: acta-inventario-2025.md]
- Se detectó mercadería vencida o dañada separada físicamente pero sin baja registrada en Lapacho [fuente: acta-inventario-2025.md]. Ver [Roturas y vencidos](../proceso/roturas-y-vencidos.md)

## Contingencia
- Si Lapacho no está disponible, se usa la planilla de contingencia y su contenido se carga en Lapacho al restablecerse el servicio [fuente: manual-deposito.md]
- No definido en la documentación: el formato de la planilla de contingencia [fuente: manual-deposito.md]

## Relacionado
- [Manual de Depósito y Operaciones de Almacén](../politica/manual-de-deposito.md)
- [Recepción de mercadería](../proceso/recepcion-de-mercaderia.md)
- [Almacenamiento en depósito](../proceso/almacenamiento-en-deposito.md)
- [Armado de pedidos](../proceso/armado-de-pedidos.md)
- [Inventarios](../proceso/inventarios.md)
- [Roturas y vencidos](../proceso/roturas-y-vencidos.md)
- [Sistema Tacuarí](tacuari.md)
- [Sistema Fénix](fenix.md)
