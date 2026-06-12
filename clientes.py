"""
clientes.py — Alta, baja, modificación y consulta de clientes del sistema Oli.

Funciones: crear_cliente, listar_clientes, buscar_cliente_por_id,
           modificar_cliente, eliminar_cliente.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    ARCHIVO_CLIENTES, ARCHIVO_PEDIDOS, TIPOS_CLIENTE
)


def crear_cliente(datos):
    """
    Agrega un cliente nuevo a la lista.

    Recibe: datos (dict) con nombre, direccion, telefono, tipo.
    Devuelve: el dict del cliente creado, o None si el tipo es inválido.
    """
    if datos.get("tipo") not in TIPOS_CLIENTE:
        print(f"Tipo inválido. Debe ser uno de: {TIPOS_CLIENTE}")
        return None

    clientes = cargar_datos(ARCHIVO_CLIENTES)
    cliente = {
        "id_cliente": generar_id(clientes, "id_cliente"),
        "nombre": datos["nombre"],
        "direccion": datos["direccion"],
        "telefono": datos["telefono"],
        "tipo": datos["tipo"]
    }
    clientes.append(cliente)
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return cliente


def listar_clientes():
    """
    Devuelve todos los clientes.

    Recibe: nada.
    Devuelve: lista de dicts; [] si no hay clientes.
    """
    return cargar_datos(ARCHIVO_CLIENTES)


def buscar_cliente_por_id(id_cliente):
    """
    Busca un cliente por su ID.

    Recibe: id_cliente (int).
    Devuelve: el dict del cliente, o None si no existe.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    return buscar_por_id(clientes, "id_cliente", id_cliente)


def modificar_cliente(id_cliente, nuevos_datos):
    """
    Actualiza los campos de un cliente existente.

    Recibe: id_cliente (int), nuevos_datos (dict) con los campos a modificar.
    Devuelve: el dict actualizado, o None si el cliente no existe o el tipo es inválido.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    cliente = buscar_por_id(clientes, "id_cliente", id_cliente)

    if cliente is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return None

    if "tipo" in nuevos_datos and nuevos_datos["tipo"] not in TIPOS_CLIENTE:
        print(f"Tipo inválido. Debe ser uno de: {TIPOS_CLIENTE}")
        return None

    cliente.update(nuevos_datos)
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return cliente


def eliminar_cliente(id_cliente):
    """
    Elimina un cliente si no tiene pedidos asociados.

    Recibe: id_cliente (int).
    Devuelve: True si se eliminó, False si no existe o tiene pedidos.
    """
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    cliente = buscar_por_id(clientes, "id_cliente", id_cliente)

    if cliente is None:
        print(f"No existe un cliente con ID {id_cliente}.")
        return False

    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    tiene_pedidos = any(p["id_cliente"] == id_cliente for p in pedidos)
    if tiene_pedidos:
        print(f"No se puede eliminar a {cliente['nombre']} porque tiene pedidos asociados.")
        return False

    clientes = [c for c in clientes if c["id_cliente"] != id_cliente]
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return True
