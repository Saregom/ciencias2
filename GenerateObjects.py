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
        return f"Product(id_product={self.id_product}, name={self.name}, price={self.price}, description={self.description})"
    
class Owner:
    def __init__(self, id_owner, name):
        self.id_owner = id_owner
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        product.owner = self



if __name__ == "__main__":
    products = []
    Owners= []
    owner = Owner(1, "Pablo monterreal")
    Owners.append(owner)
    owner = Owner(2, "Juan Pablo")
    Owners.append(owner)
    owner = Owner(3, "Diego")
    Owners.append(owner)
    owner = Owner(4, "Lopez Obrador")
    Owners.append(owner)
    owner = Owner(5, "Sofia")
    Owners.append(owner)
    # Crear 800,000 productos
    for id in range(1, 800001):
        item = Product(id, f"Producto {id}", round(random.uniform(10, 1000), 2), f"Descripción del producto {id}")
        Owners[random.randint(1, 5)].add_product(item)
        products.append(item)

    with open('products.pkl', 'wb') as file:
        pickle.dump(products, file)
    
