import json
import csv 
from data_asignation import create_random_data 
from calculate_connection_weights import calculate_weight

with open("Graph/data_graph.json", 'r') as file:
    data_graph = json.load(file)

# --------------- algoritmo dijkstra ----------------
def load_data():
    routers = []
    distancias = []
    
    with open('Graph/connection_weights.csv', 'r') as archivo:
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

def get_messages_path(router_origen, router_destino, message, data_messages):
    routers, distancias = load_data()
    camino, distancia_total = dijkstra(router_origen, router_destino, routers, distancias)
        
    if camino == []:
        print(f'El mensaje "{message}" no pudo ser enviado de debido a un fallo en la red.')
    else:
        print(f'El mensaje "{message}" ha pasado por los routers:')
        print(" -> ".join(camino))
        print(f"Tiempo tomado: {distancia_total:.2f} s")

        data_messages.append({
            'message': message,
            'time': distancia_total
        })


# --------------- ejecucion principal ----------------
if __name__ == "__main__":
    message_to_send = input('\nIngrese el mensaje a enviar: ')
    message_packages = message_to_send.split(' ')

    data_messages = []

    for message in message_packages:
        print('\n--------------------------------')
        create_random_data() # le da de nuevo valores ramdoms a los nodos
        calculate_weight() # vuelve a calcular el peso de las aristas con los nuevos valores
        get_messages_path('1', '20', message, data_messages)

    # ordenar mensajes por menor tiempo
    data_messages_ordered = sorted(data_messages, key=lambda data: data['time'])

    final_message = ' '.join([message['message'] for message in data_messages_ordered])
    
    print('\n--------------------------------')
    print(f'El mensaje recibido es: "{final_message}"')
