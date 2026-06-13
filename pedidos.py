"""
pedidos.py — Gestión de pedidos/órdenes de trabajo del sistema Oli.

Funciones de datos: crear_pedido, listar_pedidos, listar_pedidos_por_estado,
                    listar_pedidos_por_cliente, listar_pedidos_por_tecnico,
                    asignar_tecnico, cambiar_estado_pedido, eliminar_pedido.
Menú:              menu_pedidos.
"""

from datetime import date

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, pedir_opcion, pedir_confirmacion,
    ARCHIVO_PEDIDOS, ARCHIVO_CLIENTES, ARCHIVO_TECNICOS,
    ARCHIVO_COBROS, ARCHIVO_REPUESTOS,
    ESTADOS_PEDIDO
)


# ── Funciones de datos ────────────────────────────────────────────────────────

def crear_pedido(datos):
    """
    Agrega un pedido nuevo.

    Recibe: datos (dict) con id_cliente, descripcion, urgente, fecha.
            id_tecnico es opcional (puede ser None).
    Devuelve: el dict del pedido creado, o None si el cliente no existe.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    if buscar_por_id(clientes, "id_cliente", datos["id_cliente"]) is None:
        print(f"No existe un cliente con ID {datos['id_cliente']}.")
        return None

    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    pedido = {
        "id_pedido": generar_id(pedidos, "id_pedido"),
        "id_cliente": datos["id_cliente"],
        "id_tecnico": datos.get("id_tecnico", None),
        "descripcion": datos["descripcion"],
        "urgente": datos.get("urgente", False),
        "fecha": datos["fecha"],
        "estado": "pendiente",
        "precio": None
    }
    pedidos.append(pedido)
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)
    return pedido


def listar_pedidos():
    """
    Devuelve todos los pedidos.

    Recibe: nada.
    Devuelve: lista de dicts; [] si no hay pedidos.
    """
    return cargar_datos(ARCHIVO_PEDIDOS)


def listar_pedidos_por_estado(estado):
    """
    Devuelve los pedidos que tienen el estado indicado.

    Recibe: estado (str).
    Devuelve: lista de dicts, o None si el estado es inválido.
    """
    if estado not in ESTADOS_PEDIDO:
        print(f"Estado inválido. Debe ser uno de: {ESTADOS_PEDIDO}")
        return None

    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    return list(filter(lambda p: p["estado"] == estado, pedidos))


def listar_pedidos_por_cliente(id_cliente):
    """
    Devuelve todos los pedidos de un cliente.

    Recibe: id_cliente (int).
    Devuelve: lista de dicts.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    return list(filter(lambda p: p["id_cliente"] == id_cliente, pedidos))


def listar_pedidos_por_tecnico(id_tecnico):
    """
    Devuelve todos los pedidos asignados a un técnico.

    Recibe: id_tecnico (int).
    Devuelve: lista de dicts.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    return list(filter(lambda p: p["id_tecnico"] == id_tecnico, pedidos))


def asignar_tecnico(id_pedido, id_tecnico):
    """
    Asigna o reasigna un técnico a un pedido. Funciona en cualquier estado.
    Pasar id_tecnico=None desasigna al técnico.

    Recibe: id_pedido (int), id_tecnico (int o None).
    Devuelve: el dict del pedido actualizado, o None si el pedido o técnico no existen.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    pedido = buscar_por_id(pedidos, "id_pedido", id_pedido)

    if pedido is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return None

    if id_tecnico is not None:
        tecnicos = cargar_datos(ARCHIVO_TECNICOS)
        if buscar_por_id(tecnicos, "id_tecnico", id_tecnico) is None:
            print(f"No existe un técnico con ID {id_tecnico}.")
            return None

    pedido["id_tecnico"] = id_tecnico
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)
    return pedido


def cambiar_estado_pedido(id_pedido, nuevo_estado):
    """
    Avanza el estado de un pedido al siguiente en la secuencia lineal.
    Secuencia: pendiente → asignado → en_curso → terminado → cobrado

    Recibe: id_pedido (int), nuevo_estado (str).
    Devuelve: el dict actualizado, o None si hay error.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    pedido = buscar_por_id(pedidos, "id_pedido", id_pedido)

    if pedido is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return None

    estado_actual = pedido["estado"]
    indice_actual = ESTADOS_PEDIDO.index(estado_actual)
    indice_nuevo = ESTADOS_PEDIDO.index(nuevo_estado) if nuevo_estado in ESTADOS_PEDIDO else -1

    if indice_nuevo == -1:
        print(f"Estado inválido. Debe ser uno de: {ESTADOS_PEDIDO}")
        return None

    if indice_nuevo != indice_actual + 1:
        siguiente = ESTADOS_PEDIDO[indice_actual + 1] if indice_actual + 1 < len(ESTADOS_PEDIDO) else None
        if siguiente:
            print(f"El pedido está en '{estado_actual}'. Solo puede avanzar a '{siguiente}'.")
        else:
            print(f"El pedido ya está en el estado final '{estado_actual}'.")
        return None

    pedido["estado"] = nuevo_estado
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)
    return pedido


def eliminar_pedido(id_pedido):
    """
    Elimina un pedido si no tiene cobros ni repuestos asociados.

    Recibe: id_pedido (int).
    Devuelve: True si se eliminó, False si no existe o tiene registros asociados.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    pedido = buscar_por_id(pedidos, "id_pedido", id_pedido)

    if pedido is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return False

    cobros = cargar_datos(ARCHIVO_COBROS)
    if any(c["id_pedido"] == id_pedido for c in cobros):
        print(f"No se puede eliminar el pedido {id_pedido} porque tiene cobros asociados.")
        return False

    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    if any(r["id_pedido"] == id_pedido for r in repuestos):
        print(f"No se puede eliminar el pedido {id_pedido} porque tiene repuestos asociados.")
        return False

    pedidos = [p for p in pedidos if p["id_pedido"] != id_pedido]
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)
    return True


# ── Menú de pedidos ───────────────────────────────────────────────────────────

def menu_pedidos():
    while True:
        print("\n=== PEDIDOS ===")
        print("1. Listar todos los pedidos")
        print("2. Filtrar por estado")
        print("3. Ver pedidos de un cliente")
        print("4. Ver pedidos de un técnico")
        print("5. Cargar pedido nuevo")
        print("6. Asignar / cambiar técnico")
        print("7. Cambiar estado de pedido")
        print("8. Eliminar pedido")
        print("0. Volver al menú principal")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            _listar_pedidos()
        elif opcion == "2":
            _filtrar_por_estado()
        elif opcion == "3":
            _pedidos_por_cliente()
        elif opcion == "4":
            _pedidos_por_tecnico()
        elif opcion == "5":
            _cargar_pedido()
        elif opcion == "6":
            _asignar_tecnico()
        elif opcion == "7":
            _cambiar_estado()
        elif opcion == "8":
            _eliminar_pedido()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


def _formato_pedido(p):
    tecnico = f"Técnico ID {p['id_tecnico']}" if p["id_tecnico"] else "Sin técnico"
    urgente = " [URGENTE]" if p["urgente"] else ""
    precio = f"${p['precio']}" if p["precio"] is not None else "sin precio"
    return (f"  [{p['id_pedido']}] Cliente {p['id_cliente']} — {tecnico} — "
            f"{p['estado']}{urgente} — {p['fecha']} — {precio}\n"
            f"       {p['descripcion']}")


def _listar_pedidos():
    print("\n--- Pedidos registrados ---")
    pedidos = listar_pedidos()
    if not pedidos:
        print("No hay pedidos cargados.")
        return
    for p in pedidos:
        print(_formato_pedido(p))


def _filtrar_por_estado():
    print("\n--- Filtrar pedidos por estado ---")
    print("Estados disponibles:")
    estado = pedir_opcion("Elegí el estado: ", ESTADOS_PEDIDO)
    pedidos = listar_pedidos_por_estado(estado)
    if not pedidos:
        print(f"No hay pedidos en estado '{estado}'.")
        return
    for p in pedidos:
        print(_formato_pedido(p))


def _pedidos_por_cliente():
    print("\n--- Pedidos por cliente ---")
    id_cliente = pedir_entero("ID del cliente: ")
    pedidos = listar_pedidos_por_cliente(id_cliente)
    if not pedidos:
        print(f"No hay pedidos para el cliente ID {id_cliente}.")
        return
    for p in pedidos:
        print(_formato_pedido(p))


def _pedidos_por_tecnico():
    print("\n--- Pedidos por técnico ---")
    id_tecnico = pedir_entero("ID del técnico: ")
    pedidos = listar_pedidos_por_tecnico(id_tecnico)
    if not pedidos:
        print(f"No hay pedidos asignados al técnico ID {id_tecnico}.")
        return
    for p in pedidos:
        print(_formato_pedido(p))


def _cargar_pedido():
    print("\n--- Cargar pedido nuevo ---")
    id_cliente = pedir_entero("ID del cliente: ")
    descripcion = pedir_texto("Descripción del trabajo: ")
    urgente = pedir_confirmacion("¿Es urgente?")
    fecha = date.today().strftime("%d/%m/%Y")

    pedido = crear_pedido({
        "id_cliente": id_cliente,
        "descripcion": descripcion,
        "urgente": urgente,
        "fecha": fecha
    })
    if pedido:
        print(f"\nPedido #{pedido['id_pedido']} creado para el cliente {id_cliente}.")


def _asignar_tecnico():
    print("\n--- Asignar / cambiar técnico ---")
    id_pedido = pedir_entero("ID del pedido: ")
    print("Ingresá el ID del técnico, o 0 para desasignar.")
    id_tecnico = pedir_entero("ID del técnico: ")
    if id_tecnico == 0:
        id_tecnico = None

    resultado = asignar_tecnico(id_pedido, id_tecnico)
    if resultado:
        if id_tecnico:
            print(f"Técnico {id_tecnico} asignado al pedido #{id_pedido}.")
        else:
            print(f"Técnico desasignado del pedido #{id_pedido}.")


def _cambiar_estado():
    print("\n--- Cambiar estado de pedido ---")
    id_pedido = pedir_entero("ID del pedido: ")

    pedido = buscar_por_id(listar_pedidos(), "id_pedido", id_pedido)
    if pedido is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return

    estado_actual = pedido["estado"]
    indice = ESTADOS_PEDIDO.index(estado_actual)
    if indice + 1 >= len(ESTADOS_PEDIDO):
        print(f"El pedido ya está en el estado final '{estado_actual}'.")
        return

    siguiente = ESTADOS_PEDIDO[indice + 1]
    print(f"Estado actual: {estado_actual}")
    if not pedir_confirmacion(f"¿Avanzar a '{siguiente}'?"):
        print("Cancelado.")
        return

    cambiar_estado_pedido(id_pedido, siguiente)
    print(f"Pedido #{id_pedido} avanzado a '{siguiente}'.")


def _eliminar_pedido():
    print("\n--- Eliminar pedido ---")
    id_pedido = pedir_entero("ID del pedido a eliminar: ")

    pedido = buscar_por_id(listar_pedidos(), "id_pedido", id_pedido)
    if pedido is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return

    if not pedir_confirmacion(f"¿Confirmás eliminar el pedido #{id_pedido}?"):
        print("Cancelado.")
        return

    eliminar_pedido(id_pedido)
