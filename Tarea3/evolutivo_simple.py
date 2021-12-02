import numpy as np
from numpy.core.fromnumeric import argpartition
from problemas import *

"""
@author: Martin Felipe Espinal Cruces
Componentes del algoritmo evolutivo simple:
    Representación: Punto flotante Real
    Escalamiento: Escalamiento Sigma <- pendiente
    Selección de padres: Muestreo determinístico
    Cruza: Intermedia
    Mutación: uniforme
    Selección: Más
    Elitismo: 
"""
# -Generar (aleatoriamente) una poblacion 
#  inicial y evaluar
# -Hasta cumplir la condición de paro:
#   -Escalamiento: Singma
#   -Selección de padres (probabilísticamente)  
#    con base en su aptitud
#   -Aplicar operadores genéticos y evaluar
#    Seleccionar siguiente población

def inicializa(f, npop, nvar, lb, ub):
    # Generar población inicial
    genotipos = lb + (ub - lb) * np.random.uniform(low=0.0, high=1.0, size=[npop, nvar])
    # Fenotipos
    fenotipos = genotipos
    # Evaluar población
    aptitudes = []
    for fen in fenotipos:
        aptitudes.append(f(fen))
    aptitudes = np.array(aptitudes)
    return genotipos,fenotipos,aptitudes

#def escalamiento():
    

def seleccion_padres(aptitudes, npop):
    """
    aptitudes: listado con la evaluación de la función f
               a cada individuo generado
    npop: el número de 
    """
    aptitud_total = np.sum(aptitudes)
    esperanzas =[]
    # Diccionario auxiliar que nos permitira
    # saber cual individuo tiene tal esperaza
    # esto para poderlo indicar tras el
    # ordenamiento
    indices = {}
    i = 0
    for fi in aptitudes:
        # Probabilidad de la i-esima aptitud
        pi = fi/aptitud_total 
        # Esperanza de la i-esima aptitud
        efi = pi * npop 
        esperanzas.append(efi)
        indices[efi] = i
        i += 1
    esperanzas = np.array(esperanzas)
    esperanzas.sort()
    # indices de los padres seleccionados
    nuevos_padres = []
    for j in range(int(npop)):
        nuevos_padres.append(indices[esperanzas[j]])
    return nuevos_padres

def cruza(genotipos, punto_cruza, a, idx):
    """
    genotipos: poblacion actual
    punto_cruza: indice donde comenzara la cuza
    a: valor aleatorio entre [0, 1]
    ind: indices de los padres peviamente seleccionados
    """
    hijos_genotipo = np.zeros(np.shape(genotipos))
    k = 0
    for i, j in zip(idx[::2], idx[1::2]):
        if k >= punto_cruza:
            hijos_genotipo[k] = np.copy(genotipos[j]*a)
            hijos_genotipo[k+1] = np.copy(genotipos[i]*a)
        else:
            hijos_genotipo[k] = np.copy(genotipos[i])
            hijos_genotipo[k + 1] = np.copy(genotipos[j])
        k += 2
    return hijos_genotipo

def mutacion(genotipos, pm, lb, ub):
    """
    genotipos: padres previamente mutados
    pm: probabilidad de mutacion
    lb: limite inferior
    ub: limite superior
    """
    for i in range(len(genotipos)):
        for j in range(len(genotipos[i])):
            flip = np.random.uniform() <= pm
            if flip:
                genotipos[i, j] = np.random.uniform(lb[j], ub[j])
    return genotipos

def seleccion_mas(fenotipos, genotipos, aptitudes, hijos_genotipo, hijos_fenotipos, hijos_aptitudes, idx):
    nuevos_fenotiopos = []
    nuevos_genotipos = []
    nuevas_aptitudes = []
    # Primero agregamos a los padres seleccionados
    for i in idx:
        nuevos_fenotiopos.append(fenotipos[i])
        nuevos_genotipos.append(genotipos[i])
        nuevas_aptitudes.append(aptitudes[i])
    for i in range(len(hijos_genotipo)):
        nuevos_fenotiopos.append(hijos_fenotipos[i])
        nuevos_genotipos.append(hijos_genotipo[i])
        nuevas_aptitudes.append(hijos_aptitudes[i])
    nuevos_fenotiopos = np.array(nuevos_fenotiopos)
    nuevos_genotipos = np.array(nuevos_genotipos)
    nuevas_aptitudes = np.array(nuevas_aptitudes)
    return nuevos_fenotiopos, nuevos_genotipos, nuevas_aptitudes

def estadisticas(generacion, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes, padres):
    print('---------------------------------------------------------')
    print('Generación:', generacion)
    print('Población:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1,1), genotipos, fenotipos, aptitudes.reshape(-1, 1), aptitudes.reshape(-1, 1)/np.sum(aptitudes)), 1))
    print('Padres:', padres)
    print('frecuencia de padres:', np.bincount(padres))
    # print('Hijos:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1, 1), hijos_genotipo, hijos_fenotipo, hijos_aptitudes.reshape(-1, 1), hijos_aptitudes.reshape(-1, 1)/np.sum(hijos_aptitudes)), 1))
    print('Desempeño en línea para t=1: ', np.mean(aptitudes))
    print('Desempeño fuera de línea para t=1: ', np.max(aptitudes))
    print('Mejor individuo en la generación: ', np.argmax(aptitudes))

def algoritmo_evolutivo(f, lb, ub, pc, pm, nvars, npop, ngen):
    """
    f: Función de aptitud
    lb: Límite inferior
    up: Límite superior
    pc: Porcentaje de cruza
    pm: Prcentaje de mutación
    nvars: Número de variables
    npop: Número de población
    ngen: Número de generaciones
    """
    bg = np.zeros((ngen, nvars))
    bf = np.zeros((ngen, nvars))
    ba = np.zeros((ngen, 1))
    genotipos, fenotipos, aptitudes = inicializa(f, npop, nvars, lb, ub)
    for i in range(ngen):
        # Seleccion de padres
        indx = seleccion_padres(aptitudes, npop/2)
        # Cruza
        punto_cruza = np.random.uniform(low=0, high=nvars)
        a = np.random.uniform(low=0, high=1)
        hijos_genotipos = cruza(genotipos, punto_cruza, 1-a, indx)
        # Mutacion
        hijos_genotipos = mutacion(hijos_genotipos, pm, lb, ub)
        hijos_fenotipo = hijos_genotipos
        hijos_aptitudes = []
        for fen in hijos_fenotipo:
            hijos_aptitudes.append(f(fen))
        hijos_aptitudes = np.array(hijos_aptitudes)
        idx_best = np.argmax(aptitudes)
        # Estadisticas
        estadisticas(i, genotipos, fenotipos, aptitudes, hijos_genotipos, hijos_fenotipo, hijos_aptitudes, indx)
        b_gen = np.copy(genotipos[idx_best])
        b_fen = np.copy(fenotipos[idx_best])
        b_apt = np.copy(aptitudes[idx_best])
        ba[i] = np.copy(aptitudes[idx_best])
        genotipos, fenotipos, aptitudes = seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipos, hijos_fenotipo, hijos_aptitudes, indx)
        # Mejor individuo
        # Seleccion de la siguiente generacion
    print('Tabla de mejores:\n', ba)
    #Regresar mejor solución
    idx = np.argmax(aptitudes)
    return genotipos[idx], fenotipos[idx], aptitudes[idx]

nvars = 10
lb = 0*np.ones(nvars)
ub = 100*np.ones(nvars)
pc = 0.9
pm = 0.01
npop = 200
ngen = 100
print(algoritmo_evolutivo(rastrigin, lb, ub, pc, pm, nvars, npop, ngen))