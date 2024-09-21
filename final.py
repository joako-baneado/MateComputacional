import numpy as np
from collections import deque
import graphviz as gv

def showGraph(G):
    n = len(G)
    dot = gv.Digraph("g")
    for i in range(n):
        dot.node(str(i))
    for i in range (n):
        for j in range(n):
            if(G[i,j] == 1):
                dot.edge(str(i),str(j))
    return dot

#CREAR MATRIZ RANDOM CON M UNOS
def randomMatrix(n,m):
    G=np.zeros((n*n),dtype= int)
    G[:m] = 1
    np.random.shuffle(G)
    G = G.reshape(n,n)
    return G

#PONEMOS UNOS EN LA DIAGONAL
def normalize(M):
    for i in range(len(M)):
        M[i,i] = 1

#MODIFICAMOS M A LA MATRIZ DE CAMINOS
def matrix_caminos(M):
    size = len(M)
    for i in range(size):
        for j in range(size):
            if M[i,j] == 1 and i!=j:
                for k in range(size):
                    if M[j,k] == 1:
                        M[i,k] = 1

#REORDENAMOS M DE MAYOR A MENOR CON BUBBLESORT
def reordenar(M):
    size = len(M)
    orden = np.zeros((size,2))
    for i in range(size):
        orden[i,0] = i
        orden[i,1] = np.sum(M[i,:])
    for i in range(size):
        # Últimos elementos ya están en su lugar
        for j in range(0, size-i-1):
            # Intercambiar si el elemento es mayor que el siguiente
            if orden[j,1] < orden[(j+1),1]:                
                temp = np.copy(orden[j, :])  
                orden[j,:] = orden[(j+1),:]
                orden[(j+1),:] = temp
    print("orden de la nueva matriz:")
    print (orden)
    L = np.copy(M)
    for i in range(size):
        num = int(orden[i,0])
        if num != i:
            L[i,:] = M[num,:]
    print("orden aplicado en las filas")
    print(L)
    M = np.transpose(L)
    L = np.copy(M)       
    for i in range(size):
        num = int(orden[i,0])
        if num != i:
            L[i,:] = M[num,:]
    print("orden aplicado en las filas")
    M = np.transpose(L)
    print(M)
    return M

def f_recursiva(inicio, matriz, t_cuadrado, comp_temp):
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
            f_recursiva(inicio, matriz, t_cuadrado+1, comp_temp)
    elif t_cuadrado != 1:
            lista_c = []
            for num in range(inicio, inicio + t_cuadrado - 1):
                 lista_c.append(num)
            comp_temp.append(lista_c)
            f_recursiva(inicio + t_cuadrado - 1, matriz, 1, comp_temp)
    elif inicio +t_cuadrado == len(matriz):
         return comp_temp
    else:
        f_recursiva(inicio+1, matriz, 1, comp_temp)

def componentes(M):
    L = np.copy(M)
    n = len(M)
    max=0
    comprobacion= np.where(M==0)
    if len(comprobacion[0]) == 0:
        return M
    for i in range(n):
        if i == n-1: return L
        if max==0:
            for j in range(n-i):
                if M[i,j+i] == 0 or M[i+j,i] == 0:
                    max=j
                    break            
        L[i,max+i:], L[max+i:,i] = 0 , 0
        if max>=1: max = max-1
    
    for i in range(n):
        L[i,i] = 1

    return L


def ingresar_grafo():
    grafo = {}
    num_nodos = Ingresar_n_entre8y16()
    while 1:
        num_aristas = int(input("Ingrese el número de aristas: \n"))
        if num_aristas>=1 and num_aristas<=num_nodos*num_nodos:
            break    
        else: print("Ingrese un valor correcto.")
    
    #num_aristas = int(input("Ingresa el número de aristas: "))
    
    nodos = []
    
    # Ingresar nodos
    for i in range(num_nodos):
        nodo = input(f"Ingrese el nombre del nodo {i+1}: ")
        if nodo not in grafo:
            grafo[nodo] = []
        nodos.append(nodo)

    # Ingresar aristas
    for i in range(num_aristas):
        while (1):
            nodo1 = input(f"Ingrese el nodo de origen de la arista {i+1}: ")
            nodo2 = input(f"Ingrese el nodo de destino de la arista {i+1}: ")
            
            # Asegurarse de que ambos nodos existan en el grafo
            if nodo1 in grafo and nodo2 in grafo:
                grafo[nodo1].append(nodo2)
                grafo[nodo2].append(nodo1)  # Si el grafo es no dirigido
                break
            else:
                print("Uno o ambos nodos no existen en el grafo. Inténtalo de nuevo.")

    return grafo, nodos

def convertir_a_matriz_adyacencia(grafo, nodos):
    num_nodos = len(nodos)
    matriz = np.zeros((num_nodos*num_nodos),dtype= int)
    matriz = matriz.reshape(num_nodos,num_nodos)
    # Crear un índice para cada nodo
    indices = {nodo: idx for idx, nodo in enumerate(nodos)}
    # Llenar la matriz de adyacencia
    for nodo in grafo:
        for vecino in grafo[nodo]:
            i = indices[nodo]
            j = indices[vecino]
            matriz[i,j] = 1  # Hay una arista entre nodo y vecino
    
    return matriz

def Ingresar_n_entre8y16():
    while 1:
        n = int(input("Ingrese el número de nodos: (de 8 a 16) \n"))
        if n>=8 and n<=16:
            break    
        else: print("Ingrese un valor correcto.")
    return n

def crear_matriz_aleatoria():
    M = []
    n = Ingresar_n_entre8y16()
    M = randomMatrix(n,n*2)
    return M  

def ingreso_grafo_manual():
    grafo, nodos = ingresar_grafo()
    return convertir_a_matriz_adyacencia(grafo, nodos) 

def main():   
    print("Ingrese opción: ")
    while 1:
        print("1: Generar Matriz aleatoria \n2: Ingresar datos de una Matriz")
        n = input()
        n = int(n)
        if n==1 or n ==2:
            break    
    if n==1:
        M = crear_matriz_aleatoria()
    elif n==2:
        M = ingreso_grafo_manual()
    
    print("matriz de adyaciencia generada:")
    print(M)

    print("Ponemos unos en la diagonal:")
    normalize(M)
    print(M)

    matrix_caminos(M)
    print("MATRIZ DE CAMINOS:")
    print(M)
    M = reordenar(M)
    print("REORDEN FINAL:")
    print(M)
    print("Componentes Conexas:")
    comp_temp = []
    f_recursiva(0,M,1,comp_temp)
    L = componentes(M)
    print(L)
    showGraph(L).view()
    print(comp_temp) 



if __name__ == "__main__":
    main()