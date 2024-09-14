import heapq
import pandas as pd
from MatrizDeDistancias import calculate_distance 

coordenates = pd.read_json('data/coordenates.json')
matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)


def prim_algoritm(matriz_adyacencia):
    # Inicializamos las estructuras
    num_cities = len(matriz_adyacencia)
    visited = set()  # Conjunto de ciudades visitadas
    min_heap = []  # Cola de prioridad para elegir la arista de menor peso
    mst = []  # Lista de aristas que formarán el árbol de expansión mínima (MST)
    
    # Empezamos desde la primera ciudad (puede ser cualquier ciudad)
    start_city = matriz_adyacencia.index[0]
    visited.add(start_city)
    
    # Insertamos las aristas conectadas a la primera ciudad en la cola de prioridad
    for neighbor in matriz_adyacencia.columns:
        if matriz_adyacencia.loc[start_city, neighbor] > 0:  # Ignorar conexiones de peso 0
            heapq.heappush(min_heap, (matriz_adyacencia.loc[start_city, neighbor], start_city, neighbor))
    
    # Mientras no hayamos visitado todas las ciudades
    while len(visited) < num_cities and min_heap:
        # Extraemos la arista con menor peso
        weight, city1, city2 = heapq.heappop(min_heap)
        
        if city2 not in visited:
            # Agregamos la arista al MST
            mst.append((city1, city2, weight))
            visited.add(city2)
            
            # Insertamos las nuevas aristas del nodo recién añadido
            for neighbor in matriz_adyacencia.columns:
                if matriz_adyacencia.loc[city2, neighbor] > 0 and neighbor not in visited:
                    heapq.heappush(min_heap, (matriz_adyacencia.loc[city2, neighbor], city2, neighbor))
    
    return mst

if __name__ == "__main__":
    mst = prim_algoritm(matriz_adyacencia)
    print("Árbol de expansión mínima (MST):")
    for edge in mst:
        print(f"{edge[0]} -- {edge[1]} : {edge[2]}")
