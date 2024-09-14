import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

csv_df = pd.read_csv('data/conexiones2.csv')
coordenates = pd.read_json('data/coordenates2.json')

# Función para obtener las coordenadas de una ciudad
def create_coordenates():
    geolocator = Nominatim(user_agent="geoapi") # Si sale error: Reemplazar "geoapi" por caulquier otra palabra
    coordenates_dicc = {}
    for municipio in csv_df.iloc[:, 0]:
        location = geolocator.geocode(f"{municipio}, Colombia")
        if location:
            coordenates_dicc[municipio] = {"latitude": location.latitude, "longitude": location.longitude}
        else:
            print(f"No se encontraron coordenates para {municipio}")
    return coordenates_dicc

# pd.DataFrame(create_coordenates()).to_json('data/coordenates2.json', force_ascii=False)


# Función para calcular la distancia entre dos ciudades
def calculate_distance(city1_name, city2_name):
    city1_coords = coordenates[city1_name]
    city2_coords = coordenates[city2_name]
    distance = geodesic(city1_coords, city2_coords).kilometers
    return distance

if __name__ == "__main__":
    # ver conexiones por fila
    matriz_adyacencia = pd.DataFrame(index=csv_df.iloc[:, 0], columns=csv_df.columns[1:], data=0.0)

    # Llenar la matriz de adyacencia con las distancias entre los municipios conectados
    for index, row in csv_df.iterrows():
        municipio = row.iloc[0]
        # print(f"Municipio: {municipio}")
        for i, conexion in enumerate(row[1:]):
            municipio_conectado = csv_df.columns[i + 1]
            if conexion == 1:
                # print(f"  Conectado con: {municipio_conectado}")
                distancia = calculate_distance(municipio, municipio_conectado)
                matriz_adyacencia.at[municipio, municipio_conectado] = distancia
        # print("----------------------------------------------\n") 

    matriz_adyacencia = matriz_adyacencia.astype(float)
    # matriz_adyacencia.to_csv('data/distances2.csv')
    # print("| Matriz Adyacente de los Municipios |\n")
    # print(matriz_adyacencia)