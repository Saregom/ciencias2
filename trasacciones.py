from hashlib import sha256
import random
import copy

class Transaction:
    def __init__(self, data):
        self.beforeHash = None
        self.hash = sha256(data.encode('utf-8')).hexdigest
        self.data = data
        self.nextHash = None

node1 = []
node2 = []
node3 = []
node4 = []
node5 = []

nodes = [node1, node2, node3, node4, node5]

def copy_nodes():
    global nodes
    
    selectRandomNode = random.randint(0, 4)
    selected_node = nodes[selectRandomNode]

    new_transaction = Transaction('data')
    selected_node.append(new_transaction)

    for index, node in enumerate(nodes):
        if index != selectRandomNode:
            # node.append(copy.deepcopy(new_transaction))
            node.append(new_transaction)

while True:
    input_ = input('\nEnter something for hash: ')
    print(sha256(input_.encode('utf-8')).hexdigest())

    print('\n- Oprime cualquier tecla para continuar \n- Ingresa 0 para salir ')
    opcion = int(input())
    
    if opcion == 0:
        exit()
    else:
        copy_nodes()

    print(f'Node1: {node1}')
    print(f'Node2: {node2}')
    print(f'Node3: {node3}')
    print(f'Node4: {node4}')
    print(f'Node5: {node5}')

