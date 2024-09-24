import csv
import json

def calculate_weight():
    # Cargar el archivo JSON con los atributos
    with open('Graph/data_graph.json', 'r') as jsonfile:
        atributos = json.load(jsonfile)

    # Leer la matriz del archivo CSV
    with open('Graph/connections.csv', newline='') as csvfile:
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

    # Calculo del peso de la arista segun atributos de los nodos(routers) (sin decimas)
    for i in range(1, len(matriz)): 
        show_message_failure = True
        for j in range(1, len(matriz[i])):
            if matriz[i][j] == 1:
                activo = 1
                ancho_banda_i = atributos[str(i)]['ancho de banda']
                ancho_banda_j = atributos[str(j)]['ancho de banda']
                ecolamineto_i = atributos[str(i)]['capacidad de encolamiento']
                ecolamineto_j = atributos[str(i)]['capacidad de encolamiento']
                activo_i = atributos[str(i)]['activo']
                activo_j = atributos[str(j)]['activo']
                promedio_encolamiento = (ecolamineto_i+ecolamineto_j) / 2 
                promedio_ancho_banda = (ancho_banda_i + ancho_banda_j) / 2

                if not atributos[str(i)]['activo'] and show_message_failure:
                    show_message_failure = False
                    print(f"El router #{i} se ha caido")

                if not activo_i or not activo_j:
                    activo = 0
                
                matriz[i][j] = ((1/promedio_ancho_banda) + (1/promedio_encolamiento)) * activo

    with open('Graph/connection_weights.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matriz)
