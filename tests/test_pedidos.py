"""
test_pedidos.py — Tests para las funciones de pedidos.py.

Ejecutar con: python3 tests/test_pedidos.py  (desde sistema_oli/)

Estrategia: antes de cada test se guardan los datos reales y al final
se restauran, de modo que los archivos .json quedan igual que al principio.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    cargar_datos, guardar_datos,
    ARCHIVO_CLIENTES, ARCHIVO_PEDIDOS, ARCHIVO_COBROS, ARCHIVO_REPUESTOS
)
from pedidos import (
    crear_pedido, listar_pedidos, listar_pedidos_por_estado,
    listar_pedidos_por_cliente, asignar_tecnico,
    cambiar_estado_pedido, eliminar_pedido
)


# ── Helpers de backup/restore ─────────────────────────────────────────────────

def _backup():
    return (
        cargar_datos(ARCHIVO_CLIENTES),
        cargar_datos(ARCHIVO_PEDIDOS),
        cargar_datos(ARCHIVO_COBROS),
        cargar_datos(ARCHIVO_REPUESTOS),
    )


def _restore(clientes, pedidos, cobros, repuestos):
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    guardar_datos(ARCHIVO_PEDIDOS, pedidos)
    guardar_datos(ARCHIVO_COBROS, cobros)
    guardar_datos(ARCHIVO_REPUESTOS, repuestos)


def _cliente_test(clientes):
    """Inserta un cliente de prueba y devuelve su id_cliente."""
    from utils import generar_id
    id_nuevo = generar_id(clientes, "id_cliente")
    clientes.append({
        "id_cliente": id_nuevo,
        "nombre": "Cliente Test",
        "direccion": "Calle Test 1",
        "telefono": "01112345678",
        "tipo": "particular"
    })
    guardar_datos(ARCHIVO_CLIENTES, clientes)
    return id_nuevo


# ── Tests de crear_pedido ─────────────────────────────────────────────────────

def test_crear_pedido_cliente_valido():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        total_antes = len(cargar_datos(ARCHIVO_PEDIDOS))
        pedido = crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Reparar aire acondicionado",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        total_despues = len(cargar_datos(ARCHIVO_PEDIDOS))
        assert pedido is not None, "crear_pedido devolvió None"
        assert pedido["id_cliente"] == id_cliente, "id_cliente incorrecto"
        assert pedido["estado"] == "pendiente", "Estado inicial debe ser 'pendiente'"
        assert pedido["precio"] is None, "Precio inicial debe ser None"
        assert total_despues == total_antes + 1, "No se agregó el pedido a la lista"
        print("✓ crear_pedido: pedido válido creado en estado 'pendiente'")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


def test_crear_pedido_cliente_inexistente():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        try:
            crear_pedido({
                "id_cliente": 99999,
                "descripcion": "Trabajo fantasma",
                "urgente": False,
                "fecha": "25/06/2026"
            })
            assert False, "Debería haber lanzado ValueError"
        except ValueError:
            pass
        print("✓ crear_pedido: cliente inexistente lanza ValueError")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


# ── Tests de listar_pedidos_por_estado ────────────────────────────────────────

def test_listar_pedidos_por_estado_valido():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Test estado pendiente",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        resultado = listar_pedidos_por_estado("pendiente")
        assert isinstance(resultado, list), "Debe devolver una lista"
        assert all(p["estado"] == "pendiente" for p in resultado), \
            "Todos deben estar en estado 'pendiente'"
        print("✓ listar_pedidos_por_estado: filtra correctamente por estado")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


def test_listar_pedidos_por_estado_invalido():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        resultado = listar_pedidos_por_estado("inventado")
        assert resultado is None, "Estado inválido debe devolver None"
        print("✓ listar_pedidos_por_estado: estado inválido devuelve None")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


# ── Tests de cambiar_estado_pedido ────────────────────────────────────────────

def test_cambiar_estado_secuencia_correcta():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        pedido = crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Test avance de estado",
            "urgente": True,
            "fecha": "25/06/2026"
        })
        id_pedido = pedido["id_pedido"]
        # pendiente → asignado
        resultado = cambiar_estado_pedido(id_pedido, "asignado")
        assert resultado is not None, "Debería poder avanzar a 'asignado'"
        assert resultado["estado"] == "asignado", "Estado incorrecto"
        # asignado → en_curso
        resultado = cambiar_estado_pedido(id_pedido, "en_curso")
        assert resultado["estado"] == "en_curso", "Estado incorrecto"
        print("✓ cambiar_estado_pedido: avanza correctamente en la secuencia")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


def test_cambiar_estado_saltando_paso():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        pedido = crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Test saltar estado",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        # Intentar ir directo de "pendiente" a "en_curso" (saltando "asignado")
        resultado = cambiar_estado_pedido(pedido["id_pedido"], "en_curso")
        assert resultado is None, "No debería permitir saltar estados"
        print("✓ cambiar_estado_pedido: rechaza saltar pasos en la secuencia")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


# ── Tests de listar_pedidos_por_cliente ───────────────────────────────────────

def test_listar_pedidos_por_cliente():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Primer trabajo",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Segundo trabajo",
            "urgente": True,
            "fecha": "25/06/2026"
        })
        resultado = listar_pedidos_por_cliente(id_cliente)
        assert len(resultado) == 2, f"Esperaba 2 pedidos, obtuve {len(resultado)}"
        assert all(p["id_cliente"] == id_cliente for p in resultado), \
            "Todos los pedidos deben ser de ese cliente"
        print("✓ listar_pedidos_por_cliente: devuelve solo pedidos del cliente")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


# ── Tests de eliminar_pedido ──────────────────────────────────────────────────

def test_eliminar_pedido_sin_cobros():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        pedido = crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Test eliminar",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        resultado = eliminar_pedido(pedido["id_pedido"])
        assert resultado is True, "Debería poder eliminar un pedido sin cobros"
        pedidos_actuales = cargar_datos(ARCHIVO_PEDIDOS)
        ids = [p["id_pedido"] for p in pedidos_actuales]
        assert pedido["id_pedido"] not in ids, "El pedido sigue en la lista"
        print("✓ eliminar_pedido: elimina correctamente si no tiene cobros ni repuestos")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


def test_eliminar_pedido_con_cobros():
    clientes, pedidos, cobros, repuestos = _backup()
    try:
        id_cliente = _cliente_test(clientes)
        pedido = crear_pedido({
            "id_cliente": id_cliente,
            "descripcion": "Test con cobro",
            "urgente": False,
            "fecha": "25/06/2026"
        })
        # Simular un cobro asociado al pedido
        cobros_actuales = cargar_datos(ARCHIVO_COBROS)
        cobros_actuales.append({
            "id_cobro": 99999,
            "id_pedido": pedido["id_pedido"],
            "monto": 1000.0,
            "forma_pago": "efectivo",
            "recibido_por": "Oli",
            "estado": "pendiente",
            "fecha": "25/06/2026"
        })
        guardar_datos(ARCHIVO_COBROS, cobros_actuales)

        resultado = eliminar_pedido(pedido["id_pedido"])
        assert resultado is False, "No debería poder eliminar un pedido con cobros"
        print("✓ eliminar_pedido: bloquea eliminación si tiene cobros")
    finally:
        _restore(clientes, pedidos, cobros, repuestos)


# ── Runner ────────────────────────────────────────────────────────────────────

def ejecutar_tests():
    tests = [
        test_crear_pedido_cliente_valido,
        test_crear_pedido_cliente_inexistente,
        test_listar_pedidos_por_estado_valido,
        test_listar_pedidos_por_estado_invalido,
        test_cambiar_estado_secuencia_correcta,
        test_cambiar_estado_saltando_paso,
        test_listar_pedidos_por_cliente,
        test_eliminar_pedido_sin_cobros,
        test_eliminar_pedido_con_cobros,
    ]

    aprobados = 0
    fallados = 0

    print("\n=== TESTS DE pedidos.py ===\n")
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
