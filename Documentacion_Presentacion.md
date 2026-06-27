# Documentación del Sistema Oli — Presentación

## 1. ¿Qué es el Sistema Oli?

Es un sistema de gestión por consola desarrollado en Python para una empresa de servicios técnicos. El dueño, Oli, llevaba todo en un cuaderno: pedidos, cobros, técnicos y repuestos. El sistema reemplaza ese cuaderno con un programa organizado que guarda los datos en archivos `.json`.

---

## 2. Arquitectura general

El sistema está dividido en **7 módulos**, cada uno en su propio archivo `.py`. Todos los módulos comparten un archivo central de utilidades.

```
main.py          → menú principal, punto de entrada
clientes.py      → gestión de clientes
tecnicos.py      → gestión de técnicos
pedidos.py       → gestión de pedidos/órdenes de trabajo
cobros.py        → gestión de cobros
historial.py     → historial y búsqueda de garantías
repuestos.py     → repuestos específicos por pedido
stock.py         → stock del estante (insumos comunes)
utils.py         → funciones compartidas por todos los módulos
datos/           → archivos .json donde se guardan los datos
```

### Cómo se conectan los módulos

```
Clientes ──┐
           ├──► Pedidos ──► Cobros
Técnicos ──┘        │
                    ├──► Repuestos ◄── Stock (cuando se usa un insumo)
                    │
                    └──► Historial (solo lectura, cruza todo)
```

---

## 3. utils.py — La base de todo

`utils.py` provee las funciones que usan **todos** los demás módulos. Sin este archivo, nada funciona.

### Funciones clave y su justificación

#### `cargar_datos(nombre_archivo)` y `guardar_datos(nombre_archivo, lista)`

**Qué hacen:** leen y escriben archivos `.json`. Todos los módulos llaman a estas dos funciones para persistir los datos.

**Justificación:** Oli necesita que los datos se guarden entre sesiones. El cuaderno físico se traspapelaba y la letra era ilegible. Los archivos `.json` reemplazan ese cuaderno con datos siempre legibles. Se usó `.json` porque el TP no permite bases de datos externas.

---

#### `generar_id(lista, nombre_id)`

**Qué hace:** devuelve el próximo ID disponible para una entidad (cliente, pedido, técnico, etc.). Si la lista está vacía, devuelve 1; si no, devuelve el máximo existente + 1.

**Justificación:** cada entidad necesita un identificador único para que los módulos puedan referenciarse entre sí (por ejemplo, un pedido guarda el `id_cliente` para saber a quién pertenece).

---

#### `buscar_por_id(lista, nombre_id, valor)` — **función recursiva**

**Qué hace:** busca un diccionario en una lista comparando el campo `nombre_id` con el `valor`. Se implementó de forma **recursiva**: si el primero no coincide, llama a sí misma con el resto de la lista.

```python
def buscar_por_id(lista, nombre_id, valor):
    if not lista:
        return None
    if lista[0][nombre_id] == valor:
        return lista[0]
    return buscar_por_id(lista[1:], nombre_id, valor)
```

**Justificación (requerimiento del TP):** la cátedra exige recursividad. Esta función es la más adecuada porque la búsqueda en una lista tiene estructura recursiva natural: "¿Es el primero? Si no, buscar en el resto."

---

#### `validar_telefono(telefono)` — **uso de regex**

**Qué hace:** valida que el teléfono tenga entre 8 y 15 dígitos, permitiendo guiones y espacios.

```python
patron = r"[\d\- ]{8,15}"
return bool(re.fullmatch(patron, telefono))
```

**Justificación:** Oli pide el teléfono del cliente para contactarlo. Sin validación, podría ingresarse cualquier texto y después no poder llamar. La expresión regular garantiza un formato mínimo válido. (El TP también exige uso de `re`.)

---

#### `pedir_fecha(mensaje)` — **uso de regex**

**Qué hace:** valida que la fecha ingresada tenga formato `DD/MM/AAAA`.

```python
patron = re.compile(r"^\d{2}/\d{2}/\d{4}$")
```

**Justificación:** Oli registra la fecha de cada pedido y cobro. Sin validación del formato, podría ingresar "martes" o "12-6" y después no poder ordenar ni mostrar los datos correctamente.

---

#### `pedir_opcion(mensaje, opciones)`

**Qué hace:** muestra una lista numerada de opciones y devuelve el valor elegido. Usa **lambda** implícitamente a través de `enumerate`.

**Justificación:** garantiza que el usuario solo pueda elegir valores válidos (por ejemplo, la especialidad del técnico tiene que ser `"electrica"`, `"aires"` o `"multiuso"`; no puede ingresarse cualquier texto).

---

## 4. clientes.py

### Funciones clave

#### `crear_cliente(datos)`

**Qué hace:** valida el tipo de cliente y el teléfono, genera un ID único y guarda el nuevo cliente en `clientes.json`.

**Justificación:**
> *"Lo básico: el nombre para saber con quién hablo, la dirección para mandarle a los chicos, y un teléfono por las dudas."* — Oli

Oli anota estos datos en el cuaderno a las apuradas y después no entiende su letra. Esta función fuerza que los datos queden bien registrados antes de guardarlos.

---

#### `buscar_clientes_por_nombre(nombre)` — **uso de filter + lambda + regex**

**Qué hace:** busca clientes cuyo nombre contenga el texto ingresado, sin importar mayúsculas.

```python
patron = re.compile(nombre, re.IGNORECASE)
return list(filter(lambda c: patron.search(c["nombre"]), clientes))
```

**Justificación:** Oli no siempre va a recordar el ID de un cliente; va a escribir "Rosa" y esperar encontrar a "Doña Rosa González". La búsqueda parcial e insensible a mayúsculas replica ese comportamiento natural.

---

#### `eliminar_cliente(id_cliente)`

**Qué hace:** antes de eliminar, verifica que el cliente no tenga pedidos asociados. Si tiene, bloquea la eliminación.

**Justificación:** Oli preguntó explícitamente:
> *"¿Qué pasa con las cosas que ya le hicimos antes? ¿Se borran de la memoria de la máquina?"*

La protección garantiza que aunque un cliente no vuelva más, sus pedidos, cobros e historial siguen existiendo para los totales del negocio.

---

## 5. tecnicos.py

### Funciones clave

#### `listar_disponibles()`

**Qué hace:** filtra los técnicos con estado `"disponible"`.

```python
return list(filter(lambda t: t["estado"] == "disponible", tecnicos))
```

**Justificación:**
> *"No tengo una pantalla mágica que me diga dónde están. Yo más o menos sé en la cabeza qué le di a cada uno a la mañana."* — Oli

Esta función es exactamente esa "pantalla mágica" que Oli pedía: con una sola consulta sabe quién está libre para mandarle un trabajo nuevo.

---

#### `listar_por_especialidad(especialidad)`

**Qué hace:** filtra los técnicos por especialidad (`electrica`, `aires`, `multiuso`).

**Justificación:** Oli explicó que tiene a Carlos para eléctrica, al Negro para aires y a Santi como comodín. Mandar al técnico equivocado es un problema real (Carlos puede revisar un aire, pero no es lo ideal). Esta función permite elegir al más adecuado.

---

#### `eliminar_tecnico(id_tecnico)`

**Qué hace:** bloquea la eliminación si el técnico tiene pedidos activos (en cualquier estado que no sea `"cobrado"`).

**Justificación:** no tendría sentido eliminar a un técnico que todavía tiene trabajos abiertos. Los pedidos quedarían huérfanos y Oli perdería la trazabilidad.

---

## 6. pedidos.py — El corazón del sistema

### Funciones clave

#### `crear_pedido(datos)`

**Qué hace:** registra un nuevo trabajo con cliente, descripción, urgencia, fecha y estado inicial `"pendiente"`.

**Justificación:**
> *"lo más urgente es el tema de los pedidos enganchado con la plata y los técnicos. O sea, saber qué laburo entró, a quién mandé y si se cobró o se debe."* — Oli

Este módulo es la máxima prioridad declarada. Cada mensaje de WhatsApp o llamado telefónico que hoy va al cuaderno pasa a ser un pedido en el sistema.

---

#### `cambiar_estado_pedido(id_pedido, nuevo_estado)`

**Qué hace:** avanza el estado del pedido de forma lineal y secuencial:

```
pendiente → asignado → en_curso → terminado → cobrado
```

No permite retroceder ni saltear pasos.

**Justificación:** Oli no sabe en qué estado están los trabajos; se entera de los terminados a la noche. Este flujo de estados permite que en cualquier momento pueda saber exactamente dónde está cada trabajo sin tener que llamar al técnico.

---

#### `listar_pedidos_por_estado(estado)` — **uso de filter + lambda**

**Qué hace:** devuelve solo los pedidos en el estado pedido.

```python
return list(filter(lambda p: p["estado"] == estado, pedidos))
```

**Justificación:** Oli necesita ver "qué laburos entran hoy que están pendientes" o "cuáles terminaron y hay que cobrar". El filtro por estado reemplaza el cuaderno donde buscaba a mano trabajo por trabajo.

---

#### `eliminar_pedido(id_pedido)`

**Qué hace:** bloquea la eliminación si el pedido tiene cobros o repuestos asociados.

**Justificación:** protege la integridad de los datos. Si se elimina un pedido que ya tiene un cobro registrado, ese cobro quedaría apuntando a la nada y los números del negocio no cerrarían.

---

## 7. cobros.py

### Funciones clave

#### `registrar_cobro(datos)`

**Qué hace:** registra un pago (o una cuota) para un pedido ya terminado. Guarda quién recibió el dinero (`recibido_por`), la forma de pago y el estado (`pendiente` o `pagado`).

**Justificación:**
> *"el cliente le da la plata en la mano al técnico. El técnico se guarda el efectivo en el bolsillo... y recién me lo da tres días después"* — Oli

El campo `recibido_por` resuelve exactamente este problema: Oli puede anotar "lo recibió Carlos" y saber que ese dinero existe aunque todavía no le llegó. Las cuotas se implementan como múltiples cobros para el mismo pedido.

---

#### `calcular_deuda_pedido(id_pedido)` — **uso de reduce**

**Qué hace:** suma los montos de todos los cobros pendientes de un pedido usando `reduce`.

```python
from functools import reduce
pendientes = list(filter(lambda c: c["estado"] == "pendiente", cobros))
return reduce(lambda acum, c: acum + c["monto"], pendientes, 0)
```

**Justificación:** Oli tiene plata "flotando en el aire". Esta función la materializa: de un vistazo dice exactamente cuánto falta cobrar de un trabajo.

---

#### `listar_deudores()`

**Qué hace:** cruza cobros, pedidos y clientes para devolver la lista de clientes con deuda pendiente y el monto total.

**Justificación:**
> *"Fulanito te debe tanta plata"* — lo que Oli quería poder ver con un solo botón.

Es la vista más importante para la gestión del negocio: cuánto le deben y quién.

---

#### `marcar_pago(id_cobro)`

**Qué hace:** marca un cobro como pagado. Si todos los cobros del pedido quedan pagados, avanza el pedido automáticamente a `"cobrado"`.

**Justificación:** automatiza el paso final del flujo sin que Oli tenga que hacerlo manualmente. Cuando el último pago entra, el sistema cierra el pedido solo.

---

## 8. historial.py — Garantías y reclamos

### Funciones clave

#### `historial_por_cliente(id_cliente)`

**Qué hace:** cruza los datos de clientes, pedidos, técnicos, cobros y repuestos para devolver el historial completo de un cliente en una sola consulta.

**Justificación:** Oli lo pidió explícitamente al final de la charla:
> *"Me vendría bárbaro que, cuando un cliente viejo me llama por un problema en un laburo que ya hicimos, yo pueda encontrar rápido ese historial para saber qué pasó y no quedar como un improvisado."*

Este módulo es de **solo lectura**: no modifica ningún archivo. Simplemente cruza los datos ya existentes.

---

#### `buscar_garantia(id_cliente, texto)` — **uso de regex**

**Qué hace:** busca dentro del historial de un cliente los pedidos cuya descripción contenga una palabra clave.

```python
patron = re.compile(texto, re.IGNORECASE)
return [p for p in historial["pedidos"] if patron.search(p["descripcion"])]
```

**Justificación:** cuando Doña Rosa llama diciendo "el aire que me instalaron hace dos semanas no enfría", Oli puede buscar "aire" en el historial de esa clienta y encontrar al instante cuándo fue, quién fue y qué se hizo. Antes tenía que revolver cuadernos viejos.

---

## 9. repuestos.py

### Funciones clave

#### `registrar_repuesto(datos)`

**Qué hace:** registra una pieza específica asociada a un pedido con estado inicial `"solicitado"`.

**Justificación:**
> *"Terminamos gastando el doble y con dos piezas iguales en la mano"* — Oli

Cuando el técnico avisa que necesita un motor o una placa, se registra en el sistema. Así Oli sabe si ya lo averiguó, si ya lo compró o si todavía está pendiente.

---

#### `avanzar_estado_repuesto(id_repuesto, nuevo_estado)` — flujo lineal

**Qué hace:** avanza el estado del repuesto de forma secuencial:

```
solicitado → comprado → entregado → instalado
```

Al pasar a `"entregado"`, requiere indicar el técnico que lo recibe.

**Justificación:** resuelve el caos que describió Oli: "¿se compró?, ¿quién lo tiene?, ¿ya se instaló?". El estado del repuesto responde esas tres preguntas.

---

#### `listar_pendientes_compra()`

**Qué hace:** devuelve todos los repuestos en estado `"solicitado"` (todavía no se salió a comprar).

**Justificación:** Oli se olvidaba de averiguar repuestos porque le entraba un llamado y se distraía. Con esta lista, tiene un recordatorio inmediato de lo que falta comprar.

---

## 10. stock.py

### Funciones clave

#### `usar_insumo(id_insumo, cantidad, id_pedido, id_tecnico)`

**Qué hace:** descuenta la cantidad del estante, registra automáticamente el insumo como repuesto del pedido, y avisa si el stock bajó del mínimo.

```python
insumo["cantidad"] -= cantidad
registrar_repuesto({"id_pedido": id_pedido, "descripcion": descripcion})
if insumo["cantidad"] <= insumo["cantidad_minima"]:
    print(f"  ⚠ Quedan solo {insumo['cantidad']}...")
```

**Justificación:** Oli fue muy preciso en lo que necesitaba:
> *"si Carlos usa una térmica de mi cajón para Doña Rosa, el sistema me descuente una del estante y se la sume a la cuenta de ella para que yo no me olvide de cobrársela"*

Esta función hace exactamente eso: una sola operación hace dos cosas a la vez.

---

#### `listar_stock_bajo()`

**Qué hace:** devuelve los insumos cuya cantidad está en o por debajo del mínimo definido.

```python
return list(filter(lambda i: i["cantidad"] <= i["cantidad_minima"], stock))
```

**Justificación:**
> *"de golpe viene Carlos a la mañana y me dice: 'Che, Oli, no hay más cinta aisladora'. Ahí me quiero matar porque tengo que salir corriendo a la ferretería del barrio que me arranca la cabeza con los precios."*

Con esta función Oli puede revisar el estante virtual antes de que los técnicos lleguen y comprar en el mayorista con tiempo.

---

## 11. main.py — Punto de entrada

**Qué hace:** muestra el menú principal con las 7 opciones y maneja excepciones para que un error en un módulo no tire abajo todo el programa.

```python
try:
    ...  # llamada al módulo
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
finally:
    print("Volviendo al menú principal...")
```

**Justificación (requerimiento del TP):** la cátedra exige manejo de excepciones. El bloque `try/except/finally` garantiza que si el usuario ingresa un dato inválido o ocurre un error inesperado, el sistema vuelve al menú en lugar de caerse.

---

## 12. Resumen: ¿por qué cada módulo existe?

| Módulo | Problema de Oli que resuelve | Prioridad declarada |
|---|---|---|
| Clientes | "Anoto la dirección a las apuradas y no entiendo mi letra" | Media |
| Técnicos | "No tengo una pantalla mágica que me diga dónde están" | Media |
| Pedidos | "No sé si el técnico está yendo para allá o si ya terminó" | **ALTA** |
| Cobros | "Tengo una plata flotando en el aire que ni yo sé cuánto es" | **ALTA** |
| Historial | "Tengo que revolver el cuaderno viejo para atender un reclamo" | Media |
| Repuestos | "Terminamos gastando el doble con dos piezas iguales en la mano" | Baja |
| Stock | "De golpe no hay más cinta aisladora y salgo corriendo a la ferretería" | Baja |

---

## 13. Conceptos de programación usados y dónde

| Concepto | Dónde se usa |
|---|---|
| **Recursividad** | `buscar_por_id()` en `utils.py` |
| **Expresiones regulares (re)** | `validar_telefono()`, `pedir_fecha()`, `buscar_clientes_por_nombre()`, `buscar_garantia()` |
| **Lambda + filter** | `listar_disponibles()`, `listar_pedidos_por_estado()`, `listar_deudores()`, `listar_stock_bajo()`, `buscar_clientes_por_nombre()` |
| **reduce** | `calcular_deuda_pedido()` en `cobros.py` |
| **Excepciones (try/except/finally)** | `main.py` y todos los menús de cada módulo |
| **Archivos JSON** | `cargar_datos()` y `guardar_datos()` en `utils.py` |
| **Módulos separados** | Un archivo `.py` por módulo, importados desde `main.py` |
| **pytest** | `tests/` — 27 tests automatizados |

---

## 14. Tests — verificación automatizada

El proyecto incluye 27 tests organizados en tres archivos dentro de `tests/`. Se ejecutan con `pytest`.

### Cómo correr los tests

```bash
python3 -m pytest tests/ -v
```

### Qué se testea y por qué

| Archivo | Tests | Qué verifican |
|---|---|---|
| `test_utils.py` | 9 | `generar_id`, `buscar_por_id` (recursiva), `cargar_datos`, `guardar_datos` |
| `test_clientes.py` | 9 | Crear, buscar, modificar y eliminar clientes; validaciones de tipo y teléfono; protección de baja |
| `test_pedidos.py` | 9 | Crear pedidos, filtrar por estado, avance lineal de estados, eliminar con protección de integridad |

### Conceptos de pytest usados

**`assert`** — verifica que el resultado sea el esperado:
```python
assert cliente["tipo"] == "particular", "Tipo incorrecto"
assert resultado is None, "Esperaba None"
```

**`pytest.raises`** — verifica que una función lance la excepción correcta:
```python
with pytest.raises(ValueError):
    crear_cliente({"tipo": "fantasma", ...})
```

**`from archivo import funcion`** — cada test importa solo las funciones que necesita testear:
```python
from clientes import crear_cliente, buscar_cliente_por_id, modificar_cliente, eliminar_cliente
from utils import cargar_datos, guardar_datos, ARCHIVO_CLIENTES
```

### Patrón backup/restore

Cada test guarda los datos reales antes de ejecutarse y los restaura al terminar, usando `try/finally`. Así los tests no modifican los datos del sistema:

```python
def test_crear_cliente_valido():
    clientes, pedidos = _backup()   # guarda datos reales
    try:
        cliente = crear_cliente({...})
        assert cliente is not None
    finally:
        _restore(clientes, pedidos)  # restaura siempre, aunque el test falle
```
