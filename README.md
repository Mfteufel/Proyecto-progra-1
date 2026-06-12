# Sistema Oli — Gestión de servicios técnicos

Sistema de gestión por consola para una empresa de servicios técnicos (aires acondicionados, electricidad y mantenimiento general). Proyecto final de Programación I — UADE.

---

## ¿Qué hace el sistema?

Permite a Oli (el dueño) gestionar:
- **Clientes** — altas, bajas, modificaciones y búsqueda
- **Técnicos** — Carlos, El Negro y Santi (próximamente)
- **Pedidos** — órdenes de trabajo con estados y asignación de técnicos (próximamente)
- **Cobros** — registro de pagos, cuotas y deudores (próximamente)
- **Repuestos** — piezas pedidas para cada trabajo (próximamente)
- **Historial** — consulta de todo lo relacionado a un cliente (próximamente)

---

## Estructura del proyecto

```
sistema_oli/
├── main.py           ← punto de entrada, acá se corre el sistema
├── utils.py          ← funciones y constantes compartidas por todos los módulos
├── clientes.py       ← módulo de clientes (único módulo completo hasta ahora)
├── datos/            ← archivos JSON con los datos del sistema
│   ├── clientes.json
│   ├── tecnicos.json
│   ├── pedidos.json
│   ├── cobros.json
│   └── repuestos.json
├── tests/
│   └── test_utils.py ← tests de las funciones base
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
2. Técnicos        (próximamente)
3. Pedidos         (próximamente)
4. Cobros          (próximamente)
5. Historial       (próximamente)
6. Repuestos       (próximamente)
0. Salir
```

Por ahora solo el menú de **Clientes** está activo. Las demás opciones muestran "próximamente".

---

## Cómo correr los tests

Desde la carpeta `sistema_oli/`:

```bash
python3 tests/test_utils.py
```

Tiene que mostrar algo así:

```
=== TESTS DE utils.py ===

✓ generar_id: lista vacía devuelve 1
✓ generar_id: devuelve max + 1 (no largo + 1)
...
9 aprobados, 0 fallados de 9 tests
```

---

## Estado actual del proyecto

| Archivo | Estado | Qué hace |
|---|---|---|
| `utils.py` | ✅ Completo | Funciones genéricas: cargar/guardar JSON, generar IDs, buscar por ID. Constantes compartidas. |
| `tests/test_utils.py` | ✅ Completo | 9 tests sobre `generar_id`, `buscar_por_id`, `cargar_datos` y `guardar_datos`. |
| `clientes.py` | ✅ Completo | Alta, baja, modificación y búsqueda de clientes con validaciones de integridad. |
| `main.py` | 🔄 En progreso | Menú principal funcionando. Solo clientes conectado, el resto "próximamente". |
| `tecnicos.py` | ❌ Pendiente | Gestión de técnicos. |
| `pedidos.py` | ❌ Pendiente | Gestión de pedidos y estados. |
| `cobros.py` | ❌ Pendiente | Registro de cobros y deudas. |
| `historial.py` | ❌ Pendiente | Consulta del historial por cliente. |
| `repuestos.py` | ❌ Pendiente | Gestión de repuestos por pedido. |
| `tests/test_clientes.py` | ❌ Pendiente | Tests de integridad de clientes. |
| `tests/test_pedidos.py` | ❌ Pendiente | Tests de integridad de pedidos. |

---

## Cómo están guardados los datos

Cada entidad se guarda en un archivo `.json` dentro de la carpeta `datos/`. Cada archivo es una lista de diccionarios. Ejemplo de `clientes.json`:

```json
[
  {
    "id_cliente": 1,
    "nombre": "Doña Rosa",
    "direccion": "Av. Siempreviva 742",
    "telefono": "11-1234-5678",
    "tipo": "particular"
  }
]
```

Los datos de prueba ya están cargados en los archivos JSON con clientes, técnicos, pedidos, cobros y repuestos de ejemplo.

---

## Reglas importantes del proyecto

- **Sin clases** en los módulos del sistema (restricción del profesor). Solo funciones.
- **Sin librerías externas** — solo biblioteca estándar de Python (`json`, `os`).
- **Los IDs son autoincrementales** — el sistema los genera solo, nunca se ingresan a mano.
- **Los datos persisten** en archivos `.json` — si cerrás y abrís el sistema, los datos siguen ahí.
- **Mensajes en español argentino** — el sistema habla como habla Oli.

---

## Técnicos del sistema (precargados)

| ID | Nombre | Especialidad |
|---|---|---|
| 1 | Carlos | Eléctrica (el más experimentado) |
| 2 | El Negro | Aires acondicionados |
| 3 | Santi | Multiuso / todo terreno |

---

## Requisitos

- Python 3.x (no requiere instalar nada extra)
