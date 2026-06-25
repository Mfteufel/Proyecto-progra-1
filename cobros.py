"""
cobros.py — Gestión de cobros del sistema Oli.

Funciones de datos: registrar_cobro, listar_cobros_por_pedido,
                    calcular_deuda_pedido, listar_deudores, marcar_pago.
Menú:              menu_cobros.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, pedir_opcion, pedir_confirmacion,
    ARCHIVO_COBROS, ARCHIVO_PEDIDOS, ARCHIVO_CLIENTES,
    FORMAS_PAGO, ESTADOS_COBRO
)
from pedidos import cambiar_estado_pedido


# ── Funciones de datos ────────────────────────────────────────────────────────

def registrar_cobro(datos):
    """
    Registra un cobro para un pedido.
    Si el pedido no tiene precio cargado, lo pide y lo guarda.

    Recibe: datos (dict) con id_pedido, monto, forma_pago, recibido_por, fecha.
    Devuelve: el dict del cobro creado, o None si el pedido no existe o su estado no lo permite.
    """
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    pedido = buscar_por_id(pedidos, "id_pedido", datos["id_pedido"])

    if pedido is None:
        print(f"No existe un pedido con ID {datos['id_pedido']}.")
        return None

    if pedido["estado"] not in ("terminado", "cobrado"):
        print(f"El pedido está en '{pedido['estado']}'. Solo se puede cobrar si está en 'terminado' o 'cobrado'.")
        return None

    if datos.get("forma_pago") not in FORMAS_PAGO:
        print(f"Forma de pago inválida. Debe ser una de: {FORMAS_PAGO}")
        return None

    cobros = cargar_datos(ARCHIVO_COBROS)
    cobro = {
        "id_cobro": generar_id(cobros, "id_cobro"),
        "id_pedido": datos["id_pedido"],
        "monto": datos["monto"],
        "forma_pago": datos["forma_pago"],
        "recibido_por": datos["recibido_por"],
        "estado": "pendiente",
        "fecha": datos.get("fecha", None)
    }
    cobros.append(cobro)
    guardar_datos(ARCHIVO_COBROS, cobros)
    return cobro


def listar_cobros_por_pedido(id_pedido):
    """
    Devuelve todos los cobros de un pedido.

    Recibe: id_pedido (int).
    Devuelve: lista de dicts.
    """
    cobros = cargar_datos(ARCHIVO_COBROS)
    return list(filter(lambda c: c["id_pedido"] == id_pedido, cobros))


def calcular_deuda_pedido(id_pedido):
    """
    Suma los montos de los cobros pendientes de un pedido.

    Recibe: id_pedido (int).
    Devuelve: float con el total adeudado.
    """
    cobros = listar_cobros_por_pedido(id_pedido)
    pendientes = filter(lambda c: c["estado"] == "pendiente", cobros)
    return sum(map(lambda c: c["monto"], pendientes))


def listar_deudores():
    """
    Devuelve clientes con al menos un cobro pendiente.

    Recibe: nada.
    Devuelve: lista de dicts con id_cliente, nombre y deuda_total.
    """
    cobros = cargar_datos(ARCHIVO_COBROS)
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    clientes = cargar_datos(ARCHIVO_CLIENTES)

    # Acumular deuda por cliente
    deuda_por_cliente = {}
    for cobro in cobros:
        if cobro["estado"] != "pendiente":
            continue
        pedido = buscar_por_id(pedidos, "id_pedido", cobro["id_pedido"])
        if pedido is None:
            continue
        id_cliente = pedido["id_cliente"]
        deuda_por_cliente[id_cliente] = deuda_por_cliente.get(id_cliente, 0) + cobro["monto"]

    resultado = []
    for id_cliente, deuda in deuda_por_cliente.items():
        cliente = buscar_por_id(clientes, "id_cliente", id_cliente)
        nombre = cliente["nombre"] if cliente else f"Cliente {id_cliente}"
        resultado.append({"id_cliente": id_cliente, "nombre": nombre, "deuda_total": deuda})

    return resultado


def marcar_pago(id_cobro):
    """
    Marca un cobro como pagado.
    Si todos los cobros del pedido quedan pagados, avanza el pedido a 'cobrado'.

    Recibe: id_cobro (int).
    Devuelve: el dict del cobro actualizado, o None si no existe o ya estaba pagado.
    """
    cobros = cargar_datos(ARCHIVO_COBROS)
    cobro = buscar_por_id(cobros, "id_cobro", id_cobro)

    if cobro is None:
        print(f"No existe un cobro con ID {id_cobro}.")
        return None

    if cobro["estado"] == "pagado":
        print(f"El cobro {id_cobro} ya estaba marcado como pagado.")
        return None

    cobro["estado"] = "pagado"
    guardar_datos(ARCHIVO_COBROS, cobros)

    # Si todos los cobros del pedido están pagados, avanzar el pedido a "cobrado"
    id_pedido = cobro["id_pedido"]
    cobros_del_pedido = list(filter(lambda c: c["id_pedido"] == id_pedido, cobros))
    todos_pagados = all(c["estado"] == "pagado" for c in cobros_del_pedido)
    if todos_pagados:
        cambiar_estado_pedido(id_pedido, "cobrado")
        print(f"Todos los cobros del pedido #{id_pedido} están pagados. Pedido marcado como 'cobrado'.")

    return cobro


# ── Menú de cobros ────────────────────────────────────────────────────────────

def menu_cobros():
    while True:
        try:
            print("\n=== COBROS ===")
            print("1. Ver cobros de un pedido")
            print("2. Registrar cobro")
            print("3. Marcar cobro como pagado")
            print("4. Ver deuda de un pedido")
            print("5. Ver deudores")
            print("0. Volver al menú principal")

            opcion = input("\nElegí una opción: ").strip()

            if opcion == "1":
                _ver_cobros_pedido()

            elif opcion == "2":
                _registrar_cobro()

            elif opcion == "3":
                _marcar_pago()

            elif opcion == "4":
                _ver_deuda_pedido()

            elif opcion == "5":
                _ver_deudores()

            elif opcion == "0":
                break

            else:
                raise ValueError(
                    "Opción inválida. Elegí una opción del menú."
                )

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")
            print(f"Tipo de excepción: {type(e).__name__}")

        finally:
            print("Volviendo al menú de cobros...")

def _ver_cobros_pedido():
    print("\n--- Cobros de un pedido ---")
    id_pedido = pedir_entero("ID del pedido: ")
    cobros = listar_cobros_por_pedido(id_pedido)
    if not cobros:
        print(f"No hay cobros registrados para el pedido #{id_pedido}.")
        return
    for c in cobros:
        fecha = c["fecha"] or "sin fecha"
        print(f"  [{c['id_cobro']}] ${c['monto']} — {c['forma_pago']} — {c['estado']} — {fecha} — Recibido por: {c['recibido_por']}")
    deuda = calcular_deuda_pedido(id_pedido)
    if deuda > 0:
        print(f"  Deuda pendiente: ${deuda}")


def _registrar_cobro():
    from datetime import date

    try:
        print("\n--- Registrar cobro ---")

        id_pedido = pedir_entero("ID del pedido: ")

        # Mostrar precio del pedido y cargarlo si falta
        pedidos = cargar_datos(ARCHIVO_PEDIDOS)
        pedido = buscar_por_id(pedidos, "id_pedido", id_pedido)

        if pedido is None:
            raise ValueError(
                f"No existe un pedido con ID {id_pedido}."
            )

        if pedido["estado"] not in ("terminado", "cobrado"):
            raise ValueError(
                f"El pedido está en '{pedido['estado']}'. "
                "Solo se puede cobrar si está en 'terminado' o 'cobrado'."
            )

        if pedido["precio"] is None:
            print("El pedido no tiene precio cargado.")

            while True:
                try:
                    precio = float(
                        input("Ingresá el precio total del trabajo: $").strip()
                    )

                    if precio <= 0:
                        raise ValueError(
                            "El precio debe ser mayor a cero."
                        )

                    break

                except ValueError as e:
                    print(f"Error: {e}")

            pedido["precio"] = precio
            guardar_datos(ARCHIVO_PEDIDOS, pedidos)

            print(
                f"Precio ${precio} guardado en el pedido #{id_pedido}."
            )

        else:
            print(f"Precio del trabajo: ${pedido['precio']}")

        while True:
            try:
                monto = float(
                    input("Monto de este cobro: $").strip()
                )

                if monto <= 0:
                    raise ValueError(
                        "El monto debe ser mayor a cero."
                    )

                break

            except ValueError as e:
                print(f"Error: {e}")

        print("Forma de pago:")
        forma_pago = pedir_opcion(
            "Elegí la forma de pago: ",
            FORMAS_PAGO
        )

        recibido_por = pedir_texto("Recibido por: ")

        fecha = date.today().strftime("%d/%m/%Y")

        cobro = registrar_cobro({
            "id_pedido": id_pedido,
            "monto": monto,
            "forma_pago": forma_pago,
            "recibido_por": recibido_por,
            "fecha": fecha
        })

        if cobro:
            print(
                f"\nCobro #{cobro['id_cobro']} "
                f"registrado por ${monto}."
            )

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")
        print(f"Tipo de excepción: {type(e).__name__}")

    finally:
        print("Operación finalizada.")

def _marcar_pago():
    print("\n--- Marcar cobro como pagado ---")
    id_cobro = pedir_entero("ID del cobro: ")
    cobro = marcar_pago(id_cobro)
    if cobro is None:
        raise ValueError(
            f"No existe un cobro con ID {id_cobro}."
        )

    if cobro["estado"] == "pagado":
        raise ValueError(
            f"El cobro {id_cobro} ya estaba marcado como pagado."
        )

def _ver_deuda_pedido():
    print("\n--- Deuda de un pedido ---")
    id_pedido = pedir_entero("ID del pedido: ")
    deuda = calcular_deuda_pedido(id_pedido)
    if deuda == 0:
        print(f"El pedido #{id_pedido} no tiene deuda pendiente.")
    else:
        print(f"Deuda pendiente del pedido #{id_pedido}: ${deuda}")


def _ver_deudores():
    print("\n--- Clientes con deuda ---")
    deudores = listar_deudores()
    if not deudores:
        print("No hay clientes con deuda pendiente.")
        return
    for d in deudores:
        print(f"  [{d['id_cliente']}] {d['nombre']} — Deuda total: ${d['deuda_total']}")
