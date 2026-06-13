"""
main.py — Punto de entrada del sistema Oli.

Solo contiene el menú principal. Cada módulo maneja su propio submenú.
"""

from clientes import menu_clientes
from tecnicos import menu_tecnicos
from pedidos import menu_pedidos
from cobros import menu_cobros
from repuestos import menu_repuestos
from stock import menu_stock


def main():
    print("\n¡Bienvenido al Sistema Oli!")

    while True:
        print("\n=== SISTEMA OLI ===")
        print("1. Clientes")
        print("2. Técnicos")
        print("3. Pedidos")
        print("4. Cobros")
        print("5. Historial       (próximamente)")
        print("6. Repuestos")
        print("7. Stock del estante")
        print("0. Salir")

        opcion = input("\nElegí una opción: ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_tecnicos()
        elif opcion == "3":
            menu_pedidos()
        elif opcion == "4":
            menu_cobros()
        elif opcion == "5":
            print("Ese módulo todavía no está disponible.")
        elif opcion == "6":
            menu_repuestos()
        elif opcion == "7":
            menu_stock()
        elif opcion == "0":
            print("\nHasta luego.")
            break
        else:
            print("Opción inválida, elegí una de las que aparecen en el menú.")


if __name__ == "__main__":
    main()
