"""
repuestos.py — Gestión de repuestos por pedido del sistema Oli.

Funciones de datos: registrar_repuesto, listar_repuestos_por_pedido,
                    listar_repuestos_por_tecnico, listar_pendientes_compra,
                    avanzar_estado_repuesto.
Menú:              menu_repuestos.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, pedir_opcion, pedir_confirmacion,
    ARCHIVO_REPUESTOS, ARCHIVO_PEDIDOS, ARCHIVO_TECNICOS,
    ESTADOS_REPUESTO
)


# ── Funciones de datos ────────────────────────────────────────────────────────

def registrar_repuesto(datos):
    """
    Registra un repuesto asociado a un pedido.
    Para piezas especiales que no salen del estante; las del estante
    se registran automáticamente via stock.usar_insumo().

    Recibe: datos (dict) con id_pedido, descripcion.
            id_tecnico y precio son opcionales.
    Devuelve: el dict del repuesto creado, o None si el pedido no existe.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    if buscar_por_id(pedidos, "id_pedido", datos["id_pedido"]) is None:
        print(f"No existe un pedido con ID {datos['id_pedido']}.")
        return None

    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    repuesto = {
        "id_repuesto": generar_id(repuestos, "id_repuesto"),
        "id_pedido": datos["id_pedido"],
        "id_tecnico": datos.get("id_tecnico", None),
        "descripcion": datos["descripcion"],
        "estado": "solicitado",
        "precio": datos.get("precio", None)
    }
    repuestos.append(repuesto)
    guardar_datos(ARCHIVO_REPUESTOS, repuestos)
    return repuesto


def listar_repuestos_por_pedido(id_pedido):
    """
    Devuelve todos los repuestos de un pedido.

    Recibe: id_pedido (int).
    Devuelve: lista de dicts.
    """
    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    return list(filter(lambda r: r["id_pedido"] == id_pedido, repuestos))


def listar_repuestos_por_tecnico(id_tecnico):
    """
    Devuelve todos los repuestos asignados a un técnico.

    Recibe: id_tecnico (int).
    Devuelve: lista de dicts.
    """
    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    return list(filter(lambda r: r["id_tecnico"] == id_tecnico, repuestos))


def listar_pendientes_compra():
    """
    Devuelve los repuestos en estado "solicitado" (hay que salir a comprarlos).

    Recibe: nada.
    Devuelve: lista de dicts.
    """
    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    return list(filter(lambda r: r["estado"] == "solicitado", repuestos))


def avanzar_estado_repuesto(id_repuesto, nuevo_estado, id_tecnico=None):
    """
    Avanza el estado de un repuesto al siguiente en la secuencia lineal.
    Al pasar a "entregado" requiere id_tecnico.

    Secuencia: solicitado → comprado → entregado → instalado

    Recibe: id_repuesto (int), nuevo_estado (str), id_tecnico (int, obligatorio si nuevo_estado == "entregado").
    Devuelve: el dict actualizado, o None si hay error.
    """
    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    repuesto = buscar_por_id(repuestos, "id_repuesto", id_repuesto)

    if repuesto is None:
        print(f"No existe un repuesto con ID {id_repuesto}.")
        return None

    estado_actual = repuesto["estado"]
    indice_actual = ESTADOS_REPUESTO.index(estado_actual)
    indice_nuevo = ESTADOS_REPUESTO.index(nuevo_estado) if nuevo_estado in ESTADOS_REPUESTO else -1

    if indice_nuevo == -1:
        print(f"Estado inválido. Debe ser uno de: {ESTADOS_REPUESTO}")
        return None

    if indice_nuevo != indice_actual + 1:
        siguiente = ESTADOS_REPUESTO[indice_actual + 1] if indice_actual + 1 < len(ESTADOS_REPUESTO) else None
        if siguiente:
            print(f"El repuesto está en '{estado_actual}'. Solo puede avanzar a '{siguiente}'.")
        else:
            print(f"El repuesto ya está en el estado final '{estado_actual}'.")
        return None

    if nuevo_estado == "entregado" and id_tecnico is None:
        print("Para pasar a 'entregado' tenés que indicar el técnico que lo recibió.")
        return None

    repuesto["estado"] = nuevo_estado
    if id_tecnico is not None:
        repuesto["id_tecnico"] = id_tecnico

    guardar_datos(ARCHIVO_REPUESTOS, repuestos)
    return repuesto


# ── Menú de repuestos ─────────────────────────────────────────────────────────

def menu_repuestos():
    while True:
        print("\n=== REPUESTOS ===")
        print("1. Ver repuestos de un pedido")
        print("2. Ver repuestos de un técnico")
        print("3. Cargar repuesto especial")
        print("4. Avanzar estado de repuesto")
        print("5. Ver pendientes de compra")
        print("0. Volver al menú principal")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            _repuestos_por_pedido()
        elif opcion == "2":
            _repuestos_por_tecnico()
        elif opcion == "3":
            _cargar_repuesto_especial()
        elif opcion == "4":
            _avanzar_estado()
        elif opcion == "5":
            _pendientes_compra()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


def _formato_repuesto(r):
    tecnico = f"Técnico ID {r['id_tecnico']}" if r["id_tecnico"] else "Sin técnico"
    precio = f"${r['precio']}" if r["precio"] is not None else "sin precio"
    return f"  [{r['id_repuesto']}] {r['descripcion']} — {r['estado']} — {tecnico} — {precio}"


def _repuestos_por_pedido():
    print("\n--- Repuestos de un pedido ---")
    id_pedido = pedir_entero("ID del pedido: ")
    repuestos = listar_repuestos_por_pedido(id_pedido)
    if not repuestos:
        print(f"No hay repuestos registrados para el pedido #{id_pedido}.")
        return
    for r in repuestos:
        print(_formato_repuesto(r))


def _repuestos_por_tecnico():
    print("\n--- Repuestos de un técnico ---")
    id_tecnico = pedir_entero("ID del técnico: ")
    repuestos = listar_repuestos_por_tecnico(id_tecnico)
    if not repuestos:
        print(f"No hay repuestos asignados al técnico ID {id_tecnico}.")
        return
    for r in repuestos:
        print(_formato_repuesto(r))


def _cargar_repuesto_especial():
    print("\n--- Cargar repuesto especial ---")
    print("(Usá esto para piezas que no están en el estante.)")
    print("(Para insumos del estante usá la opción 'Usar insumo del estante' en el menú de Stock.)")
    id_pedido = pedir_entero("ID del pedido: ")
    descripcion = pedir_texto("Descripción del repuesto: ")

    while True:
        try:
            precio_str = input("Precio (Enter para dejarlo vacío): $").strip()
            precio = float(precio_str) if precio_str else None
            break
        except ValueError:
            print("  Ingresá un número válido o dejá vacío.")

    repuesto = registrar_repuesto({
        "id_pedido": id_pedido,
        "descripcion": descripcion,
        "precio": precio
    })
    if repuesto:
        print(f"\nRepuesto '{descripcion}' registrado en el pedido #{id_pedido}.")


def _avanzar_estado():
    print("\n--- Avanzar estado de repuesto ---")
    id_repuesto = pedir_entero("ID del repuesto: ")

    repuestos = cargar_datos(ARCHIVO_REPUESTOS)
    repuesto = buscar_por_id(repuestos, "id_repuesto", id_repuesto)
    if repuesto is None:
        print(f"No existe un repuesto con ID {id_repuesto}.")
        return

    estado_actual = repuesto["estado"]
    indice = ESTADOS_REPUESTO.index(estado_actual)
    if indice + 1 >= len(ESTADOS_REPUESTO):
        print(f"El repuesto ya está en el estado final '{estado_actual}'.")
        return

    siguiente = ESTADOS_REPUESTO[indice + 1]
    print(f"Estado actual: {estado_actual}")
    if not pedir_confirmacion(f"¿Avanzar a '{siguiente}'?"):
        print("Cancelado.")
        return

    id_tecnico = None
    if siguiente == "entregado":
        id_tecnico = pedir_entero("ID del técnico que lo recibe: ")

    avanzar_estado_repuesto(id_repuesto, siguiente, id_tecnico)
    print(f"Repuesto #{id_repuesto} avanzado a '{siguiente}'.")


def _pendientes_compra():
    print("\n--- Repuestos pendientes de compra ---")
    repuestos = listar_pendientes_compra()
    if not repuestos:
        print("No hay repuestos pendientes de compra.")
        return
    for r in repuestos:
        print(f"  [{r['id_repuesto']}] Pedido #{r['id_pedido']} — {r['descripcion']}")
