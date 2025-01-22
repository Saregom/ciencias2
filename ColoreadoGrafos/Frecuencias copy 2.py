import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button, Slider, TextBox

class GraphColoring:
    def __init__(self):
        self.frecuencies_matrix = pd.read_csv('frecuencias.csv', header=None).values
        self.n = self.frecuencies_matrix.shape[0]
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.input_box_n_coloring = []
        # self.colors = self.get_coloracion(self.adjacency_matrix)
        self.colors = self.get_optimal_n_coloring(3) # Se especifica el numero de colores minimos (aumentar la cantidad de colores para mayor variedad)
        self.color_map = ['green', 'blue', 'red', 'orange', 'purple', 'cyan', 'lime', 'magenta', 'yellow', 'pink']
        self.radius = 10
        self.points = self.create_points()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.3)
        self.sliders = []
        self.create_sliders()
        self.create_button()
        self.create_input_box()
        self.create_button2()
        self.node_labels = list(range(1, self.n + 1))
        self.min_colors_text = None
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
    # algoritmo para obtener la coloración de los nodos (minima) 
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
        min_colors = len(set(self.colors)) - self.colors.count(-1)
        print(f'- Minimum Colors: {min_colors}')

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
            print(f'\n- La probabilidad del 3-Coloreado optimo es:', round(probabilidad_coloreado, 3))

    
    def get_optimal_n_coloring(self, num_colors):
        colors = [-1] * self.n  # -1 representa nodos sin colorear

        # Heuristica para robustez: colorear con mayor diversidad
        try:
            for node in range(self.n):
                forbidden_colors = {
                    colors[j] for j in range(self.n) if self.get_adjacency_matrix(self.frecuencies_matrix)[node, j] == 1 and colors[j] != -1
                }
                # Asignar el color con menos frecuencia de uso para distribuir uniformemente la cantidad de colores
                color_usage = [colors.count(c) for c in range(num_colors)]
                available_colors = [
                    color for color in range(num_colors) if color not in forbidden_colors
                ]
                best_color = min(available_colors, key=lambda c: color_usage[c])
                colors[node] = best_color

            self.calculate_coloring_probability(self.n, colors)

        # excepcion si no se puede colorear con el numero de colores especificado
        except ValueError:
            print("\n----- ¡ No se puede colorear el grafo con", num_colors, "colores. ! -----\n")
            exit()

        return colors
    

    # ------ EVENTOS ------
    def add_node(self, event):
        print("Button pressed!") 
        
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
        # self.colors = self.get_optimal_n_coloring(3)

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
                    self.ax.plot([self.points[i, 0], self.points[j, 0]], [self.points[i, 1], self.points[j, 1]], color="gray")
        for i in range(len(self.points)):
            self.ax.annotate(
                self.node_labels[i], self.points[i, :],
                color='white', fontsize="large", weight='heavy',
                horizontalalignment='center', verticalalignment='center'
            )
        
        #if self.min_colors_text:
        #    self.min_colors_text.remove()
        #self.min_colors_text = self.ax.text(0.5, 1.05, f'Minimum Colors: {min_colors}', transform=self.ax.transAxes, ha='center', fontsize=12, color='black')
        
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

    def update_coloring(self, event):
        try:
            num_colors = int(self.input_box_n_coloring[0].text)  # Convertir el texto a número
            self.colors = self.get_optimal_n_coloring(num_colors)
            self.draw_graph()
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    
    GraphColoring()
