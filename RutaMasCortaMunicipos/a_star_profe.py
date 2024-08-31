
# usando algoritmo a* hallar el camino mas corto entre dos nodos en un multigrafo de 20 nodos
import heapq
import matplotlib.pyplot as plt
import networkx as nx


def a_star(start_node, goal_node, graph, posicion):
    # Inicializar listas abierta y cerrada
    open_list = []
    closed_list = set()

    # Inicializar costos G y H de cada nodo
    g_costs = {node: float('inf') for node in graph}
    h_costs = {node: heuristic(node, posicion) for node in graph}
    g_costs[start_node] = 0

    # Agregar nodo inicial a lista abierta
    heapq.heappush(
        open_list, (g_costs[start_node] + h_costs[start_node], start_node))

    while open_list:
        # Seleccionar nodo con menor costo total estimado
        current_node = heapq.heappop(open_list)[1]

        # Si se alcanza el nodo objetivo, devolver la ruta
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node)
                current_node = graph[current_node]['parent']
            path.append(start_node)
            return path[::-1]  # , g_costs[goal_node]

        # Agregar nodo actual a lista cerrada
        closed_list.add(current_node)

        # Explorar nodos vecinos
        for neighbor, cost in graph[current_node]['neighbors'].items():
            if neighbor in closed_list:
                continue

            tentative_g_cost = g_costs[current_node] + cost
            if tentative_g_cost < g_costs[neighbor]:
                # Actualizar costos G y H del vecino
                g_costs[neighbor] = tentative_g_cost
                h_costs[neighbor] = heuristic(neighbor, posicion)
                graph[neighbor]['parent'] = current_node

                # Agregar vecino a lista abierta
                heapq.heappush(
                    open_list, (g_costs[neighbor] + h_costs[neighbor], neighbor))

    # No se encontró una ruta, devolver None
    return None


def heuristic(node1, posicion):  # estimar la distancia desde node1 hasta node2
    # distancia euclidiana entre nodos
    return ((posicion[node1]))


if __name__ == '__main__':
    # Ejemplo de uso
    graph = {
        'Bucharest': {'neighbors': {'Urziceni': 85, 'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90}, 'parent': None},
        'Urziceni': {'neighbors': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142}, 'parent': None},
        'Vaslui': {'neighbors': {'Lasi': 92, 'Urziceni': 142}, 'parent': None},
        'Lasi': {'neighbors': {'Neamt': 87, 'Vaslui':92}, 'parent': None},
        'Neamt': {'neighbors': {'Lasi':  87}, 'parent': None},
        'Hirsova': {'neighbors': {'Eforie':86, 'Urziceni': 98}, 'parent': None},
        'Eforie': {'neighbors': {'Hirsova': 86}, 'parent': None},
        'Fagaras': {'neighbors': {'Sibiu': 99, 'Bucharest': 211}, 'parent': None},
        'Sibiu': {'neighbors': {'Rimnicu Vilcea':80, 'Oradea': 151, 'Arad': 140, 'Fagaras': 99}, 'parent': None},
        'Oradea': {'neighbors': {'Zerind': 71, 'Sibiu': 151}, 'parent': None},
        'Zerind': {'neighbors': {'Oradea': 71, 'Arad': 75}, 'parent': None},
        'Arad': {'neighbors': {'Sibiu': 140, 'Zerind': 75, 'Timisoara': 118}, 'parent': None},
        'Timisoara': {'neighbors': {'Lugoj': 11, 'Arad': 118}, 'parent': None},
        'Lugoj': {'neighbors': {'Timisoara': 111, 'Mehadia': 70}, 'parent': None},
        'Mehadia': {'neighbors': {'Lugoj': 70, 'Dobreta': 75}, 'parent': None},
        'Dobreta': {'neighbors': {'Mehadia': 75, 'Craiova': 120}, 'parent': None},
        'Craiova': {'neighbors': {'Dobreta':120 ,'Rimnicu Vilcea': 146, 'Pitesti': 138}, 'parent': None},
        'Rimnicu Vilcea': {'neighbors': {'Sibiu': 80, 'Craiova': 146,'Pitesti':97}, 'parent': None},
        'Pitesti': {'neighbors': {'Craiova':138 , 'Bucharest': 101, 'Rimnicu Vilcea': 97}, 'parent': None},
        'Giurgiu': {'neighbors': {'Bucharest': 90}, 'parent': None}
    }
    posicion = {
        'Arad': 366,
        'Bucharest': 0,
        'Craiova':  160,
        'Dobreta': 242,
        'Eforie': 161,
        'Fagaras': 176,
        'Giurgiu': 77,
        'Hirsova': 151,
        'Lasi': 226,
        'Lugoj': 244,
        'Mehadia': 241,
        'Neamt': 234,
        'Oradea': 380,
        'Pitesti': 100,
        'Rimnicu Vilcea': 193,
        'Sibiu': 253,
        'Timisoara': 329,
        'Urziceni': 80,
        'Vaslui': 199,
        'Zerind': 374
    }

    start_node = 'Zerind'
    goal_node = 'Bucharest'
    tree = a_star(start_node, goal_node, graph, posicion)
    #agregamos el dato de la distancia entre esas ciudades
    weight=[]
    for i in range(len(tree)-1):
        weight.append(graph[tree[i]]['neighbors'][tree[i+1]])
    #cambiamos el formato de la informacion para graficar
    edges = []
    for i in range(len(tree)):
        if i<len(weight):
            edges.append((tree[i], tree[i+1], {'weight': weight[i]}))
        
    G = nx.Graph()
    G.add_nodes_from(tree)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    # Dibujamos el grafo con las aristas y los pesos de las aristas
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=1)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Mostramos el grafo
    plt.axis('off')
    plt.show()

