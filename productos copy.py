import pickle
import time
from GenerateObjects import Product

def take_time(func):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        tiempo =(f"\nTiempo de ejecución de {func.__name__}: {(fin - inicio)*1000:.10f} milisegundos")
        return resultado,tiempo
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

def search_products():
    print("""

    Búsqueda binaria y secuencial de productos (por ID y por nombre)
      
    Programa hecho por: Juan Lozada 2022020014,
                    Jhojan Aragon 20221020098,
                    Santiago Reyes 20221020060
    
""")
    
    while True:
        opcion = int(input("""
      ¿Qué tipo de búsqueda desea realizar?
      1. Secuencial
      2. Binaria
      """))
        
        if opcion == 1:
            print("Busqueda secuencial")
            
            opcion = int(input("ID a buscar: "))
            aux = "Producto " + str(opcion)
            
            result, imprimir = sequential_search_by_id(products, opcion)
            if result != -1:
                print("\\nEl producto se encuentra en la lista:")
                print(result)
                print(imprimir)
            else:
                print("\\nEl producto NO se encuentra en la lista")
            
            result_name, imprimir2 = sequential_search_by_name(products, aux)
            if result_name != -1:
                print("\\nEl producto se encuentra en la lista:")
                print(result_name)
                print(imprimir2)
            else:
                print("\\nEl producto NO se encuentra en la lista")
                
        elif opcion == 2:
            print("Busqueda binaria")
            
            products_sorted_by_name = sorted(products, key=lambda product: product.name)
            opcion_binaria = int(input("ID a buscar: "))
            str_opcion_binaria = str(opcion_binaria)
            aux_binaria = "Producto " + str_opcion_binaria
            
            result_id_binary, imprimir = binary_search_by_id(products, opcion_binaria)
            if result_id_binary != -1:
                print("\\nEl producto se encuentra en la lista:")
                print(result_id_binary)
                print(imprimir)
            else:
                print("\\nEl producto NO se encuentra en la lista")
                
            result_name_binaria, imprimir2 = binary_search_by_name(products_sorted_by_name, aux_binaria)
            if result_name_binaria != -1:
                print("\\nEl producto se encuentra en la lista:")
                print(result_name_binaria)
                print(imprimir2)
            else:
                print("\\nEl producto NO se encuentra en la lista")
                
        else: 
            print("Opción no válida, intente de nuevo.")
        
        otra_busqueda = input("¿Desea realizar otra búsqueda? (s/n): ").strip().lower()
        if otra_busqueda != 's':
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    search_products()