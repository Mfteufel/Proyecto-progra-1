# Sistema Oli — Gestión de servicios técnicos

Sistema de gestión por consola para una empresa de servicios técnicos (aires acondicionados, electricidad y mantenimiento general). Proyecto final de Programación I — UADE.

**Integrantes:** Marco Teufel, Santino Amadey, Fabrizio Ruarte, Catherine Alcaraz

---

## ¿Qué hace el sistema?

Permite a Oli (el dueño) gestionar:
- **Clientes** — altas, bajas, modificaciones y búsqueda
- **Técnicos** — Carlos, El Negro y Santi; gestión de estados y especialidades
- **Pedidos** — órdenes de trabajo con máquina de estados y asignación de técnicos
- **Cobros** — registro de pagos, cuotas, deudores y avance automático a "cobrado"
- **Repuestos** — piezas pedidas para cada trabajo (especiales o del estante)
- **Stock del estante** — insumos comunes con alerta de reposición; al usar un insumo se descuenta del estante y se suma al pedido automáticamente
- **Historial** — consulta de todo lo relacionado a un cliente y búsqueda de trabajos por garantía

---

## Estructura del proyecto

```
sistema_oli/
├── main.py           ← punto de entrada; solo llama a los menús de cada módulo
├── utils.py          ← funciones genéricas, constantes y helpers de input compartidos
├── clientes.py       ← datos + menú de clientes
├── tecnicos.py       ← datos + menú de técnicos
├── pedidos.py        ← datos + menú de pedidos
├── cobros.py         ← datos + menú de cobros
├── repuestos.py      ← datos + menú de repuestos por pedido
├── stock.py          ← datos + menú del estante de insumos
├── datos/
│   ├── clientes.json
│   ├── tecnicos.json
│   ├── pedidos.json
│   ├── cobros.json
│   ├── repuestos.json
│   └── stock.json
├── tests/
│   ├── test_utils.py     ← tests de las funciones base
│   ├── test_clientes.py  ← tests de alta, baja, modificación y búsqueda de clientes
│   └── test_pedidos.py   ← tests de creación, estados, filtros y eliminación de pedidos
└── README.md         ← este archivo
```

---

## Cómo correr el sistema

Desde la carpeta `sistema_oli/`:

```bash
python3 main.py
```

Aparece el menú principal:

```
=== SISTEMA OLI ===

1. Clientes
2. Técnicos
3. Pedidos
4. Cobros
5. Historial
6. Repuestos
7. Stock del estante
0. Salir
```

---

## Cómo correr los tests

Desde la carpeta `sistema_oli/`:

```bash
python3 tests/test_utils.py
python3 tests/test_clientes.py
python3 tests/test_pedidos.py
```

Cada suite restaura los archivos `.json` al estado original al terminar, así que se pueden correr en cualquier orden sin afectar los datos.

---

## Estado actual del proyecto

| Archivo | Estado | Qué hace |
|---|---|---|
| `utils.py` | ✅ Completo | Funciones genéricas: cargar/guardar JSON, generar IDs, buscar por ID. Helpers de input compartidos. Constantes. |
| `tests/test_utils.py` | ✅ Completo | 9 tests sobre las funciones base. |
| `clientes.py` | ✅ Completo | Alta, baja, modificación y búsqueda. Baja bloqueada si tiene pedidos. |
| `tecnicos.py` | ✅ Completo | Alta, baja, listado por especialidad/disponibilidad, cambio de estado. Baja bloqueada si tiene pedidos activos. |
| `pedidos.py` | ✅ Completo | Alta, baja, filtros, asignación de técnico, avance de estado lineal. |
| `cobros.py` | ✅ Completo | Registro de cobros/cuotas, deuda, deudores. Al pagar todo avanza el pedido a "cobrado". Pide precio del trabajo si falta. |
| `repuestos.py` | ✅ Completo | Repuestos por pedido. Carga manual para piezas especiales; las del estante entran vía `stock.usar_insumo()`. Avance de estado lineal. |
| `stock.py` | ✅ Completo | Estante de insumos comunes. `usar_insumo()` descuenta del estante y registra el repuesto en el pedido en un solo paso. Alerta automática cuando un insumo llega al mínimo. |
| `main.py` | ✅ Completo | Menú principal. Solo importa y llama a los menús de cada módulo. |
| `historial.py` | ✅ Completo | Consulta del historial por cliente: todos sus pedidos, cobros y repuestos. Incluye búsqueda de trabajos por garantía (regex, sin distinguir mayúsculas). |
| `tests/test_clientes.py` | ✅ Completo | 9 tests: crear, buscar, modificar y eliminar clientes. Valida integridad referencial. |
| `tests/test_pedidos.py` | ✅ Completo | 9 tests: crear, filtrar, cambiar estado y eliminar pedidos. Valida secuencia lineal de estados. |

---

## Arquitectura y convenciones

### Patrón de cada módulo

Cada módulo tiene dos secciones bien separadas:

1. **Funciones de datos** — trabajan con los JSON. Sin `input()` ni `print()` de UI. Usables desde tests o desde otros módulos.
2. **Menú** — `menu_X()` y funciones privadas `_nombre()` que manejan toda la interacción por consola.

`main.py` solo importa los `menu_X()` y arma el menú principal.

### Helpers de input (en utils.py)

```python
pedir_texto(mensaje)         # string no vacío
pedir_entero(mensaje)        # entero, repite si hay error
pedir_opcion(mensaje, lista) # opciones numeradas, devuelve el valor elegido
pedir_confirmacion(mensaje)  # s/n → True/False
```

---

## Cómo están guardados los datos

Cada entidad se guarda en un archivo `.json` dentro de `datos/`. Campos sin valor usan `null`.

**stock.json** — insumos del estante
```json
[
  {"id_insumo": 1, "nombre": "Rollo de cable", "unidad": "rollos", "cantidad": 5, "cantidad_minima": 2}
]
```

**repuestos.json** — piezas usadas en cada trabajo
```json
[
  {"id_repuesto": 1, "id_pedido": 1, "id_tecnico": null, "descripcion": "Térmica 25A", "estado": "solicitado", "precio": null}
]
```

**cobros.json**
```json
[
  {"id_cobro": 1, "id_pedido": 2, "monto": 5000.0, "forma_pago": "cuotas", "recibido_por": "Oli", "estado": "pagado", "fecha": "06/06/2026"}
]
```

---

## Máquinas de estado

**Pedidos** (avance lineal, no se puede retroceder ni saltar):
```
pendiente → asignado → en_curso → terminado → cobrado
```

**Repuestos** (avance lineal; al pasar a "entregado" requiere indicar el técnico):
```
solicitado → comprado → entregado → instalado
```

---

## Reglas de integridad referencial

| Operación | Validación |
|---|---|
| Crear pedido | `id_cliente` debe existir |
| Asignar técnico | `id_tecnico` debe existir |
| Eliminar cliente | No puede tener pedidos asociados |
| Eliminar técnico | No puede tener pedidos en estado distinto de "cobrado" |
| Eliminar pedido | No puede tener cobros ni repuestos |
| Registrar cobro | Pedido debe estar en "terminado" o "cobrado" |
| Usar insumo del estante | Pedido debe existir; stock debe ser suficiente |
| Avanzar repuesto a "entregado" | Requiere indicar el técnico que lo recibe |

---

## Stock del estante — cómo funciona

Oli tiene insumos comunes ("infaltables") guardados en el taller: cables, térmicas, caño de cobre, gas refrigerante, tornillos, tarugos, conectores, cinta aisladora y caños plásticos.

Cuando un técnico agarra algo del estante para un trabajo:
1. Se elige el insumo y la cantidad desde el menú **Stock → Usar insumo en un pedido**
2. El sistema descuenta la cantidad del estante
3. El sistema crea automáticamente un repuesto en el pedido para que Oli no se olvide de cobrárselo al cliente
4. Si la cantidad restante queda en el mínimo o por debajo, el sistema avisa: *"¡Hay que reponer!"*

Cuando Oli vuelve del mayorista usa **Stock → Reponer stock** para sumar la cantidad comprada.

### Insumos precargados

| ID | Insumo | Unidad | Mínimo |
|---|---|---|---|
| 1 | Rollo de cable | rollos | 2 |
| 2 | Térmica 25A | unidades | 2 |
| 3 | Caño de cobre | rollos | 1 |
| 4 | Garrafa gas refrigerante | garrafas | 1 |
| 5 | Caja de tornillos | cajas | 1 |
| 6 | Tarugos | bolsas | 1 |
| 7 | Conectores eléctricos | bolsas | 2 |
| 8 | Cinta aisladora | unidades | 3 |
| 9 | Caño plástico blanco | unidades | 3 |

---

## Técnicos del sistema (precargados)

| ID | Nombre | Especialidad |
|---|---|---|
| 1 | Carlos | Eléctrica |
| 2 | El Negro | Aires acondicionados |
| 3 | Santi | Multiuso / todo terreno |

---

## Reglas del proyecto (restricciones del profesor)

- Sin clases — solo funciones
- Sin librerías externas — solo biblioteca estándar de Python
- IDs autoincrementales generados por el sistema
- Datos persistidos en archivos `.json`
- Uso obligatorio de: `lambda`, `map`, `filter`, `functools.reduce`, recursividad, excepciones, expresiones regulares

---

## Librerías utilizadas

No se requiere instalar nada. Todo es biblioteca estándar de Python 3:

| Librería | Uso |
|---|---|
| `json` | Leer y escribir archivos `.json` |
| `os` | Rutas de archivos, crear carpeta `datos/` si no existe |
| `re` | Validación de teléfonos y fechas; búsqueda de garantías en historial |
| `functools` | `reduce` para acumular deuda de cobros pendientes |

---

## Limitaciones conocidas

- **Sin autenticación:** cualquier persona que ejecute el sistema tiene acceso total. No hay usuarios ni contraseñas.
- **Un solo proceso a la vez:** los `.json` se leen y escriben en cada operación. Si dos personas abren el sistema al mismo tiempo pueden pisarse los datos.
- **Sin paginación:** si hay muchos clientes o pedidos, se listan todos juntos en consola.
- **IDs no se reutilizan:** si se elimina un cliente con ID 5, el próximo cliente creado recibe el ID siguiente al máximo actual, no el 5.
- **Fechas sin validación de formato:** el sistema guarda la fecha del día automáticamente; si se carga una fecha manual (por ejemplo en tests), no se valida el formato `DD/MM/AAAA`.
- **Sin backup automático:** si un archivo `.json` se corrompe manualmente, el sistema lanza un error. No hay recuperación automática.

---

## Requisitos

- Python 3.x (no requiere instalar nada extra)
