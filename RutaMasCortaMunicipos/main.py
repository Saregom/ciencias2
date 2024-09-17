import json
import plotly.express as px


with open('data/coordenates.json') as f:
    data = json.load(f)

# Extraer las coordenadas y nombres de los municipios
municipios = list(data.keys())
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

# Configurar el layout del mapa
fig.update_layout(
    title="Mapa de Municipios en Colombia",
    mapbox=dict(center=dict(lat=4.6, lon=-74.0))  # Centrando el mapa en Colombia
)

# Mostrar el mapa
fig.show()
