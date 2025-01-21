import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button, Slider



class GraphColoring:
    def __init__(self):
        self.frecuencies_matrix = pd.read_csv('frecuencias.csv', header=None).values
        self.n = self.frecuencies_matrix.shape[0]
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.colors = self.get_coloracion(self.adjacency_matrix)
        self.color_map = ['green', 'blue', 'red', 'pink', 'orange', 'purple']
        self.radius = 10
        self.points = self.create_points()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.3)
        self.sliders = []
        self.create_sliders()
        self.create_button()
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
        return colors

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
                    self.ax.plot([self.points[i, 0], self.points[j, 0]], [self.points[i, 1], self.points[j, 1]], color="gray")
        for i in range(len(self.points)):
            self.ax.annotate(
                i+1, self.points[i, :],
                color='white', fontsize="large", weight='heavy',
                horizontalalignment='center', verticalalignment='center'
            )
        self.ax.axis('off')
        self.ax.set_aspect('equal', adjustable='box')
        plt.draw()

    def add_node(self, event):
        print("Button pressed!") 
        self.update_frequencies()
        self.n += 1
        self.points = self.create_points()
        self.adjacency_matrix = np.pad(self.adjacency_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.colors.append(-1)
        self.frecuencies_matrix = np.pad(self.frecuencies_matrix, ((0, 1), (0, 1)), mode='constant', constant_values=0)
        self.create_sliders()  # Recreate sliders
        self.draw_graph()

    def update_frequencies(self):
        for i in range(self.n-1):
            self.frecuencies_matrix[self.n-1, i] = self.sliders[i].val
            self.frecuencies_matrix[i, self.n-1] = self.sliders[i].val
        pd.DataFrame(self.frecuencies_matrix).to_csv('frecuencias.csv', header=False, index=False)
        self.adjacency_matrix = self.get_adjacency_matrix(self.frecuencies_matrix)
        self.colors = self.get_coloracion(self.adjacency_matrix)

    def create_button(self):
        print("Button creado!") 
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
        self.btn = Button(ax_button, 'Add Node')
        self.btn.on_clicked(self.add_node)

    def create_sliders(self):
        for slider in self.sliders:
            slider.ax.remove()
        self.sliders = []
        for i in range(self.n):
            ax_slider = plt.axes([0.1, 0.05 + i * 0.03, 0.65, 0.02], facecolor='lightgoldenrodyellow')
            slider = Slider(ax_slider, f'Dist to Node {i+1}', 0, 300, valinit=0)
            self.sliders.append(slider)

if __name__ == "__main__":
    
    GraphColoring()
  