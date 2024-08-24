import random
import pickle
import random

class Product:
    def __init__(self, id_product, name, price, description) :
        self.id_product = id_product
        self.name = name
        self.price = price
        self.description = description
        self.owner_id = None

    def __repr__(self) :
        return f"Product(id_product={self.id_product}, name={self.name}, price={self.price}, description={self.description}), Dueño={self.owner_id}"
    
class Owner:
    def __init__(self, id_owner, name):
        self.id_owner = id_owner
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        product.owner_id = self.id_owner

if __name__ == "__main__":
    products = []
    Owners= []
    Owners.append(Owner(1, "Pablo monterreal"))
    Owners.append(Owner(2, "Juan Pablo"))
    Owners.append(Owner(3, "Diego"))
    Owners.append(Owner(4, "Lopez Obrador"))
    Owners.append(Owner(5, "Sofia"))
    
    # Crear 800,000 productos
    for id in range(1, 800001):
        item = Product(id, f"Producto {id}", round(random.uniform(10, 1000), 2), f"Descripción del producto {id}")
        random_owner = random.choice(Owners)  # Escoge un dueño aleatorio
        random_owner.add_product(item) 
    
    for owner in Owners:
        print(f"\nProductos de {owner.name} (ID del dueño: {owner.id_owner}):")
        for product in owner.products:
            print(f"  - {product}")

    with open('products.pkl', 'wb') as file:
        pickle.dump(products, file)