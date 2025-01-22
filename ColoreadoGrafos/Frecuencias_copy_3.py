import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button, Slider, TextBox

class GraphColoring:
    def __init__(self):
        self.frecuencies_matrix = pd.read_csv('frecuencias.csv', header=None).values
        self.n = self.frecuencies_matrix.shape[0]
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.minimum_colors = 4
        self.colors = self.get_optimal_n_coloring(self.minimum_colors)
        self.color_map = ['green', 'blue', 'red', 'orange', 'purple', 'cyan', 'lime', 'magenta', 'yellow', 'pink']
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
        self.draw_graph()
        plt.show()

    def get_adjacency_matrix(self, matrix):
        num_filas, num_columnas = matrix.shape
        adjacency_matrix = np.zeros((num_filas, num_columnas))
        for i, frecuencies in enumerate(matrix):
            for j, frecuency in enumerate(frecuencies):
                if frecuency < 150 and frecuency != 0:
                    adjacency_matrix[i, j] = 1
        return adjacency_matrix

    def get_optimal_n_coloring(self, num_colors):
        colors = [-1] * self.n
        try:
            for node in range(self.n):
                forbidden_colors = {
                    colors[j] for j in range(self.n) if self.adjacency_matrix[node, j] == 1 and colors[j] != -1
                }
                color_usage = [colors.count(c) for c in range(num_colors)]
                available_colors = [
                    color for color in range(num_colors) if color not in forbidden_colors
                ]
                best_color = min(available_colors, key=lambda c: color_usage[c])
                colors[node] = best_color
        except ValueError:
            print("\n----- ¡ No se puede colorear el grafo con", num_colors, "colores. ! -----\n")
            exit()
        return colors
    def update_coloring(self, event):
        try:
            num_colors = int(self.input_box_n_coloring[0].text)  # Convertir el texto del cuadro a un número entero
            self.colors = self.get_optimal_n_coloring(num_colors)
            self.draw_graph()
        except ValueError:
            print("Please enter a valid number.")
    def get_maximum_matching(self):
        matched = [-1] * self.n
        matching_edges = []

        def bpm(u, seen):
            for v in range(self.n):
                if self.adjacency_matrix[u, v] == 1 and not seen[v]:
                    seen[v] = True
                    if matched[v] == -1 or bpm(matched[v], seen):
                        matched[v] = u
                        return True
            return False

        for i in range(self.n):
            seen = [False] * self.n
            bpm(i, seen)

        for v in range(self.n):
            if matched[v] != -1:
                matching_edges.append((matched[v], v))

        self.max_matching_edges = list(set(matching_edges))
        print("Maximum Matching Edges:", self.max_matching_edges)

    def add_node(self, event):
        self.n += 1
        self.node_labels.append(self.n)
        self.points = self.create_points()
        self.adjacency_matrix = np.pad(self.adjacency_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.colors.append(-1)
        self.frecuencies_matrix = np.pad(self.frecuencies_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.update_frequencies()
        self.create_sliders()
        self.draw_graph()

    def update_frequencies(self):
        for i in range(self.n-1):
            self.frecuencies_matrix[self.n-1, i] = self.sliders[i].val
            self.frecuencies_matrix[i, self.n-1] = self.sliders[i].val
        pd.DataFrame(self.frecuencies_matrix).to_csv('frecuencias.csv', header=False, index=False)
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.colors = self.get_optimal_n_coloring(int(self.input_box_n_coloring[0].text))

    def create_points(self):
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
        ax_input = plt.axes([0.291, 0.02, 0.05, 0.03])
        input_box = TextBox(ax_input, 'Number for optimal N-Coloring: ', initial='3')
        self.input_box_n_coloring.append(input_box)

    def create_button2(self):
        ax_button = plt.axes([0.38, 0.02, 0.2, 0.03])
        self.btn2 = Button(ax_button, 'Create N-Coloring')
        self.btn2.on_clicked(self.update_coloring)

    def create_button3(self):
        ax_button = plt.axes([0.6, 0.02, 0.2, 0.03])
        self.btn3 = Button(ax_button, 'Find Max Matching')
        self.btn3.on_clicked(self.find_max_matching)

    def find_max_matching(self, event):
        self.get_maximum_matching()
        self.draw_graph()

if __name__ == "__main__":
    GraphColoring()
