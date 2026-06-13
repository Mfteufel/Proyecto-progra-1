"""
utils.py — Funciones genéricas y constantes compartidas del sistema Oli.

Provee: constantes de configuración, lectura/escritura de archivos .json,
generación de IDs y búsqueda por ID. Todos los módulos importan desde acá.
"""

import json
import os

# ── Rutas de archivos ──────────────────────────────────────────────────────────
# Anclar al directorio donde está utils.py para que funcione desde cualquier lugar.

_BASE = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_CLIENTES  = os.path.join(_BASE, "datos", "clientes.json")
ARCHIVO_TECNICOS  = os.path.join(_BASE, "datos", "tecnicos.json")
ARCHIVO_PEDIDOS   = os.path.join(_BASE, "datos", "pedidos.json")
ARCHIVO_COBROS    = os.path.join(_BASE, "datos", "cobros.json")
ARCHIVO_REPUESTOS = os.path.join(_BASE, "datos", "repuestos.json")
ARCHIVO_STOCK     = os.path.join(_BASE, "datos", "stock.json")

# ── Valores válidos por campo ──────────────────────────────────────────────────

TIPOS_CLIENTE          = ["particular", "comercio"]
ESPECIALIDADES         = ["electrica", "aires", "multiuso"]
ESTADOS_PEDIDO         = ["pendiente", "asignado", "en_curso", "terminado", "cobrado"]
ESTADOS_TECNICO        = ["disponible", "ocupado"]
FORMAS_PAGO            = ["efectivo", "transferencia", "cuotas"]
ESTADOS_COBRO          = ["pagado", "pendiente"]
ESTADOS_REPUESTO       = ["solicitado", "comprado", "entregado", "instalado"]
ESTADOS_PEDIDO_ACTIVOS = ["pendiente", "asignado", "en_curso", "terminado"]


def cargar_datos(nombre_archivo):
    """
    Lee un archivo .json y devuelve una lista de diccionarios.

    Recibe: nombre_archivo (str) — ruta relativa al archivo.
    Devuelve: lista de dicts; [] si el archivo no existe o está corrupto.
    """
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def guardar_datos(nombre_archivo, lista):
    """
    Escribe una lista de diccionarios en el archivo .json, sobreescribiendo el contenido.

    Recibe: nombre_archivo (str), lista (list de dicts).
    Devuelve: None. Crea la carpeta 'datos/' si no existe.
    """
    carpeta = os.path.dirname(nombre_archivo)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def generar_id(lista, nombre_id):
    """
    Devuelve el próximo ID disponible para la lista dada.

    Recibe: lista (list de dicts), nombre_id (str) — nombre del campo PK.
    Devuelve: 1 si la lista está vacía; max(ids) + 1 si no.
    """
    if not lista:
        return 1
    return max(registro[nombre_id] for registro in lista) + 1


def buscar_por_id(lista, nombre_id, valor):
    """
    Busca el primer diccionario cuyo campo nombre_id sea igual a valor.

    Recibe: lista (list de dicts), nombre_id (str), valor (int o str).
    Devuelve: el dict encontrado, o None si no existe.
    """
    for registro in lista:
        if registro[nombre_id] == valor:
            return registro
    return None


# ── Helpers de input por consola ──────────────────────────────────────────────

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
