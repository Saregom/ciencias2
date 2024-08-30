import pandas as pd
csv_df = pd.read_csv('RutaMasCortaMunicipos/Conexiones.csv')
csv_df.head()

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="geoapiExercises")
coordenadas = {}
for municipio in csv_df.iloc[:, 0]:
    location = geolocator.geocode(f"{municipio}, Colombia")
    if location:
        coordenadas[municipio] = (location.latitude, location.longitude)
    else:
        print(f"No se encontraron coordenadas para {municipio}")

