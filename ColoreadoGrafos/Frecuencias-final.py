import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button, Slider, TextBox

class GraphColoring:
    def __init__(self):
        self.frecuencies_matrix = pd.read_csv('frecuencias.csv', header=None).values
        self.n = self.frecuencies_matrix.shape[0]
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.radius = 10
        self.points = self.create_points()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.3)
        self.sliders = []
        self.create_sliders()
        self.create_button()
        self.input_box_n_coloring = []
        self.create_input_box()
        self.create_button2()
        self.create_button3()
        self.node_labels = list(range(1, self.n + 1))
        self.max_matching_edges = []
        self.minimum_colors = 3
        self.color_map = ['green', 'blue', 'red', 'orange', 'purple', 'cyan', 'lime', 'magenta', 'yellow', 'pink']
        self.colors = self.get_coloracion(self.adjacency_matrix)
        self.draw_graph()
        plt.show()

    def get_adjacency_matrix(self, matrix):
        num_filas, num_columnas = matrix.shape
        adjacency_matrix = np.zeros((num_filas, num_columnas))
        for i, frecuencies in enumerate(matrix):
            for j, frecuency in enumerate(frecuencies):
                if frecuency < 150 and frecuency != 0:
                    adjacency_matrix[i,j] = 1
        return adjacency_matrix
    
    
    # ------ COLORACION ------
    # algoritmo para obtener la coloración minima de los nodos
    def get_coloracion(self, adjacency_matrix1):
        colors = [-1] * self.n
        available_colors = [0] * self.n
        for node in range(self.n):
            for neighbor in range(self.n):
                if adjacency_matrix1[node, neighbor] == 1 and colors[neighbor] != -1:
                    available_colors[colors[neighbor]] = 1
            for color in range(self.n):
                if available_colors[color] == 0:
                    colors[node] = color
                    break
            available_colors = [0] * self.n

        # solo para mostrar el número de colores
        self.minimum_colors = len(set(colors)) - colors.count(-1)
        self.input_box_n_coloring[0].set_val(str(self.minimum_colors))
        print(f'- Minimum Colors: {self.minimum_colors}')

        return colors
    
    # se calcula la probabilidad de la n-coloración optima y se muestra en consola
    def calculate_coloring_probability(self, n, colors):
        promedios = np.zeros(n)
        for i in range(n):
            promedios[i] = np.mean(self.frecuencies_matrix[i, np.arange(n) != i])

        no_conectados = []
        for i in range(n):
            for j in range(i + 1, n):
                if self.adjacency_matrix[i, j] == 0:
                    no_conectados.append((i, j))
        
        multiplicaciones_promedios = [promedios[i] * promedios[j] for i, j in no_conectados]

        suma_multiplicada = sum(multiplicaciones_promedios)

        pares_mismo_color = []
        for i in range(n):
            for j in range(i + 1, n):
                if colors[i] == colors[j]:
                    pares_mismo_color.append((i, j))

        probabilidades_mismo_color = []
        for i, j in pares_mismo_color:
            probabilidad = (promedios[i] * promedios[j]) / suma_multiplicada
            probabilidades_mismo_color.append(probabilidad)

        probabilidad_coloreado = 1
        for i in probabilidades_mismo_color:
            probabilidad_coloreado *= 1 - round(i, 3)
        
        try:
            print(f'\n- La probabilidad del {self.input_box_n_coloring[0].text}-Coloreado optimo es:', round(probabilidad_coloreado, 3))
        except:
            print(f'\n- La probabilidad del {self.minimum_colors}-Coloreado optimo es:', round(probabilidad_coloreado, 3))

    # coloracion optima de los nodos para saber la probabilidad de la coloracion
    def get_optimal_n_coloring(self, num_colors): # Se especifica el numero de colores minimos (aumentar la cantidad de colores para mayor variedad)
        colors = [-1] * self.n  # Inicializa todos los nodos sin color
        adjacency_matrix = self.adjacency_matrix

        def is_safe_to_color(node, color):
            for neighbor in range(self.n):
                if adjacency_matrix[node][neighbor] == 1 and colors[neighbor] == color:
                    return False
            return True

        def color_graph(node, used_colors):
            if node == self.n:  # Si todos los nodos están coloreados
                # Verifica que se hayan utilizado exactamente 'num_colors'
                if len(set(colors)) == num_colors:
                    return True
                return False

            for color in range(num_colors):
                if is_safe_to_color(node, color):
                    colors[node] = color  # Asigna un color temporal
                    if color_graph(node + 1, used_colors | {color}):  # Intenta colorear el siguiente nodo
                        return True
                    colors[node] = -1  # Retrocede si no es posible

            return False

        if color_graph(0, set()):
            self.calculate_coloring_probability(self.n, colors)
            # print(f"El grafo se coloreó exitosamente con exactamente {num_colors} colores.")
            return colors
        else:
            print(f"\n----- ¡ No se puede colorear el grafo con", num_colors, "colores. ! -----\n")
            return [-1] * self.n  # Devuelve colores inválidos si no es posible
    
    # Emparejamiento 
    def get_matching(self):
        visited = [False] * self.n
        matching = []
        color_counter = max(self.colors) + 1  # Comenzar con un nuevo color para las parejas

        # Explorar las conexiones de cada nodo
        for u in range(self.n):
            if not visited[u]:
                for v in range(self.n):
                    # Si existe una conexión y ambos nodos no han sido emparejados
                    if self.adjacency_matrix[u, v] == 1 and not visited[v]:
                        matching.append((u, v))  # Añadir el par al emparejamiento
                        visited[u] = True  # Marcar nodos como visitados
                        visited[v] = True

                        # Asignar un color único a la pareja
                        self.colors[u] = color_counter
                        self.colors[v] = color_counter
                        color_counter += 1  # Incrementar el contador para el siguiente color
                        break

        # Guardar los emparejamientos en el atributo para dibujarlos
        self.max_matching_edges = matching

    # ------ EVENTOS ------
    # se llama al oprimir boton para agregar un nodo
    def add_node(self, event):
        self.n += 1
        self.node_labels.append(self.n)
        self.points = self.create_points()
        self.adjacency_matrix = np.pad(self.adjacency_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.colors.append(-1)
        self.frecuencies_matrix = np.pad(self.frecuencies_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.update_frequencies()
        self.create_sliders()  # Recreate sliders
        self.draw_graph()

    def update_frequencies(self):
        for i in range(self.n-1):
            self.frecuencies_matrix[self.n-1, i] = self.sliders[i].val
            self.frecuencies_matrix[i, self.n-1] = self.sliders[i].val
        pd.DataFrame(self.frecuencies_matrix).to_csv('frecuencias.csv', header=False, index=False)
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.colors = self.get_coloracion(self.adjacency_matrix)

    # se llama al oprimir boton para crear la coloración optima
    def update_coloring(self, event):
        try:
            num_colors = int(self.input_box_n_coloring[0].text)  # Convertir el texto a número
            self.colors = self.get_optimal_n_coloring(num_colors)
            self.draw_graph()
        except ValueError:
            print("Please enter a valid number.")

    # se llama al oprimir boton para encontrar el emparejamiento maximo
    def find_matching(self, event):
        self.get_matching()
        self.draw_graph()

    # ------ CREACION DE LA INTERFAZ GRAFICA ------
    def create_points(self): # Crear puntos para graficar (distribuidos en un círculo para visualización)    
        theta = np.linspace(0, 2 * np.pi, self.n, endpoint=False)
        return np.vstack((self.radius * np.cos(theta), self.radius * np.sin(theta))).T

    def draw_graph(self):
        self.ax.clear()
        for i in range(self.n):
            self.ax.plot(self.points[i, 0], self.points[i, 1], 'o', color=self.color_map[self.colors[i]], markersize=20)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adjacency_matrix[i, j] == 1:
                    color = 'red' if (i, j) in self.max_matching_edges or (j, i) in self.max_matching_edges else 'gray'
                    self.ax.plot([self.points[i, 0], self.points[j, 0]], [self.points[i, 1], self.points[j, 1]], color=color)
        for i in range(len(self.points)):
            self.ax.annotate(
                self.node_labels[i], self.points[i, :],
                color='white', fontsize="large", weight='heavy',
                horizontalalignment='center', verticalalignment='center'
            )
        
        self.ax.axis('off')
        self.ax.set_aspect('equal', adjustable='box')
        plt.draw()

    def create_button(self):
        ax_button = plt.axes([0.75, 0.11, 0.1, 0.075])
        self.btn = Button(ax_button, 'Add Node')
        self.btn.on_clicked(self.add_node)

    def create_sliders(self):
        for slider in self.sliders:
            slider.ax.remove()
        self.sliders = []
        for i in range(self.n):
            ax_slider = plt.axes([0.2, 0.07 + i * 0.03, 0.5, 0.015], facecolor='lightgoldenrodyellow')
            slider = Slider(ax_slider, f'Distance to Node {i+1}: ', 0, 300, valinit=0)
            self.sliders.append(slider)

    def create_input_box(self):
        ax_input = plt.axes([0.291, 0.02, 0.05, 0.03])  # Posición para el input
        input_box = TextBox(ax_input, 'Number for optimal N-Coloring: ', initial='3')
        self.input_box_n_coloring.append(input_box)

    def create_button2(self):
        ax_button = plt.axes([0.38, 0.02, 0.2, 0.03])
        self.btn2 = Button(ax_button, 'Create N-Coloring')
        self.btn2.on_clicked(self.update_coloring)

    def create_button3(self):
        ax_button = plt.axes([0.6, 0.02, 0.2, 0.03])
        self.btn3 = Button(ax_button, 'Find Max Matching')
        self.btn3.on_clicked(self.find_matching)

if __name__ == "__main__":
    GraphColoring()
