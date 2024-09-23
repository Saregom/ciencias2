import pandas as pd
import random

# crear un acncho de banda aleatorio para cada 20 nodos 
def create_random_bandwith(i_node):
    if i_node == 1 or i_node == 20:
        return random.randint(1, 10) 
    elif (i_node >= 2 and i_node <= 6) or (i_node >= 15 and i_node <= 19):
        return random.randint(10, 50)
    elif (i_node >= 7 and i_node <= 14):
        return random.randint(50, 100)

def get_fail_prob(i_node):
    if i_node == 1 or i_node == 20:
        return 0.2
    elif (i_node >= 2 and i_node <= 6) or (i_node >= 15 and i_node <= 19):
        return 0.1
    elif (i_node >= 7 and i_node <= 14):
        return 0.02
    
def get_quee_capacity(i_node):
    if i_node == 1 or i_node == 20:
        return 5
    elif (i_node >= 2 and i_node <= 6) or (i_node >= 15 and i_node <= 19):
        return 20
    elif (i_node >= 7 and i_node <= 14):
        return 50
    
def get_active(fail_prob):
    return random.random() > fail_prob

# Se ejecuta la primera vez para crear el archivo data_graph.json
def create_random_data():
    new_data_graph = {}
    for i in range(1, 21):
        fail_prob = get_fail_prob(i)
        current_failure = random.random()
        new_data_graph[i] = {
            'ancho de banda': create_random_bandwith(i),  
            'probabilidad de fallo': fail_prob,
            'capacidad de encolamiento': get_quee_capacity(i),
            'fallo actual': current_failure,
            'activo': current_failure > fail_prob,
        }
    pd.DataFrame(new_data_graph).to_json('Graph/data_graph.json')
