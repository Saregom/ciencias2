import numpy as np
import pandas as pd

# Crear la matriz inicial de frecuencias
frecuencies_matrix = np.array([[0,85,175,200,50,100], 
                              [85,0,125,175,100,160], 
                              [175,125,0,100,200,250], 
                              [200,175,100,0,210,220],
                              [50,100,200,210,0,100],
                              [100,160,250,220,100,0]])

# Guardar la matriz en un archivo CSV
pd.DataFrame(frecuencies_matrix).to_csv('frecuencias.csv', header=False, index=False)
