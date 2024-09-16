import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Algoritmo_kruskal import kruskal_algoritm
from Algoritmo_prim import prim_algoritm

with open('data/coordenates.json', encoding='utf-8') as f:
    data = json.load(f)
matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)

def visualizar(aristas):
    # aristas = kruskal_algoritm(matriz_adyacencia)
    # aristas = prim_algoritm(matriz_adyacencia)
    # Extraer las coordenadas y nombres de los municipios
    municipios = list(data.keys())
    #print(municipios)
    latitudes = [data[municipio]['latitude'] for municipio in municipios]
    longitudes = [data[municipio]['longitude'] for municipio in municipios]

    # Crear un mapa usando las coordenadas
    fig = px.scatter_mapbox(
        lat=latitudes,
        lon=longitudes,
        text=municipios,  # Mostrar el nombre del municipio
        zoom=5,  # Nivel de zoom
        mapbox_style="open-street-map"  # Estilo del mapa
    )

    # Añadir las aristas al mapa (conexiones entre municipios)
    for arista in aristas:
        ciudad_1, ciudad_2, peso= arista
        
        # Extraer las coordenadas si ambas ciudades existen
        lat_1, lon_1 = data[ciudad_1]['latitude'], data[ciudad_1]['longitude']
        lat_2, lon_2 = data[ciudad_2]['latitude'], data[ciudad_2]['longitude']
        
        # Agregar una línea entre las dos ciudades en el mapa
        fig.add_trace(go.Scattermapbox(
            lat=[lat_1, lat_2],
            lon=[lon_1, lon_2],
            mode='lines',
            line=dict(width=2, color='blue'),  
            name=f"{ciudad_1} - {ciudad_2}"  
        ))
    # Configurar el layout del mapa
    fig.update_layout(
        title="Mapa de Municipios en Colombia",
        mapbox=dict(center=dict(lat=4.6, lon=-74.0))  # Centrando el mapa en Colombia
    )

    # Mostrar el mapa
    fig.show()

if __name__ == "__main__":
    print("Elige el algoritmo a utilizar:")
    print("1. Kruskal")
    print("2. Prim")
    
    choice = input("Ingresa el número de la opción deseada: ")
    
    if choice == '1':
        mst = kruskal_algoritm(matriz_adyacencia)
        visualizar(mst)
    elif choice == '2':
        mst = prim_algoritm(matriz_adyacencia)
        visualizar(mst)
    else:
        print("Opción no válida.")
        mst = []
    
