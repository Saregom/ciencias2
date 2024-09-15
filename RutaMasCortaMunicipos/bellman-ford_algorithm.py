import pandas as pd

# Algoritmo de Bellman-Ford
def bellman_ford(distance_matrix, origin_city):
    num_cities = len(distance_matrix)
    distances = [float('inf')] * num_cities
    predecessors = [-1] * num_cities
    distances[origin_city] = 0

    # Relajación de las aristas
    for i in range(num_cities - 1):
        for j in range(num_cities):
            for k in range(num_cities):
                if distance_matrix[j][k] != 0:
                    if distances[j] + distance_matrix[j][k] < distances[k]:
                        distances[k] = distances[j] + distance_matrix[j][k]
                        predecessors[k] = j

    # Detección de ciclos de peso negativo. Como no hay distancias negativas, no es necesario
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

if __name__ == "__main__":
    # Cargar la matriz de distancias desde un archivo CSV
    df = pd.read_csv('data/distances2.csv', index_col=0)
    cities = df.columns.tolist()
    distance_matrix = df.to_numpy()

    origin_city = 'Bogotá'
    origin_city_index = cities.index(origin_city)

    distances, predecessors = bellman_ford(distance_matrix, origin_city_index)

    # Mostrar distancias y caminos
    print(f"\nDistancias desde {origin_city}:")
    for i, distance in enumerate(distances):
        if distance == float('inf'):
            print(f"{cities[i]}: No hay camino")
        else:
            path = reconstruct_path(predecessors, origin_city_index, i)
            path_cities = [cities[c] for c in path]
            print(f"{cities[i]}: {distance} {path_cities}")
