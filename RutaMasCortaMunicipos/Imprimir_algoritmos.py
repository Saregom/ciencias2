import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from Algoritmos_hn_a import greedy_best_first_search_hn
from Algoritmos_hn_a import a_star_algorithm
from Algoritmo_kruskal import kruskal_algoritm
from Algoritmo_prim import prim_algoritm
from bellman_ford_algorithm import bellman_ford_algorithm

with open('data/coordenates.json', encoding='utf-8') as f:
    data = json.load(f)

matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)

def visualize_map(aristas, choice):
    # Extraer las coordenadas y nombres de los municipios
    municipios = list(data.keys())
    latitudes = [data[municipio]['latitude'] for municipio in municipios]
    longitudes = [data[municipio]['longitude'] for municipio in municipios]

    # Crear mapa
    fig = go.Figure()

    # Añadir las aristas al mapa (conexiones entre municipios)
    for arista in aristas:
        ciudad_1, ciudad_2, peso = arista

        # Extraer las coordenadas si ambas ciudades existen
        lat_1, lon_1 = data[ciudad_1]['latitude'], data[ciudad_1]['longitude']
        lat_2, lon_2 = data[ciudad_2]['latitude'], data[ciudad_2]['longitude']
        
        # Agregar una línea entre las dos ciudades en el mapa
        trace = go.Scattermapbox(
            lat=[lat_1, lat_2],
            lon=[lon_1, lon_2],
            mode='lines',
            line=dict(width=2, color='blue')
        )

        if choice == '3':
            trace.name = f"{aristas[0][0]} - {ciudad_2}: {peso:.3f}"
        else:
            trace.name = f"{ciudad_1} - {ciudad_2}: {peso:.3f}"

        fig.add_trace(trace)

    # Añadir los municipios al mapa como puntos
    fig.add_trace(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        text=municipios,
        mode='markers',
        marker=dict(size=8, color='red'),
        hoverinfo='lat+lon+text',
        showlegend=False
    ))

    # Configurar el layout del mapa
    fig.update_layout(
        title = "Mapa de Municipios en Colombia",
        mapbox = dict(
            center=dict(lat=4.6, lon=-74.0),  # Centrando el mapa en Colombia
            style = "open-street-map",  # Estilo del mapa
            zoom = 5,  # Nivel de zoom
        )  
    )

    # Mostrar el mapa
    fig.show()

if __name__ == "__main__":
    print("Elige el algoritmo a utilizar:")
    print("1. Kruskal")
    print("2. Prim")
    print("3. Bellman-Ford")
    
    choice = input("Ingresa el número de la opción deseada: ")
    
    if choice == '1':
        visualize_map(kruskal_algoritm(matriz_adyacencia), choice)
    elif choice == '2':
        visualize_map(prim_algoritm(matriz_adyacencia), choice)
    elif choice == '3':
        visualize_map(bellman_ford_algorithm(), choice)
    else:
        print("Opción no válida.")
