import heapq
import pandas as pd
from MatrizDeDistancias import calculate_distance 

coordenates = pd.read_json('data/coordenates.json')
matriz_adyacencia = pd.read_csv('data/distances.csv', index_col=0)

start_city = "Leticia"
end_city = "Riohacha"

def greedy_best_first_search_hn(start_city, end_city):
    open_list = []  # Lista de nodos por explorar
    closed_list = set()  # Lista de nodos ya explorados
    heapq.heappush(open_list, (0, start_city))  # Iniciar con la ciudad de origen
    came_from = {}
    g_score = {city: float('inf') for city in matriz_adyacencia.index}  # Para almacenar las distancias
    g_score[start_city] = 0  # La distancia desde la ciudad de inicio es 0

    while open_list:
        # Obtener el nodo con la menor heurística (más cercano al objetivo)
        _, current_city = heapq.heappop(open_list)

        # Si ya hemos visitado esta ciudad, continuar
        if current_city in closed_list:
            continue

        # Añadir a la lista cerrada
        closed_list.add(current_city)

        # Si llegamos a la ciudad destino
        if current_city == end_city:
            total_path = [current_city]
            total_distance = g_score[current_city]  # Distancia total hasta la ciudad destino
            while current_city in came_from:
                current_city = came_from[current_city]
                total_path.append(current_city)
            return total_path[::-1], g_score, total_distance  # Retorna el camino y la distancia total

        # Explorar los vecinos
        for neighbor in matriz_adyacencia.columns:
            if matriz_adyacencia.at[current_city, neighbor] > 0:
                # Si el vecino ya fue explorado, no lo volvemos a evaluar
                if neighbor in closed_list:
                    continue
                
                # Calcular la heurística (distancia estimada hasta la meta)
                heuristic = calculate_distance(neighbor, end_city)

                # Si encontramos una mejor ruta hacia el vecino
                if neighbor not in [city for _, city in open_list]:
                    came_from[neighbor] = current_city
                    g_score[neighbor] = g_score[current_city] + matriz_adyacencia.at[current_city, neighbor]  # Acumula distancia
                    heapq.heappush(open_list, (heuristic, neighbor))

    return None, None  # No se encontró un camino

def a_star_algorithm(start_city, end_city):
    # Inicializar open_list y closed_list
    open_list = []
    heapq.heappush(open_list, (0, start_city))
    came_from = {}
    g_score = {city: float('inf') for city in matriz_adyacencia.index}
    g_score[start_city] = 0
    f_score = {city: float('inf') for city in matriz_adyacencia.index}
    f_score[start_city] = calculate_distance(start_city, end_city)
    total_distance = 0  # Variable para acumular la distancia total
    
    while open_list:
        _, current_city = heapq.heappop(open_list)

        # Si llegamos a la ciudad destino
        if current_city == end_city:
            total_path = [current_city]
            while current_city in came_from:
                previous_city = came_from[current_city]
                total_distance += matriz_adyacencia.at[previous_city, current_city]  # Suma la distancia
                current_city = previous_city
                total_path.append(current_city)
            return total_path[::-1], g_score, total_distance  # Devolvemos el camino y la distancia total

        # Ver todos los vecinos
        for neighbor in matriz_adyacencia.columns:
            if matriz_adyacencia.at[current_city, neighbor] > 0:
                tentative_g_score = g_score[current_city] + matriz_adyacencia.at[current_city, neighbor]
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_city
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + calculate_distance(neighbor, end_city)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, None  # No se encontró un camino

# Retornar formato (ciudad1, ciudad2, peso) para mostrar en mapa
def hn_a_algorithms(algorithm):
    if algorithm == 'greedy':
        path, distances, final_distance = greedy_best_first_search_hn(start_city, end_city)
    elif algorithm == 'a_star':
        path, distances, final_distance = a_star_algorithm(start_city, end_city)

    conections_list = []
    
    for i in range(len(path) - 1):
        conections_list.append((path[i], path[i + 1], distances[path[i + 1]]))

    return conections_list
    

if __name__ == "__main__":
    # Búsqueda voraz
    path_greedy, distances_greedy, final_distance_greedy = greedy_best_first_search_hn(start_city, end_city)
    if path_greedy:
        print(f"\nCamino encontrado por Búsqueda Voraz h(n) desde {start_city} a {end_city}: {path_greedy}")
        print(f"Distancia: {final_distance_greedy} km\n")
    else:
        print(f"No se encontró un camino de {start_city} a {end_city} con busqueda Voraz h(n)\n")

    # Búsqueda A*
    path_a, distances_a, final_distance_a = a_star_algorithm(start_city, end_city)
    if path_a:
        print(f"Camino encontrado por A* h(n) + g(n) desde {start_city} a {end_city}: {path_a}")
        print(f"Distancia: {final_distance_a} km\n")
    else:
        print(f"No se encontro un camino de {start_city} a {end_city} con busqueda A*\n")

