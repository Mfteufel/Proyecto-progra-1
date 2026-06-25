"""
test_clientes.py — Tests para las funciones de clientes.py.

Ejecutar con: python3 tests/test_clientes.py  (desde sistema_oli/)

Estrategia: antes de cada test se guardan los datos reales, se trabaja
con datos de prueba controlados y al final se restaura el estado original.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import cargar_datos, guardar_datos, ARCHIVO_CLIENTES, ARCHIVO_PEDIDOS
from clientes import crear_cliente, buscar_cliente_por_id, modificar_cliente, eliminar_cliente


# ── Helpers de backup/restore ─────────────────────────────────────────────────

def _backup():
    clientes = cargar_datos(ARCHIVO_CLIENTES)
    pedidos = cargar_datos(ARCHIVO_PEDIDOS)
    return clientes, pedidos


def _restore(clientes, pedidos):
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)


# ── Tests de crear_cliente ────────────────────────────────────────────────────

def test_crear_cliente_valido():
    clientes, pedidos = _backup()
    try:
        total_antes = len(cargar_datos(ARCHIVO_CLIENTES))
        cliente = crear_cliente({
            "nombre": "Test Dona Rosa",
            "direccion": "Calle Falsa 123",
            "telefono": "01112345678",
            "tipo": "particular"
        })
        total_despues = len(cargar_datos(ARCHIVO_CLIENTES))
        assert cliente is not None, "crear_cliente devolvió None"
        assert cliente["nombre"] == "Test Dona Rosa", "Nombre incorrecto"
        assert cliente["tipo"] == "particular", "Tipo incorrecto"
        assert "id_cliente" in cliente, "Falta id_cliente"
        assert total_despues == total_antes + 1, "No se agregó el cliente a la lista"
        print("✓ crear_cliente: cliente válido creado correctamente")
    finally:
        _restore(clientes, pedidos)


def test_crear_cliente_tipo_invalido():
    clientes, pedidos = _backup()
    try:
        try:
            crear_cliente({
                "nombre": "Test Invalido",
                "direccion": "Alguna dirección",
                "telefono": "01112345678",
                "tipo": "fantasma"
            })
            assert False, "Debería haber lanzado ValueError"
        except ValueError:
            pass
        print("✓ crear_cliente: tipo inválido lanza ValueError")
    finally:
        _restore(clientes, pedidos)


def test_crear_cliente_telefono_invalido():
    clientes, pedidos = _backup()
    try:
        try:
            crear_cliente({
                "nombre": "Test Teléfono Mal",
                "direccion": "Alguna dirección",
                "telefono": "123",
                "tipo": "comercio"
            })
            assert False, "Debería haber lanzado ValueError"
        except ValueError:
            pass
        print("✓ crear_cliente: teléfono inválido lanza ValueError")
    finally:
        _restore(clientes, pedidos)


# ── Tests de buscar_cliente_por_id ────────────────────────────────────────────

def test_buscar_cliente_existente():
    clientes, pedidos = _backup()
    try:
        cliente_creado = crear_cliente({
            "nombre": "Test Buscar",
            "direccion": "Av. Siempre Viva 742",
            "telefono": "01198765432",
            "tipo": "comercio"
        })
        encontrado = buscar_cliente_por_id(cliente_creado["id_cliente"])
        assert encontrado is not None, "No encontró el cliente recién creado"
        assert encontrado["nombre"] == "Test Buscar", "Nombre no coincide"
        print("✓ buscar_cliente_por_id: encuentra cliente existente")
    finally:
        _restore(clientes, pedidos)


def test_buscar_cliente_inexistente():
    clientes, pedidos = _backup()
    try:
        resultado = buscar_cliente_por_id(99999)
        assert resultado is None, f"Esperaba None, obtuve {resultado}"
        print("✓ buscar_cliente_por_id: devuelve None si no existe")
    finally:
        _restore(clientes, pedidos)


# ── Tests de modificar_cliente ────────────────────────────────────────────────

def test_modificar_cliente_nombre():
    clientes, pedidos = _backup()
    try:
        cliente = crear_cliente({
            "nombre": "Nombre Original",
            "direccion": "Calle 1",
            "telefono": "01112345678",
            "tipo": "particular"
        })
        modificado = modificar_cliente(cliente["id_cliente"], {"nombre": "Nombre Modificado"})
        assert modificado is not None, "modificar_cliente devolvió None"
        assert modificado["nombre"] == "Nombre Modificado", "No se actualizó el nombre"
        print("✓ modificar_cliente: actualiza el nombre correctamente")
    finally:
        _restore(clientes, pedidos)


def test_modificar_cliente_inexistente():
    clientes, pedidos = _backup()
    try:
        resultado = modificar_cliente(99999, {"nombre": "Nadie"})
        assert resultado is None, "Debería devolver None si el cliente no existe"
        print("✓ modificar_cliente: devuelve None si el cliente no existe")
    finally:
        _restore(clientes, pedidos)


# ── Tests de eliminar_cliente ─────────────────────────────────────────────────

def test_eliminar_cliente_sin_pedidos():
    clientes, pedidos = _backup()
    try:
        cliente = crear_cliente({
            "nombre": "Test Eliminar",
            "direccion": "Calle 2",
            "telefono": "01112345678",
            "tipo": "particular"
        })
        resultado = eliminar_cliente(cliente["id_cliente"])
        assert resultado is True, "Debería devolver True al eliminar"
        assert buscar_cliente_por_id(cliente["id_cliente"]) is None, "El cliente sigue existiendo"
        print("✓ eliminar_cliente: elimina correctamente si no tiene pedidos")
    finally:
        _restore(clientes, pedidos)


def test_eliminar_cliente_con_pedidos():
    clientes, pedidos = _backup()
    try:
        cliente = crear_cliente({
            "nombre": "Test Con Pedido",
            "direccion": "Calle 3",
            "telefono": "01112345678",
            "tipo": "comercio"
        })
        # Simular un pedido asociado
        pedidos_actuales = cargar_datos(ARCHIVO_PEDIDOS)
        pedidos_actuales.append({
            "id_pedido": 99999,
            "id_cliente": cliente["id_cliente"],
            "id_tecnico": None,
            "descripcion": "Pedido de test",
            "urgente": False,
            "fecha": "01/01/2025",
            "estado": "pendiente",
            "precio": None
        })
        guardar_datos(ARCHIVO_PEDIDOS, pedidos_actuales)

        resultado = eliminar_cliente(cliente["id_cliente"])
        assert resultado is False, "No debería poder eliminar un cliente con pedidos"
        print("✓ eliminar_cliente: bloquea eliminación si tiene pedidos")
    finally:
        _restore(clientes, pedidos)


# ── Runner ────────────────────────────────────────────────────────────────────

def ejecutar_tests():
    tests = [
        test_crear_cliente_valido,
        test_crear_cliente_tipo_invalido,
        test_crear_cliente_telefono_invalido,
        test_buscar_cliente_existente,
        test_buscar_cliente_inexistente,
        test_modificar_cliente_nombre,
        test_modificar_cliente_inexistente,
        test_eliminar_cliente_sin_pedidos,
        test_eliminar_cliente_con_pedidos,
    ]

    aprobados = 0
    fallados = 0

    print("\n=== TESTS DE clientes.py ===\n")
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
