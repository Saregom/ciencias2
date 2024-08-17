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
def binary_search_by_id(arr, id_produdt):
    left_pos = 0
    right_pos = len(arr) - 1

    while left_pos <= right_pos:
        mid_pos = left_pos + (right_pos - left_pos) // 2
        if arr[mid_pos].id_product == id_produdt:
            return arr[mid_pos]
        elif arr[mid_pos].id_product < id_produdt:
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

product_searched_by_id = binary_search_by_id(products, 2)
product_searched_by_name = binary_search_by_name(products, 'Producto 2')

if product_searched_by_id != -1:
    print("\nEl producto se encuentra en la lista:")
    print(product_searched_by_id)
else:
    print("\nEl producto NO se encuentra en la lista")

if product_searched_by_name != -1:
    print("\nEl producto se encuentra en la lista:")
    print(product_searched_by_name)
else:
    print("\nEl producto NO se encuentra en la lista")