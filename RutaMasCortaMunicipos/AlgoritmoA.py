import pandas as pd
import heapq
from geopy.distance import geodesic
from MatrizDeDistancias import calculate_distance 

coordenates = pd.read_json('coordenates.json')
matriz_adyacencia = pd.read_csv('distances.csv', index_col=0)



"""
def a_star_algorithm(start_city, end_city):
    # Inicializar open_list y closed_list
    open_list = []
    heapq.heappush(open_list, (0, start_city))
    came_from = {}
    g_score = {city: float('inf') for city in matriz_adyacencia.index}
    g_score[start_city] = 0
    f_score = {city: float('inf') for city in matriz_adyacencia.index}
    f_score[start_city] = calculate_distance(start_city, end_city)
    
    while open_list:
        # Obtener el nodo con la menor f_score
        _, current_city = heapq.heappop(open_list)

        # Si llegamos a la ciudad destino, reconstruimos el camino
        if current_city == end_city:
            total_path = [current_city]
            while current_city in came_from:
                current_city = came_from[current_city]
                total_path.append(current_city)
            return total_path[::-1]  # Devolvemos el camino en orden correcto
        
        # Ver todos los vecinos
        for neighbor in matriz_adyacencia.columns:
            if matriz_adyacencia.at[current_city, neighbor] > 0:  # Si hay una conexión
                tentative_g_score = g_score[current_city] + matriz_adyacencia.at[current_city, neighbor]
                
                if tentative_g_score < g_score[neighbor]:
                    # Este camino es el mejor hasta ahora
                    came_from[neighbor] = current_city
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + calculate_distance(neighbor, end_city)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None  # No se encontró un camino

"""

def a_star_algorithm_pandas(start_city, end_city):
    # Inicializar las estructuras de datos necesarias
    open_list = pd.Series([float('inf')] * len(matriz_adyacencia), index=matriz_adyacencia.index)
    open_list[start_city] = 0
    came_from = pd.Series(index=matriz_adyacencia.index)
    g_score = pd.Series([float('inf')] * len(matriz_adyacencia), index=matriz_adyacencia.index)
    g_score[start_city] = 0
    f_score = pd.Series([float('inf')] * len(matriz_adyacencia), index=matriz_adyacencia.index)
    f_score[start_city] = calculate_distance(start_city, end_city)

    while not open_list.empty:
        # Seleccionar el nodo en open_list con el menor f_score
        current_city = open_list.idxmin()
        open_list.drop(current_city, inplace=True)

        # Si llegamos a la ciudad destino, reconstruimos el camino
        if current_city == end_city:
            total_path = [current_city]
            while not pd.isna(came_from[current_city]):
                current_city = came_from[current_city]
                total_path.append(current_city)
            return total_path[::-1]  # Devolvemos el camino en orden correcto

        # Ver todos los vecinos
        for neighbor in matriz_adyacencia.columns:
            if matriz_adyacencia.at[current_city, neighbor] > 0:  # Si hay una conexión (no es 0)
                tentative_g_score = g_score[current_city] + matriz_adyacencia.at[current_city, neighbor]

                if tentative_g_score < g_score[neighbor]:
                    # Este camino es el mejor hasta ahora
                    came_from[neighbor] = current_city
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + calculate_distance(neighbor, end_city)
                    open_list[neighbor] = f_score[neighbor]

    return None  # No se encontró un camino

start_city = "Bogotá"
end_city = "Monguí"
input(f"""
Las ciudades para el recorrido seran {start_city} y {end_city}, 
Dale Enter para continuar
""")
path = a_star_algorithm_pandas(start_city, end_city)
if path:
    print(f"Camino encontrado de {start_city} a {end_city}: {path}")
else:
    print(f"No se encontró un camino de {start_city} a {end_city}")