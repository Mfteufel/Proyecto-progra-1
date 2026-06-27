import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import generar_id, buscar_por_id, cargar_datos, guardar_datos

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_TEMP = os.path.join(_BASE, "datos", "test_temp.json")


# ── Tests de generar_id ────────────────────────────────────────────────────────

def test_generar_id_lista_vacia():
    resultado = generar_id([], "id_cliente")
    assert resultado == 1, f"Esperaba 1, obtuve {resultado}"


def test_generar_id_con_elementos():
    lista = [{"id_cliente": 1}, {"id_cliente": 5}, {"id_cliente": 3}]
    resultado = generar_id(lista, "id_cliente")
    assert resultado == 6, f"Esperaba 6, obtuve {resultado}"


def test_generar_id_distintos_campos():
    lista = [{"id_pedido": 10}, {"id_pedido": 20}]
    resultado = generar_id(lista, "id_pedido")
    assert resultado == 21, f"Esperaba 21, obtuve {resultado}"


# ── Tests de buscar_por_id ────────────────────────────────────────────────────

def test_buscar_por_id_existente():
    lista = [{"id_cliente": 1, "nombre": "Doña Rosa"}, {"id_cliente": 2, "nombre": "Kiosco Pepe"}]
    resultado = buscar_por_id(lista, "id_cliente", 2)
    assert resultado["nombre"] == "Kiosco Pepe", f"Nombre incorrecto: {resultado}"


def test_buscar_por_id_inexistente():
    lista = [{"id_cliente": 1}]
    resultado = buscar_por_id(lista, "id_cliente", 999)
    assert resultado is None, f"Esperaba None, obtuve {resultado}"


def test_buscar_por_id_no_consecutivo():
    lista = [{"id_cliente": 1}, {"id_cliente": 5}, {"id_cliente": 10}]
    resultado = buscar_por_id(lista, "id_cliente", 5)
    assert resultado is not None, "No encontró el elemento con id=5"


# ── Tests de cargar_datos / guardar_datos ─────────────────────────────────────

def test_cargar_archivo_inexistente():
    with pytest.raises(FileNotFoundError):
        cargar_datos("datos/archivo_que_no_existe.json")


def test_guardar_y_cargar_preserva_datos():
    datos = [{"id_cliente": 1, "nombre": "Doña Rosa", "urgente": False, "precio": None}]
    guardar_datos(ARCHIVO_TEMP, datos)
    cargado = cargar_datos(ARCHIVO_TEMP)
    os.remove(ARCHIVO_TEMP)
    assert cargado == datos, f"Datos no coinciden: {cargado}"


def test_cargar_archivo_corrupto():
    os.makedirs(os.path.join(_BASE, "datos"), exist_ok=True)
    with open(ARCHIVO_TEMP, "w", encoding="utf-8") as f:
        f.write("esto no es json {{{")
    with pytest.raises(ValueError):
        cargar_datos(ARCHIVO_TEMP)
    os.remove(ARCHIVO_TEMP)
