import pandas as pd
import random
import json

from data_asignation import create_random_bandwith

with open("Graph/data_graph.json", 'r') as file:
    data_graph = json.load(file)

def update_data_graph(data_graph):
    for i in range(1, 21):
        data_graph[f'{i}']['ancho de banda'] = create_random_bandwith(i)

        current_failure = random.random()
        data_graph[f'{i}']['fallo actual'] = current_failure
        data_graph[f'{i}']['activo'] = current_failure > data_graph[f'{i}']['probabilidad de fallo']

    return data_graph

data_graph = update_data_graph(data_graph)
print(data_graph)