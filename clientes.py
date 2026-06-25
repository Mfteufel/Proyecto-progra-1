"""
clientes.py — Alta, baja, modificación, consulta y menú de clientes del sistema Oli.

Funciones de datos: crear_cliente, listar_clientes, buscar_cliente_por_id,
                    modificar_cliente, eliminar_cliente.
Menú:              menu_clientes.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, validar_telefono, pedir_opcion, pedir_confirmacion,
    ARCHIVO_CLIENTES, ARCHIVO_PEDIDOS, TIPOS_CLIENTE
)



# ── Funciones de datos ────────────────────────────────────────────────────────

def crear_cliente(datos):
    """
    Agrega un cliente nuevo a la lista.

    Recibe: datos (dict) con nombre, direccion, telefono, tipo.
    Devuelve: el dict del cliente creado, o None si el tipo es inválido.
    """
    if datos.get("tipo") not in TIPOS_CLIENTE:
        raise ValueError(
            f"Tipo inválido. Debe ser uno de: {TIPOS_CLIENTE}"
        )

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
    if any(p["id_cliente"] == id_cliente for p in pedidos):
        print(f"No se puede eliminar a {cliente['nombre']} porque tiene pedidos asociados.")
        return False

    clientes = [c for c in clientes if c["id_cliente"] != id_cliente]
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return True


# ── Menú de clientes ──────────────────────────────────────────────────────────

def menu_clientes():
    while True:
        try:
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
                raise ValueError(
                    "Opción inválida. Elegí una opción del menú."
                )

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")
            print(f"Tipo de excepción: {type(e).__name__}")

        finally:
            print("Volviendo al menú de clientes...")

def _cargar_cliente():
    try:
        print("\n--- Cargar cliente nuevo ---")

        nombre = pedir_texto("Nombre del cliente: ")
        direccion = pedir_texto("Dirección: ")
        
        while True:
            telefono = pedir_texto("Teléfono: ")
            if validar_telefono(telefono):
                break
            print("Teléfono inválido. Debe contener entre 8 y 15 dígitos.")

        print("Tipo de cliente:")
        tipo = pedir_opcion("Elegí el tipo: ", TIPOS_CLIENTE)

        cliente = crear_cliente({
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "tipo": tipo
        })

        print(
            f"\nCliente '{cliente['nombre']}' "
            f"cargado con ID {cliente['id_cliente']}."
        )

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        print("Operación finalizada.")

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

    while True:
        telefono = input(f"Teléfono [{cliente['telefono']}]: ").strip()
        if telefono == "":
            break

        if validar_telefono(telefono):
            nuevos["telefono"] = telefono
            break

        print("Teléfono inválido. Debe contener entre 8 y 15 dígitos.")

    if pedir_confirmacion(f"¿Querés cambiar el tipo? (actual: {cliente['tipo']})"):
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
