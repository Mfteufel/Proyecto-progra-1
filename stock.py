"""
stock.py — Gestión del estante de insumos del sistema Oli.

Funciones de datos: agregar_insumo, listar_stock, listar_stock_bajo,
                    reponer_stock, usar_insumo.
Menú:              menu_stock.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, pedir_confirmacion,
    ARCHIVO_STOCK, ARCHIVO_PEDIDOS, ARCHIVO_TECNICOS
)
from repuestos import registrar_repuesto


# ── Funciones de datos ────────────────────────────────────────────────────────

def agregar_insumo(datos):
    """
    Agrega un insumo nuevo al estante.

    Recibe: datos (dict) con nombre, unidad, cantidad, cantidad_minima.
    Devuelve: el dict del insumo creado.
    """
    stock = cargar_datos(ARCHIVO_STOCK)
    insumo = {
        "id_insumo": generar_id(stock, "id_insumo"),
        "nombre": datos["nombre"],
        "unidad": datos["unidad"],
        "cantidad": datos["cantidad"],
        "cantidad_minima": datos["cantidad_minima"]
    }
    stock.append(insumo)
    guardar_datos(ARCHIVO_STOCK, stock)
    return insumo


def listar_stock():
    """
    Devuelve todos los insumos del estante.

    Recibe: nada.
    Devuelve: lista de dicts.
    """
    return cargar_datos(ARCHIVO_STOCK)


def listar_stock_bajo():
    """
    Devuelve los insumos cuya cantidad está por debajo del mínimo.

    Recibe: nada.
    Devuelve: lista de dicts.
    """
    stock = cargar_datos(ARCHIVO_STOCK)
    return list(filter(lambda i: i["cantidad"] <= i["cantidad_minima"], stock))


def reponer_stock(id_insumo, cantidad):
    """
    Suma cantidad al stock de un insumo (Oli volvió del mayorista).

    Recibe: id_insumo (int), cantidad (int).
    Devuelve: el dict actualizado, o None si el insumo no existe o la cantidad es inválida.
    """
    if cantidad <= 0:
        raise ValueError(
            "La cantidad a reponer debe ser mayor a cero."
        )

    stock = cargar_datos(ARCHIVO_STOCK)
    insumo = buscar_por_id(stock, "id_insumo", id_insumo)

    if insumo is None:
        raise ValueError(
            f"No existe un insumo con ID {id_insumo}."
        )

    insumo["cantidad"] += cantidad
    guardar_datos(ARCHIVO_STOCK, stock)

    return insumo


def usar_insumo(id_insumo, cantidad, id_pedido, id_tecnico=None):
    """
    Descuenta cantidad del estante y registra el repuesto en el pedido.

    Recibe: id_insumo (int), cantidad (int), id_pedido (int), id_tecnico (int, opcional).
    Devuelve: el dict del insumo actualizado, o None si hay error.
    """
    if cantidad <= 0:
        print("La cantidad debe ser mayor a cero.")
        return None

    stock = cargar_datos(ARCHIVO_STOCK)
    insumo = buscar_por_id(stock, "id_insumo", id_insumo)

    if insumo is None:
        print(f"No existe un insumo con ID {id_insumo}.")
        return None

    if insumo["cantidad"] < cantidad:
        print(f"Stock insuficiente. Hay {insumo['cantidad']} {insumo['unidad']} de '{insumo['nombre']}'.")
        return None

    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    if buscar_por_id(pedidos, "id_pedido", id_pedido) is None:
        print(f"No existe un pedido con ID {id_pedido}.")
        return None

    # Descontar del estante
    insumo["cantidad"] -= cantidad
    guardar_datos(ARCHIVO_STOCK, stock)

    # Registrar en el pedido
    descripcion = f"{cantidad} {insumo['unidad']} de {insumo['nombre']}"
    registrar_repuesto({
        "id_pedido": id_pedido,
        "id_tecnico": id_tecnico,
        "descripcion": descripcion
    })

    # Avisar si quedó por debajo del mínimo
    if insumo["cantidad"] <= insumo["cantidad_minima"]:
        print(f"  ⚠ Quedan solo {insumo['cantidad']} {insumo['unidad']} de '{insumo['nombre']}'. ¡Hay que reponer!")

    return insumo


# ── Menú de stock ─────────────────────────────────────────────────────────────

def menu_stock():
    while True:
        try:
            print("\n=== STOCK DEL ESTANTE ===")
            print("1. Ver todo el stock")
            print("2. Ver insumos bajos")
            print("3. Usar insumo en un pedido")
            print("4. Reponer stock")
            print("5. Agregar insumo nuevo")
            print("0. Volver al menú principal")

            opcion = input("\nElegí una opción: ").strip()

            if opcion == "1":
                _ver_stock()
            elif opcion == "2":
                _ver_stock_bajo()
            elif opcion == "3":
                _usar_insumo()
            elif opcion == "4":
                _reponer_stock()
            elif opcion == "5":
                _agregar_insumo()
            elif opcion == "0":
                break
            else:
                raise ValueError("Opción inválida.")

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")
            print(f"Tipo de excepción: {type(e).__name__}")

        finally:
            print("Volviendo al menú...")

def _formato_insumo(i, alerta=False):
    aviso = " ⚠ REPONER" if alerta else ""
    return (f"  [{i['id_insumo']}] {i['nombre']} — "
            f"{i['cantidad']} {i['unidad']} (mínimo: {i['cantidad_minima']}){aviso}")


def _ver_stock():
    print("\n--- Stock del estante ---")
    stock = listar_stock()
    if not stock:
        print("No hay insumos cargados.")
        return
    for i in stock:
        bajo = i["cantidad"] <= i["cantidad_minima"]
        print(_formato_insumo(i, alerta=bajo))


def _ver_stock_bajo():
    print("\n--- Insumos a reponer ---")
    bajos = listar_stock_bajo()
    if not bajos:
        print("Todo el stock está bien. No hay nada que reponer.")
        return
    print("Estos insumos llegaron al mínimo:")
    for i in bajos:
        print(_formato_insumo(i, alerta=True))


def _usar_insumo():
    print("\n--- Usar insumo del estante ---")
    _ver_stock()
    id_insumo = pedir_entero("\nID del insumo a usar: ")
    cantidad = pedir_entero("Cantidad: ")
    id_pedido = pedir_entero("ID del pedido: ")
    id_tecnico = pedir_entero("ID del técnico (0 si no se sabe): ")
    if id_tecnico == 0:
        id_tecnico = None

    insumo = usar_insumo(id_insumo, cantidad, id_pedido, id_tecnico)
    if insumo:
        print(f"Descontado del estante. Stock actual de '{insumo['nombre']}': {insumo['cantidad']} {insumo['unidad']}.")


def _reponer_stock():
    try:
        print("\n--- Reponer stock ---")

        _ver_stock()

        id_insumo = pedir_entero("\nID del insumo a reponer: ")
        cantidad = pedir_entero("Cantidad a agregar: ")

        insumo = reponer_stock(id_insumo, cantidad)

        print(
            f"Stock de '{insumo['nombre']}' actualizado: "
            f"{insumo['cantidad']} {insumo['unidad']}."
        )

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        print("Operación finalizada.")

def _agregar_insumo():
    try:
        print("\n--- Agregar insumo nuevo ---")

        nombre = pedir_texto("Nombre del insumo: ")
        unidad = pedir_texto("Unidad (rollos, unidades, bolsas, etc.): ")
        cantidad = pedir_entero("Cantidad inicial: ")
        cantidad_minima = pedir_entero("Cantidad mínima antes de avisar: ")

        if nombre.strip() == "":
            raise ValueError(
                "El nombre del insumo no puede estar vacío."
            )

        if unidad.strip() == "":
            raise ValueError(
                "La unidad no puede estar vacía."
            )

        if cantidad < 0:
            raise ValueError(
                "La cantidad inicial no puede ser negativa."
            )

        if cantidad_minima < 0:
            raise ValueError(
                "La cantidad mínima no puede ser negativa."
            )

        insumo = agregar_insumo({
            "nombre": nombre,
            "unidad": unidad,
            "cantidad": cantidad,
            "cantidad_minima": cantidad_minima
        })

        print(
            f"\nInsumo '{insumo['nombre']}' agregado "
            f"con ID {insumo['id_insumo']}."
        )

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")
        print(f"Tipo de excepción: {type(e).__name__}")

    finally:
        print("Operación finalizada.")