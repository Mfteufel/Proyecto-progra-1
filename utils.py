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
