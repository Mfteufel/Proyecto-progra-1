"""
test_utils.py — Tests para las funciones genéricas de utils.py.

Ejecutar con: python3 tests/test_utils.py  (desde sistema_oli/)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import generar_id, buscar_por_id, cargar_datos, guardar_datos

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_TEMP = os.path.join(_BASE, "datos", "test_temp.json")


# ── Tests de generar_id ────────────────────────────────────────────────────────

def test_generar_id_lista_vacia():
    resultado = generar_id([], "id_cliente")
    assert resultado == 1, f"Esperaba 1, obtuve {resultado}"
    print("✓ generar_id: lista vacía devuelve 1")


def test_generar_id_con_elementos():
    lista = [{"id_cliente": 1}, {"id_cliente": 5}, {"id_cliente": 3}]
    resultado = generar_id(lista, "id_cliente")
    assert resultado == 6, f"Esperaba 6, obtuve {resultado}"
    print("✓ generar_id: devuelve max + 1 (no largo + 1)")


def test_generar_id_distintos_campos():
    lista = [{"id_pedido": 10}, {"id_pedido": 20}]
    resultado = generar_id(lista, "id_pedido")
    assert resultado == 21, f"Esperaba 21, obtuve {resultado}"
    print("✓ generar_id: funciona con cualquier campo PK")


# ── Tests de buscar_por_id ────────────────────────────────────────────────────

def test_buscar_por_id_existente():
    lista = [{"id_cliente": 1, "nombre": "Doña Rosa"}, {"id_cliente": 2, "nombre": "Kiosco Pepe"}]
    resultado = buscar_por_id(lista, "id_cliente", 2)
    assert resultado["nombre"] == "Kiosco Pepe", f"Nombre incorrecto: {resultado}"
    print("✓ buscar_por_id: encuentra elemento existente")


def test_buscar_por_id_inexistente():
    lista = [{"id_cliente": 1}]
    resultado = buscar_por_id(lista, "id_cliente", 999)
    assert resultado is None, f"Esperaba None, obtuve {resultado}"
    print("✓ buscar_por_id: devuelve None si no existe")


def test_buscar_por_id_no_consecutivo():
    lista = [{"id_cliente": 1}, {"id_cliente": 5}, {"id_cliente": 10}]
    resultado = buscar_por_id(lista, "id_cliente", 5)
    assert resultado is not None, "No encontró el elemento con id=5"
    print("✓ buscar_por_id: encuentra IDs no consecutivos")


# ── Tests de cargar_datos / guardar_datos ─────────────────────────────────────

def test_cargar_archivo_inexistente():
    try:
        cargar_datos("datos/archivo_que_no_existe.json")
        assert False, "Debería haber lanzado FileNotFoundError"
    except FileNotFoundError:
        pass
    print("✓ cargar_datos: archivo inexistente lanza FileNotFoundError")


def test_guardar_y_cargar_preserva_datos():
    datos = [{"id_cliente": 1, "nombre": "Doña Rosa", "urgente": False, "precio": None}]
    guardar_datos(ARCHIVO_TEMP, datos)
    cargado = cargar_datos(ARCHIVO_TEMP)
    os.remove(ARCHIVO_TEMP)
    assert cargado == datos, f"Datos no coinciden: {cargado}"
    print("✓ guardar_datos / cargar_datos: round-trip preserva tipos (None, bool)")


def test_cargar_archivo_corrupto():
    os.makedirs(os.path.join(_BASE, "datos"), exist_ok=True)
    with open(ARCHIVO_TEMP, "w", encoding="utf-8") as f:
        f.write("esto no es json {{{")
    try:
        cargar_datos(ARCHIVO_TEMP)
        assert False, "Debería haber lanzado ValueError"
    except ValueError:
        pass
    finally:
        if os.path.exists(ARCHIVO_TEMP):
            os.remove(ARCHIVO_TEMP)
    print("✓ cargar_datos: archivo corrupto lanza ValueError")


# ── Runner ────────────────────────────────────────────────────────────────────

def ejecutar_tests():
    tests = [
        test_generar_id_lista_vacia,
        test_generar_id_con_elementos,
        test_generar_id_distintos_campos,
        test_buscar_por_id_existente,
        test_buscar_por_id_inexistente,
        test_buscar_por_id_no_consecutivo,
        test_cargar_archivo_inexistente,
        test_guardar_y_cargar_preserva_datos,
        test_cargar_archivo_corrupto,
    ]

    aprobados = 0
    fallados = 0

    print("\n=== TESTS DE utils.py ===\n")
    for test in tests:
        try:
            test()
            aprobados += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            fallados += 1
        except Exception as e:
            print(f"✗ {test.__name__} — error inesperado: {e}")
            fallados += 1

    print(f"\n{aprobados} aprobados, {fallados} fallados de {len(tests)} tests")


if __name__ == "__main__":
    ejecutar_tests()
