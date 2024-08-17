import random
import pickle

class Product:
    def __init__(self, id_product, name, price, description) :
        self.id_product = id_product
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self) :
        return f"Product(id_product={self.id_product}, name={self.name}, price={self.price}, description={self.description})"

products = []

# Crear 800,000 productos
for id in range(0, 800000):
    item = Product(id, f"Producto {id}", round(random.uniform(10, 1000), 2), f"Descripción del producto {id}")
    products.append(item)

with open('products.pkl', 'wb') as file:
    pickle.dump(products, file)

