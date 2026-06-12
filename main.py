"""
main.py — Menú principal del sistema Oli.

Punto de entrada del sistema. Integra todos los módulos e implementa
los menús de navegación por consola.
"""

from clientes import (
    crear_cliente, listar_clientes, buscar_cliente_por_id,
    modificar_cliente, eliminar_cliente
)
from utils import TIPOS_CLIENTE


# ── Helpers de input ──────────────────────────────────────────────────────────

def pedir_texto(mensaje):
    """Pide un string no vacío, repite hasta que el usuario ingrese algo."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  Este campo no puede estar vacío. Intentá de nuevo.")


def pedir_entero(mensaje):
    """Pide un número entero, repite si el usuario ingresa algo inválido."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("  Tenés que ingresar un número entero.")


def pedir_opcion(mensaje, opciones):
    """
    Muestra opciones numeradas y devuelve el valor elegido.

    Recibe: mensaje (str), opciones (list).
    Devuelve: el valor de la lista correspondiente a la elección.
    """
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")
    while True:
        try:
            eleccion = int(input(mensaje).strip())
            if 1 <= eleccion <= len(opciones):
                return opciones[eleccion - 1]
            print(f"  Elegí un número entre 1 y {len(opciones)}.")
        except ValueError:
            print("  Tenés que ingresar un número.")


def pedir_confirmacion(mensaje):
    """Pide s/n y devuelve True si el usuario confirma."""
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("  Ingresá 's' para sí o 'n' para no.")


# ── Submenú de clientes ───────────────────────────────────────────────────────

def menu_clientes():
    while True:
        print("\n=== CLIENTES ===")
        print("1. Cargar cliente nuevo")
        print("2. Listar todos los clientes")
        print("3. Buscar cliente por ID")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("0. Volver al menú principal")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            _cargar_cliente()
        elif opcion == "2":
            _listar_clientes()
        elif opcion == "3":
            _buscar_cliente()
        elif opcion == "4":
            _modificar_cliente()
        elif opcion == "5":
            _eliminar_cliente()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


def _cargar_cliente():
    print("\n--- Cargar cliente nuevo ---")
    nombre = pedir_texto("Nombre del cliente: ")
    direccion = pedir_texto("Dirección: ")
    telefono = pedir_texto("Teléfono: ")
    print("Tipo de cliente:")
    tipo = pedir_opcion("Elegí el tipo: ", TIPOS_CLIENTE)

    cliente = crear_cliente({
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "tipo": tipo
    })
    if cliente:
        print(f"\nCliente '{cliente['nombre']}' cargado con ID {cliente['id_cliente']}.")


def _listar_clientes():
    print("\n--- Clientes registrados ---")
    clientes = listar_clientes()
    if not clientes:
        print("No hay clientes cargados todavía.")
        return
    for c in clientes:
        print(f"  [{c['id_cliente']}] {c['nombre']} — {c['direccion']} — Tel: {c['telefono']} — {c['tipo']}")


def _buscar_cliente():
    print("\n--- Buscar cliente ---")
    id_cliente = pedir_entero("ID del cliente: ")
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente is None:
        print(f"No existe un cliente con ID {id_cliente}.")
    else:
        print(f"\n  ID:        {cliente['id_cliente']}")
        print(f"  Nombre:    {cliente['nombre']}")
        print(f"  Dirección: {cliente['direccion']}")
        print(f"  Teléfono:  {cliente['telefono']}")
        print(f"  Tipo:      {cliente['tipo']}")


def _modificar_cliente():
    print("\n--- Modificar cliente ---")
    id_cliente = pedir_entero("ID del cliente a modificar: ")
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return

    print(f"Modificando a '{cliente['nombre']}'. Dejá vacío para no cambiar el campo.")

    nuevos = {}
    nombre = input(f"Nombre [{cliente['nombre']}]: ").strip()
    if nombre:
        nuevos["nombre"] = nombre

    direccion = input(f"Dirección [{cliente['direccion']}]: ").strip()
    if direccion:
        nuevos["direccion"] = direccion

    telefono = input(f"Teléfono [{cliente['telefono']}]: ").strip()
    if telefono:
        nuevos["telefono"] = telefono

    cambiar_tipo = pedir_confirmacion(f"¿Querés cambiar el tipo? (actual: {cliente['tipo']})")
    if cambiar_tipo:
        print("Tipo de cliente:")
        nuevos["tipo"] = pedir_opcion("Elegí el tipo: ", TIPOS_CLIENTE)

    if not nuevos:
        print("No cambiaste nada.")
        return

    modificar_cliente(id_cliente, nuevos)
    print("Cliente actualizado.")


def _eliminar_cliente():
    print("\n--- Eliminar cliente ---")
    id_cliente = pedir_entero("ID del cliente a eliminar: ")
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return

    if not pedir_confirmacion(f"¿Confirmás eliminar a '{cliente['nombre']}'?"):
        print("Cancelado.")
        return

    eliminar_cliente(id_cliente)


# ── Menú principal ────────────────────────────────────────────────────────────

def main():
    print("\n¡Bienvenido al Sistema Oli!")

    while True:
        print("\n=== SISTEMA OLI ===")
        print("1. Clientes")
        print("2. Técnicos        (próximamente)")
        print("3. Pedidos         (próximamente)")
        print("4. Cobros          (próximamente)")
        print("5. Historial       (próximamente)")
        print("6. Repuestos       (próximamente)")
        print("0. Salir")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion in ("2", "3", "4", "5", "6"):
            print("Ese módulo todavía no está disponible.")
        elif opcion == "0":
            print("\nHasta luego.")
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


if __name__ == "__main__":
    main()
