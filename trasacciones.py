from hashlib import sha256
import random

class transaction:
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

while True:
    input_ = input('Enter something: ')
    print(sha256(input_.encode('utf-8')).hexdigest())
    print('\n- Ingresa 1 para agregar una transacción \n- Ingresa 0 para salir ')
    opcion = int(input())

    selectRandomNode = random.randint(1, 5)

    if selectRandomNode == 1:
        node1.append(transaction('data'))
    elif selectRandomNode == 2:
        node2.append(transaction('data'))
    elif selectRandomNode == 3:
        node3.append(transaction('data'))
    elif selectRandomNode == 4:
        node4.append(transaction('data'))
    else:
        node5.append(transaction('data'))

    print(f'Node1: {node1}')
    print(f'Node2: {node2}')
    print(f'Node3: {node3}')
    print(f'Node4: {node4}')
    print(f'Node5: {node5}')
    
    if opcion == 0:
        break
    

# if selectRandomNode == 1:
#     node1.append(transaction(sha256(input_.encode('utf-8')).hexdigest()))
