import random
import pickle
import random

class Product:
    def __init__(self, id_product, name, price, description, owner) :
        self.id_product = id_product
        self.name = name
        self.price = price
        self.description = description
        self.owner = owner

    def __repr__(self) :
        return f"Product(id_product={self.id_product}, name={self.name}, price={self.price}, description={self.description}), Dueño={self.owner.id_owner}"
    
class Owner:
    def __init__(self, id_owner, name):
        self.id_owner = id_owner
        self.name = name
        self.products = []

    def __repr__(self) :
        return f" - id_owner: {self.id_owner}, name: {self.name}"

    def add_product(self, product):
        self.products.append(product)

if __name__ == "__main__":
    products = []
    owners= []
    owners.append(Owner(1, "Pablo monterreal"))
    owners.append(Owner(2, "Juan Pablo"))
    owners.append(Owner(3, "Diego"))
    owners.append(Owner(4, "Lopez Obrador"))
    owners.append(Owner(5, "Sofia"))
    
    # Crear 800,000 productos
    for id in range(1, 800001):
        random_owner = random.choice(owners)  # Escoge un dueño aleatorio
        product = Product(id, f"Producto {id}", round(random.uniform(10, 1000), 2), f"Descripción del producto {id}", random_owner)
        random_owner.add_product(product)
        products.append(product)
    
#    for owner in owners:
#        print(f"\nProductos de {owner.name} (ID del dueño: {owner.id_owner}):")
#        for product in owner.products:
#            print(f"  - {product}")

    with open('products.pkl', 'wb') as file:
        pickle.dump(products, file)

    with open('owners.pkl', 'wb') as file:
        pickle.dump(owners, file)