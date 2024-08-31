import random
import time

# Inicializar el diccionario de productos
productos = {}

# Función para generar un nombre de producto aleatorio
def generar_nombre_producto(idproducto):
    return f"Producto{idproducto}"

# Función para generar un precio aleatorio
def generar_precio():
    return round(random.uniform(10, 1000), 2)

# Función para generar una descripción aleatoria
def generar_descripcion(idproducto):
    return f"Descripción del producto {idproducto}"

# Crear 800,000 productos
for idproducto in range(1, 800001):
    productos[idproducto] = {
        'nombre': generar_nombre_producto(idproducto),
        'precio': generar_precio(),
        'descripcion': generar_descripcion(idproducto)
    }

# Ejemplo: acceder a un producto específico
idproducto = 80000  # Cambiar por el ID que quieras consultar


inicio = time.time()
producto = productos.get(idproducto)
fin = time.time()

if producto:
    print(f"Producto encontrado: {producto['nombre']}")
    print(f"Precio: ${producto['precio']}")
    print(f"Descripción: {producto['descripcion']}")
else:
    print("Producto no encontrado.")

print(f"Tiempo de búsqueda: {round(fin - inicio,10)/1000} milisegundos")