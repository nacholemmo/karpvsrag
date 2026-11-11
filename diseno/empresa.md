# Biblia de la empresa ficticia

> Documento de diseño. **No forma parte del corpus** y ningún brazo lo lee.
> Todo es inventado: la empresa, las personas, los proveedores, los clientes y los sistemas.
> Cualquier dato fijo que necesite un documento del corpus tiene que salir de acá o de `hechos.csv`.

## Empresa

- **Razón social:** Distribuidora Quebracho Azul S.A. Internamente se la llama "Quebracho" o "QA".
- **CUIT:** 30-71999999-0. Es ficticio y su dígito verificador es inválido a propósito.
- **Rubro:** distribución mayorista de alimentos y bebidas.
- **Ubicación:** la sede administrativa y el depósito central están en el mismo predio, en Calle 14 N° 2210, Parque Industrial Sur, en el Gran Rosario (provincia de Santa Fe).
- **Clientes:** unos 1.800 activos en el sur de Santa Fe.
- **Moneda:** pesos argentinos. Los montos se escriben `$ 1.500.000`, con espacio después del signo y punto de miles.
- **Fechas:** formato dd/mm/aaaa.

## Sistemas internos (nombres inventados)

| Sistema | Uso | Desde |
|---|---|---|
| **Tacuarí** | ERP: ventas, facturación electrónica, cuentas corrientes, compras | enero 2025 |
| **Fénix** | ERP anterior, hoy apagado. Lo mencionan los documentos viejos | hasta diciembre 2024 |
| **Lapacho** | WMS del depósito: recepción, ubicaciones, picking, inventario | 2024 |
| **Mostrador** | Mesa de reclamos de clientes. Los números tienen la forma `REC-` | enero 2025 |

## Áreas y personas (todas ficticias)

| Nombre | Puesto | Área | Notas |
|---|---|---|---|
| Horacio Benítez Lagos | Gerente General | Dirección | |
| Silvina Arrúa | Gerente de Administración y Finanzas | Administración | |
| Marta Ifrán | Jefa de Créditos y Cobranzas | Administración | Es la "Marta" de los mails |
| Paula Gorosito | Analista de Créditos | Administración | |
| Lucas Ferreyra Doce | Analista de Cobranzas | Administración | |
| Damián Quiroga Vela | Jefe de Facturación | Administración | |
| Rocío Almirón | Facturista | Administración | |
| Claudio Mansilla | Gerente de Operaciones | Operaciones | Depósito, Compras, Calidad y Distribución dependen de él |
| Ernesto Saldías | Jefe de Compras | Operaciones | |
| Florencia Lescano | Compradora (almacén seco) | Operaciones | |
| Iván Zárate | Comprador (frescos y refrigerados) | Operaciones | |
| Rubén Kowalczyk | Jefe de Depósito | Operaciones | Le dicen "el Ruso" |
| Matías Guiñazú | Supervisor de turno noche | Operaciones | |
| Gabriel Ocampo | Encargado de Recepción | Operaciones | |
| Natalia Peralta Ruiz | Responsable de Calidad | Operaciones | Desde 2024 reporta a Operaciones |
| Walter Insaurralde | Jefe de Distribución | Operaciones | Flota propia y fleteros |
| Verónica Etchart | Gerente Comercial | Comercial | |
| Sergio Bazán | Jefe de Ventas (canal tradicional) | Comercial | |
| Lorena Castagnino | Jefa de Cuentas Clave | Comercial | |
| Nicolás Pereyra | Vendedor | Comercial | |
| Agustina Romero | Vendedora | Comercial | |
| Mariela Sosa | Televentas | Comercial | |
| Julieta Acosta | Coordinadora de Atención al Cliente | Comercial | Lleva Mostrador |
| Tomás Vidal | Analista de Atención al Cliente | Comercial | |
| Graciela Toledo | Jefa de Recursos Humanos | RRHH | |
| Ezequiel Moyano | Analista de RRHH | RRHH | |

Liquidación de sueldos tercerizada: **Estudio Alonso & Ríos** (estudio contable ficticio).

## Productos

Almacén seco (harinas, aceites, conservas, fideos, yerba), lácteos y refrigerados, congelados, fiambres y bebidas.

## Proveedores ficticios

- Lácteos La Tranquera Norte (le dicen "la Tranquera")
- Molinos Santa Clotilde
- Conservas del Paraná Medio
- Frigorífico Los Aromos
- Bebidas Cumbre Alta

## Clientes ficticios y tipos de cliente

- **Tipos:** almacenes de barrio, autoservicios, supermercados regionales chicos, gastronómicos (restaurantes, bares, rotiserías) e institucionales (comedores).
- **Supermercados Hermanos Lutz:** cuenta clave, con 6 sucursales.
- **Autoservicio Don Beto:** canal tradicional.
- **Parrilla El Fogón de Tito:** cliente gastronómico.
- **Comedor Escolar N° 14:** cliente institucional.

## Línea de tiempo

| Fecha | Hito |
|---|---|
| 03/2023 | Manual de Créditos, Manual de Compras, Manual de Depósito y Procedimiento de Reclamos, todos en su primera versión (era Fénix) |
| 2023 | Procedimiento de notas de crédito y Circular de vacaciones |
| 2024 | Circular de pedido mínimo. Política de Calidad e Inocuidad (07/2024). Calidad pasa a reportar a Operaciones. Se implementa Lapacho |
| 01/2025 | Migración de Fénix a Tacuarí. Nuevo Manual de Depósito y Esquema de comisiones |
| 02/2025 | Nuevo Manual de Facturación y Reglamento interno |
| 03-06/2025 | Política de Compras, Procedimiento de alta de proveedores, Circular 04/2025 de notas de crédito (05/2025), Procedimiento de reclamos v2 y Política de cuentas clave |
| 07/2025 | Comité de créditos: se decide la Política de Créditos y Cobranzas v2, vigente desde el 01/08/2025 |
| 09/2025 | Nueva edición del Manual del Vendedor (ya remite a la Política de Créditos v2) |
| 08-11/2025 | Actas, mails, instructivos y FAQs varias |

"Hoy", para el corpus, es mediados de noviembre de 2025.

## Reglas para quien escribe documentos

1. Los textos de `hechos.csv` asignados a cada documento se copian **literalmente**, sin cambiar ni un espacio ni una tilde.
2. No inventar montos, plazos, porcentajes, horarios ni responsables fuera de esta biblia y de los hechos asignados. Sí se puede agregar prosa, contexto, pasos genéricos sin cifras, saludos y ruido.
3. Los documentos viejos no dicen que están reemplazados (en su momento estaban vigentes). Los nuevos pueden decirlo o no, según su ficha del catálogo.
4. En las contradicciones (grupos C), ningún documento menciona al otro ni dice que lo reemplaza.
5. Nada real: ni empresas, ni marcas, ni personas, ni CUIT válidos. Se pueden nombrar organismos genéricos como AFIP/ARCA, ART o "el banco" sin marca.
6. Los huecos que figuran en el catálogo se mencionan sin dar el dato.
