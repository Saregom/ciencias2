import pickle
import time
from generateObjects import Product

def take_time(func):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        product_infoado = func(*args, **kwargs)
        fin = time.perf_counter()
        tiempo =(f"\nTiempo de ejecución de {func.__name__}: {(fin - inicio)*1000:.10f} milisegundos")
        return product_infoado,tiempo
    return wrapper

with open('products.pkl', 'rb') as file:
    products = pickle.load(file)

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

def search_by_id_or_name():
    print("""
        Dsea buscar por ID o por nombre?
        1. ID
        2. Nombre
        """)

    return int(input("Opción: "))

def search_products():
    print("""
    Búsqueda binaria y secuencial de productos (por ID y por nombre)
      
    Programa hecho por: Juan Lozada 2022020014,
                        Jhojan Aragon 20221020060,
                        Santiago Reyes 20221020098
    """)
    
    while True:
        opcion = int(input("""
        ¿Qué tipo de búsqueda desea realizar?
        1. Secuencial
        2. Binaria
        """))
        
        if opcion == 1:
            print("\nBusqueda secuencial")

            if search_by_id_or_name() == 1:
                opcion = int(input("ID a buscar: "))
                product_info, time_taken = sequential_search_by_id(products, opcion)
            else:
                opcion = input("Nombre a buscar (Prodcuto #)(Ej: Producto 5000): ")
                product_info, time_taken = sequential_search_by_name(products, opcion)
                
        elif opcion == 2:
            print("\nBusqueda binaria")
            
            if search_by_id_or_name() == 1:
                opcion_binaria = int(input("ID a buscar: "))
                product_info, time_taken = binary_search_by_id(products, opcion_binaria)

            else:
                opcion = input("Nombre a buscar (Producto #): ")
                products_sorted_by_name = sorted(products, key=lambda product: product.name)
                product_info, time_taken = binary_search_by_name(products_sorted_by_name, opcion)
                
        else: 
            print("Opción no válida, intente de nuevo.")

        if product_info != -1:
            print("\nEl producto se encuentra en la lista:")
            print(product_info)
            print(time_taken)
        else:
            print("\nEl producto NO se encuentra en la lista")
        
        continue_searching = input("\n¿Desea realizar otra búsqueda? (s/n): ").strip().lower()

        if continue_searching != 's':
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    search_products()
    
