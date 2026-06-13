"""
tecnicos.py — Gestión de técnicos del sistema Oli.

Funciones de datos: crear_tecnico, listar_tecnicos, listar_disponibles,
                    listar_por_especialidad, buscar_tecnico_por_id,
                    cambiar_estado_tecnico, eliminar_tecnico.
Menú:              menu_tecnicos.
"""

from utils import (
    cargar_datos, guardar_datos, generar_id, buscar_por_id,
    pedir_texto, pedir_entero, pedir_opcion, pedir_confirmacion,
    ARCHIVO_TECNICOS, ARCHIVO_PEDIDOS,
    ESPECIALIDADES, ESTADOS_TECNICO
)

# Solo "cobrado" es estado final — "terminado" todavía tiene deuda pendiente.
_ESTADOS_ACTIVOS = ["pendiente", "asignado", "en_curso", "terminado"]


# ── Funciones de datos ────────────────────────────────────────────────────────

def crear_tecnico(datos):
    """
    Agrega un técnico nuevo a la lista.

    Recibe: datos (dict) con nombre, especialidad.
            estado es opcional; si no viene, arranca como "disponible".
    Devuelve: el dict del técnico creado, o None si la especialidad es inválida.
    """
    if datos.get("especialidad") not in ESPECIALIDADES:
        print(f"Especialidad inválida. Debe ser una de: {ESPECIALIDADES}")
        return None

    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    tecnico = {
        "id_tecnico": generar_id(tecnicos, "id_tecnico"),
        "nombre": datos["nombre"],
        "especialidad": datos["especialidad"],
        "estado": datos.get("estado", "disponible")
    }
    tecnicos.append(tecnico)
    guardar_datos(ARCHIVO_TECNICOS, tecnicos)
    return tecnico


def listar_tecnicos():
    """
    Devuelve todos los técnicos.

    Recibe: nada.
    Devuelve: lista de dicts; [] si no hay técnicos.
    """
    return cargar_datos(ARCHIVO_TECNICOS)


def listar_disponibles():
    """
    Devuelve solo los técnicos con estado "disponible".

    Recibe: nada.
    Devuelve: lista de dicts.
    """
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    return list(filter(lambda t: t["estado"] == "disponible", tecnicos))


def listar_por_especialidad(especialidad):
    """
    Devuelve los técnicos que tienen la especialidad indicada.

    Recibe: especialidad (str).
    Devuelve: lista de dicts, o None si la especialidad es inválida.
    """
    if especialidad not in ESPECIALIDADES:
        print(f"Especialidad inválida. Debe ser una de: {ESPECIALIDADES}")
        return None

    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    return list(filter(lambda t: t["especialidad"] == especialidad, tecnicos))


def buscar_tecnico_por_id(id_tecnico):
    """
    Busca un técnico por su ID.

    Recibe: id_tecnico (int).
    Devuelve: el dict del técnico, o None si no existe.
    """
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    return buscar_por_id(tecnicos, "id_tecnico", id_tecnico)


def cambiar_estado_tecnico(id_tecnico, nuevo_estado):
    """
    Cambia el estado de un técnico (disponible / ocupado).

    Recibe: id_tecnico (int), nuevo_estado (str).
    Devuelve: el dict actualizado, o None si no existe o el estado es inválido.
    """
    if nuevo_estado not in ESTADOS_TECNICO:
        print(f"Estado inválido. Debe ser uno de: {ESTADOS_TECNICO}")
        return None

    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    tecnico = buscar_por_id(tecnicos, "id_tecnico", id_tecnico)

    if tecnico is None:
        print(f"No existe un técnico con ID {id_tecnico}.")
        return None

    tecnico["estado"] = nuevo_estado
    guardar_datos(ARCHIVO_TECNICOS, tecnicos)
    return tecnico


def eliminar_tecnico(id_tecnico):
    """
    Elimina un técnico si no tiene pedidos activos (cualquier estado distinto de "cobrado").

    Recibe: id_tecnico (int).
    Devuelve: True si se eliminó, False si no existe o tiene pedidos activos.
    """
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    tecnico = buscar_por_id(tecnicos, "id_tecnico", id_tecnico)

    if tecnico is None:
        print(f"No existe un técnico con ID {id_tecnico}.")
        return False

    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    if any(p["id_tecnico"] == id_tecnico and p["estado"] in _ESTADOS_ACTIVOS for p in pedidos):
        print(f"No se puede eliminar a {tecnico['nombre']} porque tiene pedidos activos.")
        return False

    tecnicos = [t for t in tecnicos if t["id_tecnico"] != id_tecnico]
    guardar_datos(ARCHIVO_TECNICOS, tecnicos)
    return True


# ── Menú de técnicos ──────────────────────────────────────────────────────────

def menu_tecnicos():
    while True:
        print("\n=== TÉCNICOS ===")
        print("1. Listar todos los técnicos")
        print("2. Ver disponibles")
        print("3. Filtrar por especialidad")
        print("4. Buscar técnico por ID")
        print("5. Cambiar estado (disponible / ocupado)")
        print("6. Agregar técnico")
        print("7. Eliminar técnico")
        print("0. Volver al menú principal")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            _listar_tecnicos()
        elif opcion == "2":
            _listar_disponibles()
        elif opcion == "3":
            _filtrar_por_especialidad()
        elif opcion == "4":
            _buscar_tecnico()
        elif opcion == "5":
            _cambiar_estado_tecnico()
        elif opcion == "6":
            _agregar_tecnico()
        elif opcion == "7":
            _eliminar_tecnico()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


def _listar_tecnicos():
    print("\n--- Técnicos registrados ---")
    tecnicos = listar_tecnicos()
    if not tecnicos:
        print("No hay técnicos cargados.")
        return
    for t in tecnicos:
        print(f"  [{t['id_tecnico']}] {t['nombre']} — {t['especialidad']} — {t['estado']}")


def _listar_disponibles():
    print("\n--- Técnicos disponibles ---")
    tecnicos = listar_disponibles()
    if not tecnicos:
        print("No hay técnicos disponibles en este momento.")
        return
    for t in tecnicos:
        print(f"  [{t['id_tecnico']}] {t['nombre']} — {t['especialidad']}")


def _filtrar_por_especialidad():
    print("\n--- Filtrar por especialidad ---")
    print("Especialidades disponibles:")
    especialidad = pedir_opcion("Elegí la especialidad: ", ESPECIALIDADES)
    tecnicos = listar_por_especialidad(especialidad)
    if not tecnicos:
        print(f"No hay técnicos con especialidad '{especialidad}'.")
        return
    for t in tecnicos:
        print(f"  [{t['id_tecnico']}] {t['nombre']} — {t['estado']}")


def _buscar_tecnico():
    print("\n--- Buscar técnico ---")
    id_tecnico = pedir_entero("ID del técnico: ")
    tecnico = buscar_tecnico_por_id(id_tecnico)
    if tecnico is None:
        print(f"No existe un técnico con ID {id_tecnico}.")
    else:
        print(f"\n  ID:           {tecnico['id_tecnico']}")
        print(f"  Nombre:       {tecnico['nombre']}")
        print(f"  Especialidad: {tecnico['especialidad']}")
        print(f"  Estado:       {tecnico['estado']}")


def _cambiar_estado_tecnico():
    print("\n--- Cambiar estado de técnico ---")
    id_tecnico = pedir_entero("ID del técnico: ")
    tecnico = buscar_tecnico_por_id(id_tecnico)
    if tecnico is None:
        print(f"No existe un técnico con ID {id_tecnico}.")
        return
    print(f"Estado actual de {tecnico['nombre']}: {tecnico['estado']}")
    print("Nuevo estado:")
    nuevo_estado = pedir_opcion("Elegí el estado: ", ESTADOS_TECNICO)
    cambiar_estado_tecnico(id_tecnico, nuevo_estado)
    print(f"Estado de {tecnico['nombre']} actualizado a '{nuevo_estado}'.")


def _agregar_tecnico():
    print("\n--- Agregar técnico ---")
    nombre = pedir_texto("Nombre del técnico: ")
    print("Especialidad:")
    especialidad = pedir_opcion("Elegí la especialidad: ", ESPECIALIDADES)
    tecnico = crear_tecnico({"nombre": nombre, "especialidad": especialidad})
    if tecnico:
        print(f"\nTécnico '{tecnico['nombre']}' agregado con ID {tecnico['id_tecnico']}.")


def _eliminar_tecnico():
    print("\n--- Eliminar técnico ---")
    id_tecnico = pedir_entero("ID del técnico a eliminar: ")
    tecnico = buscar_tecnico_por_id(id_tecnico)
    if tecnico is None:
        print(f"No existe un técnico con ID {id_tecnico}.")
        return
    if not pedir_confirmacion(f"¿Confirmás eliminar a '{tecnico['nombre']}'?"):
        print("Cancelado.")
        return
    eliminar_tecnico(id_tecnico)
