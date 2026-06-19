"""
historial.py — Consulta de historial por cliente del sistema Oli.

Funciones de datos: historial_por_cliente, buscar_garantia.
Menú:              menu_historial.

Módulo de solo lectura: no modifica ningún archivo .json.
"""

from utils import (
    cargar_datos, buscar_por_id,
    pedir_entero, pedir_texto,
    ARCHIVO_CLIENTES, ARCHIVO_TECNICOS,
    ARCHIVO_PEDIDOS, ARCHIVO_COBROS, ARCHIVO_REPUESTOS
)


# ── Funciones de datos ────────────────────────────────────────────────────────

def historial_por_cliente(id_cliente):
    """
    Devuelve toda la info de un cliente: datos básicos y, por cada pedido,
    el técnico asignado (nombre), cobros y repuestos asociados.

    Recibe: id_cliente (int).
    Devuelve: dict con claves 'cliente' y 'pedidos', o None si el cliente no existe.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    cliente = buscar_por_id(clientes, "id_cliente", id_cliente)
    if cliente is None:
        return None

    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    cobros = cargar_datos(ARCHIVO_COBROS)
    repuestos = cargar_datos(ARCHIVO_REPUESTOS)

    pedidos_cliente = [p for p in pedidos if p["id_cliente"] == id_cliente]

    historial_pedidos = []
    for pedido in pedidos_cliente:
        tecnico = buscar_por_id(tecnicos, "id_tecnico", pedido["id_tecnico"])
        nombre_tecnico = tecnico["nombre"] if tecnico else "Sin asignar"

        cobros_pedido = [
            {
                "monto": c["monto"],
                "forma_pago": c["forma_pago"],
                "estado": c["estado"],
                "fecha": c["fecha"]
            }
            for c in cobros if c["id_pedido"] == pedido["id_pedido"]
        ]

        repuestos_pedido = [
            {
                "descripcion": r["descripcion"],
                "estado": r["estado"],
                "precio": r["precio"]
            }
            for r in repuestos if r["id_pedido"] == pedido["id_pedido"]
        ]

        historial_pedidos.append({
            "id_pedido": pedido["id_pedido"],
            "fecha": pedido["fecha"],
            "descripcion": pedido["descripcion"],
            "urgente": pedido["urgente"],
            "estado": pedido["estado"],
            "precio": pedido["precio"],
            "tecnico": nombre_tecnico,
            "cobros": cobros_pedido,
            "repuestos": repuestos_pedido
        })

    return {"cliente": cliente, "pedidos": historial_pedidos}


def buscar_garantia(id_cliente, texto):
    """
    Busca pedidos de un cliente cuya descripción contenga el texto dado
    (sin distinguir mayúsculas/minúsculas).

    Recibe: id_cliente (int), texto (str).
    Devuelve: lista de pedidos coincidentes con info completa, o None si el cliente no existe.
    """
    historial = historial_por_cliente(id_cliente)
    if historial is None:
        return None

    texto_lower = texto.lower()
    return [p for p in historial["pedidos"] if texto_lower in p["descripcion"].lower()]


# ── Menú de historial ─────────────────────────────────────────────────────────

def menu_historial():
    while True:
        print("\n=== HISTORIAL ===")
        print("1. Ver historial completo de un cliente")
        print("2. Buscar trabajo por garantía")
        print("0. Volver al menú principal")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            _ver_historial()
        elif opcion == "2":
            _buscar_garantia()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


def _ver_historial():
    print("\n--- Historial de cliente ---")
    id_cliente = pedir_entero("ID del cliente: ")
    historial = historial_por_cliente(id_cliente)

    if historial is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return

    cliente = historial["cliente"]
    pedidos = historial["pedidos"]

    print(f"\n{'─'*50}")
    print(f"  Cliente: {cliente['nombre']}  [{cliente['tipo']}]")
    print(f"  Dirección: {cliente['direccion']}  |  Tel: {cliente['telefono']}")
    print(f"{'─'*50}")

    if not pedidos:
        print("  Este cliente no tiene pedidos registrados.")
        return

    for p in pedidos:
        urgente = " [URGENTE]" if p["urgente"] else ""
        precio = f"${p['precio']}" if p["precio"] is not None else "sin precio"
        print(f"\n  Pedido #{p['id_pedido']} — {p['fecha']}{urgente}")
        print(f"  Trabajo:  {p['descripcion']}")
        print(f"  Estado:   {p['estado']}  |  Precio: {precio}")
        print(f"  Técnico:  {p['tecnico']}")

        if p["cobros"]:
            print("  Cobros:")
            for c in p["cobros"]:
                fecha = c["fecha"] or "sin fecha"
                print(f"    · ${c['monto']} — {c['forma_pago']} — {c['estado']} — {fecha}")
        else:
            print("  Cobros:   ninguno registrado")

        if p["repuestos"]:
            print("  Repuestos:")
            for r in p["repuestos"]:
                precio_r = f"${r['precio']}" if r["precio"] is not None else "sin precio"
                print(f"    · {r['descripcion']} — {r['estado']} — {precio_r}")
        else:
            print("  Repuestos: ninguno registrado")

    print(f"\n{'─'*50}")


def _buscar_garantia():
    print("\n--- Buscar trabajo por garantía ---")
    id_cliente = pedir_entero("ID del cliente: ")
    texto = pedir_texto("Palabra clave a buscar: ")

    resultado = buscar_garantia(id_cliente, texto)

    if resultado is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return

    if not resultado:
        print(f"No se encontraron trabajos que contengan '{texto}'.")
        return

    historial = historial_por_cliente(id_cliente)
    cliente = historial["cliente"]
    print(f"\nResultados para '{texto}' en el historial de {cliente['nombre']}:")

    for p in resultado:
        urgente = " [URGENTE]" if p["urgente"] else ""
        precio = f"${p['precio']}" if p["precio"] is not None else "sin precio"
        print(f"\n  Pedido #{p['id_pedido']} — {p['fecha']}{urgente}")
        print(f"  Trabajo:  {p['descripcion']}")
        print(f"  Estado:   {p['estado']}  |  Precio: {precio}")
        print(f"  Técnico:  {p['tecnico']}")

        if p["cobros"]:
            print("  Cobros:")
            for c in p["cobros"]:
                fecha = c["fecha"] or "sin fecha"
                print(f"    · ${c['monto']} — {c['forma_pago']} — {c['estado']} — {fecha}")

        if p["repuestos"]:
            print("  Repuestos:")
            for r in p["repuestos"]:
                precio_r = f"${r['precio']}" if r["precio"] is not None else "sin precio"
                print(f"    · {r['descripcion']} — {r['estado']} — {precio_r}")
