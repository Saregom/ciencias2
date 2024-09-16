import heapq
import numpy as np
import pandas as pd
from MatrizDeDistancias import calculate_distance
coordenates = pd.read_json('data/coordenates.json')
matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)
matriz__whitout_0 = matriz_adyacencia.replace(0, np.nan)
def less_score(matriz_adyacencia, visited):
    minim = 50000
    visited = []
    visited2 = []
    n=0
    arista = None
    while True:
        for i in matriz_adyacencia.index:
            for j in matriz_adyacencia.columns:
                value = matriz_adyacencia.loc[i,j]
                if value != 0 and value < minim and (i,j) not in visited and (j,i) not in visited and j not in visited2:
                    minim = value
                    arista = (i,j)
                    print(value)
                    print(f"Esto va desde {i} hasta {j}")
        visited.append(arista)
        visited2.append(arista[1])
        print(visited)
        print(visited2)
        print(len(visited2))
        minim = 50000
        n+=1
        if n == 30:
            break
    return False
def kruskal_algoritm(matriz_adyacencia):
    num_cities = len(matriz_adyacencia)
    visited = set()
    min_heap = []
    mst= []

    less_score(matriz_adyacencia, visited)

    # Entonces se empieza con una ciudad cualquiera 

    return False




if __name__ == "__main__":
    kruskal_algoritm(matriz_adyacencia)
    #mst = prim_algoritm(matriz_adyacencia)
    # print("Árbol de expansión mínima (MST):")
    # for edge in mst:
    #     print(f"{edge[0]} -- {edge[1]} : {edge[2]}")
