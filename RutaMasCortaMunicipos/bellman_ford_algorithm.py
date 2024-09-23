import pandas as pd

df = pd.read_csv('data/distances.csv', index_col=0)
cities = df.columns.tolist()
distance_matrix = df.to_numpy() # Matriz de distancias sin nombres de ciudades

def bellman_ford(distance_matrix, origin_city):
    num_cities = len(distance_matrix)
    distances = [float('inf')] * num_cities
    predecessors = [-1] * num_cities
    distances[origin_city] = 0

    # Relajacion de las aristas
    for i in range(num_cities - 1):
        for j in range(num_cities):
            for k in range(num_cities):
                if distance_matrix[j][k] != 0:
                    if distances[j] + distance_matrix[j][k] < distances[k]:
                        distances[k] = distances[j] + distance_matrix[j][k]
                        predecessors[k] = j

    # Deteccion de ciclos de peso negativo. Como no hay distancias negativas, no es necesario
    # for j in range(num_cities):
    #     for k in range(num_cities):
    #         if distance_matrix[j][k] != 0 and distances[j] + distance_matrix[j][k] < distances[k]:
    #             raise ValueError("The graph contains a negative weight cycle")

    return distances, predecessors

# Reconstruir el camino desde el predecesor
def reconstruct_path(predecessors, origin_city, destination_city):
    path = []
    current = destination_city
    while current != -1:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    
    if path[0] == origin_city:
        return path
    else:
        return []  # No hay camino
    
# Devuelve el formato (ciudad1, ciudad2, peso) para mostrar en mapa
def bellman_ford_algorithm():
    origin_city = 'Leticia'
    destination_city = 'Medellín'
    origin_city_index = cities.index(origin_city)
    distances, predecessors = bellman_ford(distance_matrix, origin_city_index)


    # Mostrar distancias y caminos
    for i, distance in enumerate(distances):
        path = reconstruct_path(predecessors, origin_city_index, i)
        path_cities = [cities[c] for c in path]
        if path_cities[-1] == destination_city:
            conections_list = []
    
            for i in range(len(path_cities) - 1):
                conections_list.append((path_cities[i], path_cities[i + 1], distance))
            print(distance)
            return conections_list
        
    return False
    
    
# Si se ejecuta el script de forma independiente para mostrar los caminos para cada ciudad
if __name__ == "__main__":
    origin_city = 'Leticia'
    origin_city_index = cities.index(origin_city)

    #distances, predecessors = bellman_ford(distance_matrix, cities.index(origin_city))
    a = bellman_ford_algorithm()
    print(a)
    # Mostrar distancias y caminos
    
