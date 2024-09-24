import csv
import json

# Cargar el archivo JSON con los atributos
with open('data_graph.json', 'r') as jsonfile:
    atributos = json.load(jsonfile)

# Leer la matriz del archivo CSV
with open('connections.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    matriz = []
    for row in reader:
        fila = []
        for value in row:
            if value.strip(): 
                fila.append(int(value)) 
            else:
                fila.append(0)  
        matriz.append(fila)

# Promedio de ancho de banda entero (sin decimas)
for i in range(1, len(matriz)):  # se salta el encabezado
    for j in range(1, len(matriz[i])):
        if matriz[i][j] == 1:
            
            ancho_banda_i = atributos[str(i)]['ancho de banda']
            ancho_banda_j = atributos[str(j)]['ancho de banda']
            promedio_ancho_banda = (ancho_banda_i + ancho_banda_j) // 2
            matriz[i][j] = promedio_ancho_banda

with open('banda_ancha_promedios.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(matriz)