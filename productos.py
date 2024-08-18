import pickle
import time
from GenerateObjects import Product

def take_time(func):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"\nTiempo de ejecución de {func.__name__}: {(fin - inicio)*1000:.10f} milisegundos")
        return resultado
    return wrapper

with open('products.pkl', 'rb') as archivo:
    products = pickle.load(archivo)

@take_time
def sequential_search_by_id(arr, id_product):
    for product in arr:
        if product.id_product == id_product:
            return product
    return -1

@take_time
def sequential_search_by_name(arr, name):
    for product in arr:
        if product.name == name:
            return product
    return -1

@take_time
def binary_search_by_id(arr, id_product):
    left_pos = 0
    right_pos = len(arr) - 1

    while left_pos <= right_pos:
        mid_pos = left_pos + (right_pos - left_pos) // 2
        if arr[mid_pos].id_product == id_product:
            return arr[mid_pos]
        elif arr[mid_pos].id_product < id_product:
            left_pos = mid_pos + 1
        else:
            right_pos = mid_pos - 1
    return -1

@take_time
def binary_search_by_name(arr, name):
    left_pos = 0
    right_pos = len(arr) - 1

    while left_pos <= right_pos:
        mid_pos = left_pos + (right_pos - left_pos) // 2
        if arr[mid_pos].name == name:
            return arr[mid_pos]
        elif arr[mid_pos].name < name:
            left_pos = mid_pos + 1
        else:
            right_pos = mid_pos - 1
    return -1

print("""

    Búsqueda binaria y secuencial de productos (por ID y por nombre)
      
    Programa hecho por: Juan Lozada 2022020014,
                    Jhojan Aragon 20221020098,
                    Santiago Reyes 20221020060
    
""")
opcion = int(input("""
      ¿Qué tipo de búsqueda desea realizar?
      1. Secuencial
      2. Binaria
      """))

if opcion == 1:
    print("Busqueda secuencial")
    opcion = int(input("ID a buscar: "))
    str_opcion = str(opcion)
    aux = "Producto " + str_opcion
    #Busqueda por ID y nombre Secuencial
    #Ejecuta la función de búsqueda secuencial por ID
    result = sequential_search_by_id(products, opcion)
    if sequential_search_by_id(products, opcion) != -1:
        print("\nEl producto se encuentra en la lista:")
        print(result)
        
    else:
        print("\nEl producto NO se encuentra en la lista")
        exit()
    
    #Ejecuta la función de búsqueda secuencial por nombre
    result_name = sequential_search_by_name(products, aux)
    if sequential_search_by_name(products, aux) != -1:
        print("\nEl producto se encuentra en la lista:")
        print(result_name)
        
    else:
        print("\nEl producto NO se encuentra en la lista")
        exit()


elif opcion == 2:
    print("Busqueda binaria")
    
    products_sorted_by_name = sorted(products, key=lambda product: product.name)
    opcion_binaria = int(input("ID a buscar: "))
    str_opcion_binaria = str(opcion_binaria)
    aux_binaria = "Producto " + str_opcion_binaria
    #Busqueda por ID y nombre Binaria
    #Ejecuta la función de búsqueda binaria por ID
    result_id_binary = binary_search_by_id(products, opcion_binaria)
    if binary_search_by_id(products, opcion_binaria) != -1:
        print("\nEl producto se encuentra en la lista:")
        print(result_id_binary)
        
    else:
        print("\nEl producto NO se encuentra en la lista")
        exit()
    
    #Ejecuta la función de búsqueda secuencial por nombre
    result_name_binaria = binary_search_by_name(products_sorted_by_name, aux_binaria)
    if binary_search_by_name(products_sorted_by_name, aux_binaria) != -1:
        print("\nEl producto se encuentra en la lista:")
        print(result_name_binaria)
        
    else:
        print("\nEl producto NO se encuentra en la lista")
        exit()

else: 
    print("Opción no válida, inicie el programa de nuevo")
    exit()
