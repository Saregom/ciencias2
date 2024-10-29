import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


"""
# Definimos la matriz de adyacencia (ejemplo)
n = 6
adjacency_matrix = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
])
"""
# Se crea la matriz inicial de frecuencias
matrizFrecuencias = np.array([[0,85,175,200,50,100], 
                              [85,0,125,175,100,160], 
                              [175,125,0,100,200,250], 
                              [200,175,100,0,210,220],
                              [50,100,200,210,0,100],
                              [100,160,250,220,100,0]])

# Se crea la matriz de adyacencia (de conexiones) a partir de la matriz de frecuencias
n = 6
adjacency_matrix = np.zeros((n,n))

for i, frecuencies in enumerate(matrizFrecuencias):
    for j, frecuency in enumerate(frecuencies):
        if frecuency < 150 and frecuency != 0:
             adjacency_matrix[i,j] = 1

# Crear puntos para graficar (distribuidos en un círculo para visualización)
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
radius = 10
points = np.vstack((radius * np.cos(theta), radius * np.sin(theta))).T


"""
Colores de los grafos
"""
neighbors = []

for k in range(n-1):
    # Obtener los índices donde hay conexiones (1s en la matriz de adyacencia)
    neighbor_indices = np.where(adjacency_matrix[k] == 1)[0]
    # Agregar los vecinos ordenados a la lista de neighbors
    neighbors.append(np.sort(neighbor_indices))

  
variables = [str(var) for var in range(n)]

domain = ['red', 'blue', 'green', 'orange', 'purple', 'pink']
#domain = ['red', 'blue', 'green']
domains = {}
for v in variables: 
    domains[v] = domain

# create binary constraints
constraints = {}
for i in range(len(neighbors)):
    for j in neighbors[i]:
        if(i<j): constraints[tuple([str(i), str(j)])] = True

constraints = constraints.keys()
csp = {'variables': variables, 'domains': domains, 'constraints': constraints, }


def complete(assignment, csp):
    return(all([v in assignment.keys() for v in csp['variables']])) 
def consistent(assignment, csp):
    for constr in csp['constraints']:
        if(constr[0] in assignment.keys() and constr[1] in assignment.keys()):
            if assignment[constr[0]] == assignment[constr[1]]: return(False)
        
    return(True)
def select_unassigned_var(assignment, csp):
    if(complete(assignment, csp)): return(None)
    
    return(csp['variables'][np.where([not v in assignment.keys() for v in csp['variables']])[0][0]])
    # I use a global variable to turn on verbose mode in the recursion
#VERBOSE = True
VERBOSE = False
COUNT = 0

# returns None for failure
def backtrack_search(csp):
    global COUNT
    COUNT = 0
    
    assignment = backtrack({}, csp)
    
    print(f"Checked nodes: {COUNT}")
    
    return assignment

def backtrack(assignment, csp):
    global VERBOSE, COUNT
    
    COUNT += 1
    
    if complete(assignment, csp): 
        return assignment
    
    var = select_unassigned_var(assignment, csp)
    
    # TODO: implement value ordering. Use the least-constraining-vaue heuristic. 
    # for val in order_domain(assignment, var, csp)
    for val in csp['domains'][var]:
        assignment[var] = val
        
        if VERBOSE: print(f"Checking: {assignment}")
        
        if consistent(assignment, csp):
            
            #TODO: add inference for early failing (forward checking, )
            # if inference_fails(assignment, csp): return(None)
            result = backtrack(assignment, csp)
            if not result is None:
                    return(result)
                
        del assignment[var]
        
    if VERBOSE: print(f"Backtracking")
    return(None) 
assignment = backtrack_search(csp)
# Dibujar conexiones según la matriz de adyacencia
for i in range(n):
    for j in range(i + 1, n):
        if adjacency_matrix[i, j] == 1:
            plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], color="gray")

# Dibujar puntos con los colores asignados
for i in range(len(points)):
    color = assignment[str(i)] if str(i) in assignment else "gray"
    plt.plot(points[i, 0], points[i, 1], 'o', color=color, markersize=20)
    plt.annotate(i, points[i, :], 
                 color='white', fontsize="large", weight='heavy',
                 horizontalalignment='center', verticalalignment='center')

plt.gca().set_aspect('equal', adjustable='box')
plt.show()