import numpy as np
import pandas as pd
from MatrizDeDistancias import calculate_distance

coordenates = pd.read_json('data/coordenates.json')
matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)
matriz__whitout_0 = matriz_adyacencia.replace(0, np.nan)

# Funciones auxiliares para conjuntos disjuntos (union-find)
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    
    if root_x != root_y:
        if rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        elif rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

# Algoritmo de Kruskal corregido
def kruskal_algoritm(matriz_adyacencia):
    # Lista de aristas (i, j, peso)
    edges = []
    for i in matriz_adyacencia.index:
        for j in matriz_adyacencia.columns:
            value = matriz_adyacencia.loc[i, j]
            if value != 0 and not np.isnan(value):
                edges.append((i, j, value))
    
    # Ordenamos las aristas por peso
    edges.sort(key=lambda edge: edge[2])

    # Inicializamos estructuras para union-find
    parent = {}
    rank = {}
    
    for node in matriz_adyacencia.index:
        parent[node] = node
        rank[node] = 0

    mst = []
    for edge in edges:
        i, j, weight = edge
        if find(parent, i) != find(parent, j):
            mst.append(edge)
            union(parent, rank, i, j)
        
        if len(mst) == len(matriz_adyacencia.index) - 1:
            break

    return mst

if __name__ == "__main__":
    mst = kruskal_algoritm(matriz_adyacencia)
    # print("Árbol de expansión mínima (MST):")
    # for edge in mst:
    #     print(f"{edge[0]} -- {edge[1]} : {edge[2]}")
