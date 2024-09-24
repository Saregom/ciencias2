import pandas as pd
import random
import json
import csv 

from data_asignation import create_random_bandwith

with open("Graph/data_graph.json", 'r') as file:
    data_graph = json.load(file)

# --------------- actualizacion de datos ----------------
def update_data_graph(data_graph):
    for i in range(1, 21):
        data_graph[f'{i}']['ancho de banda'] = create_random_bandwith(i)

        current_failure = random.random()
        data_graph[f'{i}']['fallo actual'] = current_failure
        data_graph[f'{i}']['activo'] = current_failure > data_graph[f'{i}']['probabilidad de fallo']

    return data_graph

# data_graph = update_data_graph(data_graph)

# --------------- algoritmo dijkstra ----------------
def cargar_distancias(nombre_archivo):
    routers = []
    distancias = []
    
    with open(nombre_archivo, 'r') as archivo:
        reader = csv.reader(archivo)
        next(reader)
        
        for row in reader:
            routers.append(row[0])
            distancias.append([float(x) for x in row[1:]])

    return routers, distancias

def dijkstra(origen, destino, routers, distancias):
    num_routers = len(routers)
    visitados = [False] * num_routers
    distancias_min = [float('inf')] * num_routers
    distancias_min[routers.index(origen)] = 0
    predecesores = [None] * num_routers
    
    for _ in range(num_routers):
        min_distancia = float('inf')
        min_indice = -1
        for i in range(num_routers):
            if not visitados[i] and distancias_min[i] < min_distancia:
                min_distancia = distancias_min[i]
                min_indice = i

        visitados[min_indice] = True

        for i in range(num_routers):
            if distancias[min_indice][i] > 0 and not visitados[i]:
                nueva_distancia = distancias_min[min_indice] + distancias[min_indice][i]
                if nueva_distancia < distancias_min[i]:
                    distancias_min[i] = nueva_distancia
                    predecesores[i] = min_indice

    camino = []
    actual = routers.index(destino)
    if distancias_min[actual] == float('inf'):
        return [], float('inf')
    
    while actual is not None:
        camino.insert(0, routers[actual])
        actual = predecesores[actual]

    return camino, distancias_min[routers.index(destino)]

def encontrar_y_visualizar_camino(router_origen, router_destino, message):
    archivo_distancias = "Graph/bandwidth_speeds.csv"
    routers, distancias = cargar_distancias(archivo_distancias)
    camino, distancia_total = dijkstra(router_origen, router_destino, routers, distancias)
    
    print(f'\nEl mensaje "{message}" ha pasaodo por los routers:')
    print(" -> ".join(camino))
    print(f"Tiempo tomado: {distancia_total:.2f} ms\n")


# ejecucion principal
if __name__ == "__main__":
    message_to_send = input('Ingrese el mensaje a enviar: ')
    message_packages = message_to_send.split(' ')

    for message in message_packages:
        encontrar_y_visualizar_camino('1', '20', message)