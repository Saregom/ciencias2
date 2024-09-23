import numpy as np
import pandas as pd
import json
from MatrizDeDistancias import calculate_distance
import csv 
import heapq


def cargar_distancias(nombre_archivo):
    ciudades = []
    distancias = []
    
    with open("data/distances.csv", 'r') as archivo:
        reader = csv.reader(archivo)
        # Saltar la primera fila (cabecera)
        next(reader)
        
        for row in reader:
            # La primera columna contiene los nombres de las ciudades
            ciudades.append(row[0])
            # Convertir el resto de la fila en distancias, ignorando la primera columna
            distancias.append([float(x) if x != '' else float('inf') for x in row[1:]])
    
    return ciudades, distancias


# Algoritmo de Dijkstra
def dijkstra(origen, destino, ciudades, distancias):
    num_ciudades = len(ciudades)
    visitados = [False] * num_ciudades
    distancias_min = [float('inf')] * num_ciudades
    distancias_min[ciudades.index(origen)] = 0
    predecesores = [None] * num_ciudades
    
    for _ in range(num_ciudades):
        # Encuentra la ciudad con la distancia mínima
        min_distancia = float('inf')
        min_indice = -1
        for i in range(num_ciudades):
            if not visitados[i] and distancias_min[i] < min_distancia:
                min_distancia = distancias_min[i]
                min_indice = i

        # Marca la ciudad como visitada
        visitados[min_indice] = True

        # Actualiza las distancias para las ciudades adyacentes
        for i in range(num_ciudades):
            if distancias[min_indice][i] > 0 and not visitados[i]:
                nueva_distancia = distancias_min[min_indice] + distancias[min_indice][i]
                if nueva_distancia < distancias_min[i]:
                    distancias_min[i] = nueva_distancia
                    predecesores[i] = min_indice

    # Reconstruir el camino
    camino = []
    actual = ciudades.index(destino)
    if distancias_min[actual] == float('inf'):
        return [], float('inf')
    
    while actual is not None:
        camino.insert(0, ciudades[actual])
        actual = predecesores[actual]
    
    return camino, distancias_min[ciudades.index(destino)]

def encontrar_y_visualizar_camino(ciudad_origen, ciudad_destino, data):
    archivo_distancias = "distances.csv"
    ciudades, distancias = cargar_distancias(archivo_distancias)
    camino, distancia_total = dijkstra(ciudad_origen, ciudad_destino, ciudades, distancias)
    
       
    print(f"El camino más corto de {ciudad_origen} a {ciudad_destino} es:")
    print(" -> ".join(camino))
    print(f"Distancia total: {distancia_total:.2f} km")
        
        # Generar aristas para visualización
    aristas = []
    for i in range(len(camino) - 1):
            ciudad_1 = camino[i]
            ciudad_2 = camino[i+1]
            peso = distancias[ciudades.index(ciudad_1)][ciudades.index(ciudad_2)]
            aristas.append((ciudad_1, ciudad_2, peso))
        
        # Llamar a la función de visualización
    return aristas, data

