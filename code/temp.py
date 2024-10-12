import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

def generar_red(n_paradas, n_rutas, max_conexiones):
    # Crear lista vacía para almacenar paradas y rutas
    paradas = list(range(n_paradas))
    rutas = []

    # Crear grafo auxiliar para verificar conectividad
    grafo_aux = nx.Graph()

    # Agregar paradas al grafo auxiliar
    for parada in paradas:
        grafo_aux.add_node(parada)

    # Iterar para crear cada ruta
    for i in range(n_rutas):
        # Seleccionar aleatoriamente dos paradas que no estén conectadas
        parada1 = random.choice(paradas)
        parada2 = random.choice(paradas)
        while parada1 == parada2 or grafo_aux.has_edge(parada1, parada2):
            parada2 = random.choice(paradas)

        # Agregar conexión entre paradas
        rutas.append((parada1, parada2))

        # Agregar arista al grafo auxiliar
        grafo_aux.add_edge(parada1, parada2)

    
    # Verificar conectividad del grafo
    if not nx.is_connected(grafo_aux):
        # Si el grafo no es conexo, agregar aristas adicionales para conectar los componentes
        componentes = list(nx.connected_components(grafo_aux))
        for i in range(len(componentes) - 1):
            parada1 = random.choice(list(componentes[i]))
            parada2 = random.choice(list(componentes[i + 1]))
            rutas.append((parada1, parada2))
            grafo_aux.add_edge(parada1, parada2)

    # Crear grafo con NetworkX
    G = nx.Graph()
    G.add_nodes_from(paradas)
    for ruta in rutas:
        G.add_edge(*ruta)

    # Dibujar grafo con NetworkX
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500)
    for ruta in rutas:
        nx.draw_networkx_edges(G, pos, edgelist=[ruta])
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.show()

    # Crear matriz de adyacencia con NumPy
    matriz_adyacencia = np.zeros((n_paradas, n_paradas), dtype= int)
    for ruta in rutas:
        matriz_adyacencia[ruta[0], ruta[1]] = 1
        matriz_adyacencia[ruta[1], ruta[0]] = 1

    return G, matriz_adyacencia

def componentesconexas(inicio, matriz, t_cuadrado, comp_temp):
    result = []
    for i_f in range(inicio, inicio+t_cuadrado):
        for i_c in range(inicio, inicio+t_cuadrado):
            result.append(matriz[i_f][i_c])
    if((0 in result) == False):
        if(inicio +t_cuadrado == len(matriz)):
            lista_c = []
            for num in range(inicio, inicio + t_cuadrado):
                 lista_c.append(num)
            comp_temp.append(lista_c)
            return comp_temp
        else:
            componentesconexas(inicio, matriz, t_cuadrado+1, comp_temp)
    elif t_cuadrado != 1:
            lista_c = []
            for num in range(inicio, inicio + t_cuadrado - 1):
                 lista_c.append(num)
            comp_temp.append(lista_c)
            componentesconexas(inicio + t_cuadrado - 1, matriz, 1, comp_temp)
    elif inicio +t_cuadrado == len(matriz):
         return comp_temp
    else:
        componentesconexas(inicio+1, matriz, 1, comp_temp)

def normalize(M):
    for i in range(len(M)):
        M[i,i] = 1
    return M

# Ejemplo de uso
n_paradas = 8
n_rutas = 8
max_conexiones = 2

G, matriz_adyacencia = generar_red(n_paradas, n_rutas, max_conexiones)
print(matriz_adyacencia)

print("Componentes Conexas:")
comp_temp = []
componentesconexas(0, normalize(matriz_adyacencia),1,comp_temp)
print(comp_temp) 