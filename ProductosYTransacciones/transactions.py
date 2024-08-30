from hashlib import sha256
import random
import pickle
import copy
from GenerateObjects import Owner
from GenerateObjects import Product
from productMethods import binary_search_by_id
from productMethods import binary_search_by_name

with open('products.pkl', 'rb') as file:
    products = pickle.load(file)

with open('owners.pkl', 'rb') as file:
    owners = pickle.load(file)

nodes = [[], [], [], [], []] #Lista de nodos

class Transaction:
    def __init__(self, buyer, product):
        self.previus_hash = None
        self.id_transaction = len(nodes[0])+1
        self.hash = sha256(str(len(nodes[0])).encode('utf-8')).hexdigest() # toma la longitud de la lista de transacciones para generar cada hash diferente (index)
        self.product = product
        self.seller = product.owner.name
        self.buyer = buyer

    def __repr__(self) :
        #se muestra la información de la transaccion
        return f""" - previus hash: {self.previus_hash}
            hash: {self.hash}
            transaction id: {self.id_transaction}
            product: {self.product.name}   
            seller: {self.seller}   
            buyer: {self.buyer}
            price: {self.product.price}"""
    
    def change_info(self, product, seller, buyer):
        self.product = product
        self.seller = seller
        self.buyer = buyer
        self.hash = sha256(str(-len(nodes[0])).encode('utf-8')).hexdigest()

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


def validate_transactions_hash(nodes):
    # Valida que el hash de la transacción anterior sea igual al hash de la transacción actual
    previus_hash_error = False
    hash_per_node_error = False
    for node in nodes:
        for i in range(1, len(node)):
            if node[i].previus_hash != node[i-1].hash:
                print(f'\nError en el nodo #{nodes.index(node)+1}, hash previo de la transacción #{i+1} no coincide con el hash de la transacción #{i}')
                previus_hash_error = True
                break

    # Valida que el hash de la transacción en cada nodo sean iguales
    for i in range(len(nodes[0])):
        for j in range(len(nodes)-1):
            if nodes[j][i].hash != nodes[j+1][i].hash:
                print(f'\nError en la transaccion #{i+1}, no coincide con los hashes de los demás nodos')
                hash_per_node_error = True
                break
    
    return (previus_hash_error, hash_per_node_error)

# Se pide el nombre del producto y el comprador al usuario
def take_info():
    while True:
        new_product = input('\nEscribe el nombre del producto a comprar: ')
        productos_sorted = sorted(products, key=lambda product: product.name)       
        product_info = binary_search_by_name(productos_sorted, new_product)[0]

        if product_info != -1:
            n=0
            print('Vendedor: ', product_info.owner.name)
            while n==0:
                print("\nCompradores disponibles: ")
                for owner in owners:
                    print(owner)
                
                new_buyer = input('\nEscribe el nombre del comprador: ')

                for owner in owners:
                    if new_buyer == owner.name:
                        return product_info, owner
                        
                if n==0: print("Comprador NO existe")
            break
        else:
            print("El producto NO se encuentra en la lista")

# Ciclo principal
while True:
    action = int(input('\nQue deseas realizar?\n1. Crear una transaccion\n2. Cambiar una transaccion\n'))

    if action == 1:
        # Creación de la transacción
        product, owner = take_info()
        new_transaction = Transaction(owner.name, product) 
        add_transaction(nodes, new_transaction)

        # Imprime las transacciones de cada nodo
        for i, node in enumerate(nodes):
            print(f'\nNode {i+1}:')
            for transaction in node:
                print(transaction)
    
    elif action == 2:
        try:
            print('\nElije una transacción a cambiar (transaction id):')
            for transaction in nodes[0]:
                print(transaction)
            transaction_id = int(input())

            backup_transaction = copy.deepcopy(nodes[0][transaction_id-1])
            transaction_to_change = nodes[0][transaction_id-1]

            product, owner = take_info()
            transaction_to_change.change_info(product, product.owner.name, owner.name)
        except:
            print('Transacción no encontrada')
                
    errors = validate_transactions_hash(nodes)

    # Si hay errores se restaura la transacción desde la copia de seguridad (backup_transaction)
    if errors[0] or errors[1]:
        for node in nodes:
            for i in range(len(node)):
                if node[i].id_transaction == backup_transaction.id_transaction:
                    node[i] = backup_transaction # Restauramos desde la copia de seguridad
        
        # Revalidamos las transacciones después de la restauracion
        errors_after_restore = validate_transactions_hash(nodes)
        
        if errors_after_restore[0] or errors_after_restore[1]:
            print('\nNo se pudo restaurar completamente la integridad de las transacciones')
        else:
            print('\nHubieron cambios en la transaccion, se han restablecido los datos')

    print('\n----------------\n- Ingresa cualquier tecla para continuar\n- Ingresa 0 para salir')
    opcion = input()
    print('----------------')

    if opcion == '0':
        print('Saliendo del programa...')
        exit()
