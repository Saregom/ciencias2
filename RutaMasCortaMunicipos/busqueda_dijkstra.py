import pandas as pd

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


csv_df = pd.read_csv('conexiones.csv')

coordenates = {}

# Función para obtener las coordenadas de una ciudad
def create_coordenates():
    geolocator = Nominatim(user_agent="geoapiExercises")
    coordenates = {}
    for municipio in csv_df.iloc[:, 0]:
        location = geolocator.geocode(f"{municipio}, Colombia")
        if location:
            coordenates[municipio] = (location.latitude, location.longitude)
        else:
            print(f"No se encontraron coordenates para {municipio}")
    return

create_coordenates()
print(coordenates)
coordenates_df = pd.DataFrame(coordenates)

#coordenates_df.to_json('coordenates.json')



# Función para calcular la distancia entre dos ciudades
def calculate_distance(city1_name, city2_name):
    city1_coords = coordenates[city1_name]
    city2_coords = coordenates[city2_name]
    distance = geodesic(city1_coords, city2_coords).kilometers
    return distance


# csv_df.head()

conexiones = 0

matriz_adyacencia = pd.DataFrame(index=csv_df.iloc[:, 0], columns=csv_df.columns[1:], data=0)
"""
# ver conexiones por fila
for index, row in csv_df.iterrows():
    municipio = row[0]
    print(f"Municipio: {municipio}")
    for i, conexion in enumerate(row[1:]):
        municipio_conectado = csv_df.columns[i + 1]
        if conexion == 1:
            print(f"  Conectado con: {municipio_conectado}")
            distancia = calculate_distance(municipio, municipio_conectado)
            matriz_adyacencia.at[municipio, municipio_conectado] = distancia
"""

#print(matriz_adyacencia)