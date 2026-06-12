from utils import cargar_datos, guardar_datos, generar_id, buscar_por_id, ARCHIVO_CLIENTES

# Probar que cargar un archivo inexistente devuelve []
print(cargar_datos(ARCHIVO_CLIENTES))   # → []

# Probar guardar y volver a cargar
datos = [
    {"id_cliente": 1, "nombre": "Doña Rosa", "direccion": "Av. Siempreviva 742", "telefono": "11-1234-5678", "tipo": "particular"},
    {"id_cliente": 2, "nombre": "Kiosco Pepe", "direccion": "Calle Falsa 123", "telefono": "11-9876-5432", "tipo": "comercio"},
]
guardar_datos(ARCHIVO_CLIENTES, datos)
cargado = cargar_datos(ARCHIVO_CLIENTES)
print(cargado)   # → lista con 2 dicts, tipos correctos

# Probar generar_id
print(generar_id(cargado, "id_cliente"))   # → 3

# Probar buscar_por_id
print(buscar_por_id(cargado, "id_cliente", 1))   # → dict de Doña Rosa
print(buscar_por_id(cargado, "id_cliente", 99))  # → None
