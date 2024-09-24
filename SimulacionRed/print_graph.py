import csv
import networkx as nx
import matplotlib.pyplot as plt

# Leer la matriz de adyacencia desde el archivo CSV usando csv.reader
with open('Graph/connections.csv', newline='') as csvfile:
    df = csv.reader(csvfile)
    
    # Convertir el contenido de csv.reader a una lista de listas
    adjacency_matrix = list(df)

# Convertir la matriz de adyacencia a un grafo de NetworkX
G = nx.Graph()

# Recorrer la matriz y añadir aristas al grafo
for i, row in enumerate(adjacency_matrix):
    if i == 0:
        # Saltar la primera fila de etiquetas de nodos si es necesaria
        continue
    node = int(row[0])  # Primer valor de cada fila es el nodo
    for j, value in enumerate(row[1:], 1):  # Empezar desde la segunda columna
        if int(value) == 1:  # Si hay conexión (1), añadir una arista
            G.add_edge(node, j)

# Dibujar el grafo
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G)  # Elegir el layout (disposición de nodos)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
plt.title('Grafo desde la matriz de adyacencia')
plt.show()
