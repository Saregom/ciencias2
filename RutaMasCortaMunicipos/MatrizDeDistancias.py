import pandas as pd

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


csv_df = pd.read_csv('conexiones.csv')
coordenates = pd.read_json('coordenates.json')

# Función para obtener las coordenadas de una ciudad
def create_coordenates():
    geolocator = Nominatim(user_agent="geoapiExercises")
    coordenates_dicc = {}
    for municipio in csv_df.iloc[:, 0]:
        location = geolocator.geocode(f"{municipio}, Colombia")
        if location:
            coordenates_dicc[municipio] = (location.latitude, location.longitude)
        else:
            print(f"No se encontraron coordenates para {municipio}")
    return coordenates_dicc

# pd.DataFrame(create_coordenates()).to_json('coordenates.json')

# Función para calcular la distancia entre dos ciudades
def calculate_distance(city1_name, city2_name):
    city1_coords = coordenates[city1_name]
    city2_coords = coordenates[city2_name]
    distance = geodesic(city1_coords, city2_coords).kilometers
    return distance

# ver conexiones por fila
matriz_adyacencia = pd.DataFrame(index=csv_df.iloc[:, 0], columns=csv_df.columns[1:], data=0, dtype=float)

for index, row in csv_df.iterrows():
    municipio = row.iloc[0]
    print(f"Municipio: {municipio}")
    for i, conexion in enumerate(row[1:]):
        municipio_conectado = csv_df.columns[i + 1]
        if conexion == 1:
            print(f"  Conectado con: {municipio_conectado}")
            distancia = calculate_distance(municipio, municipio_conectado)
            matriz_adyacencia.at[municipio, municipio_conectado] = distancia

print(matriz_adyacencia)
# coordenates_df = pd.DataFrame(coordenates)
matriz_adyacencia.to_csv('distances.csv')