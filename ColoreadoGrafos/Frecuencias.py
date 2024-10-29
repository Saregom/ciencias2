import numpy as np
import matplotlib.pyplot as plt

# Se crea la matriz inicial de frecuencias
frecuencies_matrix = np.array([[0,85,175,200,50,100], 
                              [85,0,125,175,100,160], 
                              [175,125,0,100,200,250], 
                              [200,175,100,0,210,220],
                              [50,100,200,210,0,100],
                              [100,160,250,220,100,0]])

# Se crea la matriz de adyacencia (de conexiones) a partir de la matriz de frecuencias
n = 6
adjacency_matrix = np.zeros((n,n))

for i, frecuencies in enumerate(frecuencies_matrix):
    for j, frecuency in enumerate(frecuencies):
        if frecuency < 150 and frecuency != 0:
             adjacency_matrix[i,j] = 1

# Crear puntos para graficar (distribuidos en un círculo para visualización)
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
radius = 10
points = np.vstack((radius * np.cos(theta), radius * np.sin(theta))).T


# Colores de los grafos
colors = [-1] * n  # Inicialmente sin color (-1)
available_colors = [0] * n  # Lista para controlar colores disponibles

for node in range(n):
    # Marcar los colores de los nodos vecinos como no disponibles
    for neighbor in range(n):
        if adjacency_matrix[node, neighbor] == 1 and colors[neighbor] != -1:
            available_colors[colors[neighbor]] = 1

    # Asignar el primer color disponible
    for color in range(n):
        if available_colors[color] == 0:
            colors[node] = color
            break

    # Reiniciar la lista de colores disponibles para el siguiente nodo
    available_colors = [0] * n

# Definir una lista de colores (puedes agregar más si hay más nodos)
color_map = ['green', 'blue', 'red', 'pink', 'orange', 'purple']

plt.figure(figsize=(8, 8))
for i in range(n):
    plt.plot(points[i, 0], points[i, 1], 'o', color=color_map[colors[i]], markersize=20)

# Dibujar conexiones de acuerdo a la matriz de adyacencia
for i in range(n):
    for j in range(i + 1, n):
        if adjacency_matrix[i, j] == 1:
            plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], color="gray")

# Etiquetar puntos
for i in range(len(points)):
    plt.annotate(
        i+1, points[i, :],
        color='white', fontsize="large", weight='heavy',
        horizontalalignment='center', verticalalignment='center'
    )
plt.axis('off')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
