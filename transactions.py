from hashlib import sha256
import random
import pickle
import copy
from generateObjects import Owner
from generateObjects import Product
from productMethods import binary_search_by_id

with open('products.pkl', 'rb') as file:
    products = pickle.load(file)

with open('owners.pkl', 'rb') as file:
    owners = pickle.load(file)

nodes = [[], [], [], [], []] #Listas de nodoss

class Transaction:
    def __init__(self, buyer, product):
        self.previus_hash = None
        self.hash = sha256(str(len(nodes[0])).encode('utf-8')).hexdigest() # toma la longitud de la lista de transacciones para generar cada hash diferente (index)
        self.product = product
        self.seller = product.owner.name
        self.buyer = buyer

    def __repr__(self) :
        return f" - previus hash: {self.previus_hash}, hash: {self.hash} product: {self.product.name}, seller: {self.seller}, buyer: {self.buyer}"

# Se copia la transacción en los demás nodos con diferente apuntador de memoria (deepcopy)
def copy_nodes(nodes, selected_node):
    for node in nodes:
        if node != selected_node:
            node.append(copy.deepcopy(new_transaction))

# Se elige un nodo aleatorio y se agrega la transacción
def add_transaction(nodes, new_transaction):
    random_node_index = random.randint(0, 4)
    selected_node = nodes[random_node_index]
    print(f'\nEl nodo #{random_node_index} fue el primero en responer...')

    # Si el nodo no está vacío, se le asigna el previus hash de la transacción anterior
    if len(selected_node) != 0:
        new_transaction.previus_hash = selected_node[-1].hash

    selected_node.append(new_transaction)

    copy_nodes(nodes, selected_node)

while True:
    # Se elige un comprador de la lista de owners
    print('\nElije un comprador (1, 2, 3, 4, 5):')
    for owner in owners:
        print(owner)
    buyer_id = int(input())
    
    # Busca el producto por binary search
    product_to_buy_id = int(input('\nEscribe el id del producto a comparar (1-800000): '))
    product, time_taken = binary_search_by_id(products, product_to_buy_id) 

    # Creación de la transacción
    new_transaction = Transaction(owners[buyer_id-1].name, product) 
    
    add_transaction(nodes, new_transaction) 

    # Imprime las transacciones de cada nodo
    for i, node in enumerate(nodes):
        print(f'\nNode {i+1}:')
        for transaction in node:
            print(transaction)

    print('\n----------------\n- Oprime cualquier tecla para continuar\n- Ingresa 0 para salir')
    opcion = input()
    print('----------------')

    if opcion == '0':
        print('Saliendo del programa...')
        exit()
