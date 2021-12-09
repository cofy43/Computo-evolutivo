import numpy as np
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
Componentes avanzados:
    Paralelizmo en las funciones de aptitud
    Técnica de diversidad: Comparación de aptitud
"""
nombre_generico = "Resultados/{name}/Resultados_problema_{name}_ejecución_{indice}.txt"
nombre_generico_total = "Resultados/{name}/Resultados_problema_{name}_total.txt"
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
    aptitudes = f(fenotipos)
    #for fen in fenotipos:
    #    aptitudes.append(f(fen))
    aptitudes = np.array(aptitudes)
    return genotipos,fenotipos,aptitudes

def diversidad(aptitudes):
    nuevas_apt = []
    suma_sh = 0
    radio_nicho = 0.5
    print(aptitudes)
    # Subdividimos la población con base en la
    # similitud entre los individuos
    for i, j in zip(aptitudes[::2], aptitudes[1::2]):
        d_i_j = i - j
        if d_i_j < radio_nicho:
            suma_sh += 1 - (d_i_j/radio_nicho)
    # Calculamos las nuevas aptitudes 
    for aptitud in aptitudes:
        nuevas_apt.append(aptitud/suma_sh)
    return nuevas_apt
    

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

def seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes):
    mitad = int(len(fenotipos)/2)
    indices_mejores_padres = np.argpartition(aptitudes, -mitad)[-mitad:]
    indices_mejores_hijos = np.argpartition(hijos_aptitudes, -mitad)[-mitad:]
    # nuevo_fenotipo = fenotipos[indices_mejores_padres] + hijos_fenotipo[indices_mejores_hijos]
    nuevo_fenotipo = []
    nuevo_aptitudes = []
    for i in indices_mejores_padres:
        nuevo_aptitudes.append(aptitudes[i])
        nuevo_fenotipo.append(fenotipos[i])

    for i in indices_mejores_hijos:
        nuevo_aptitudes.append(hijos_aptitudes[i])
        nuevo_fenotipo.append(hijos_fenotipo[i])
    nuevo_genotipo = nuevo_fenotipo
    return np.array(nuevo_fenotipo), np.array(nuevo_genotipo), np.array(nuevo_aptitudes)

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
    nombre_archivo_t = nombre_generico_total.format(name="Easom")
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
        hijos_aptitudes = f(hijos_fenotipo)
        # Manteniendo la diversidad
        hijos_aptitudes = diversidad(hijos_aptitudes)
        hijos_aptitudes = np.array(hijos_aptitudes)
        
        idx_best = np.argmax(aptitudes)
        # Estadisticas
        estadisticas(i, genotipos, fenotipos, aptitudes, hijos_genotipos, hijos_fenotipo, hijos_aptitudes, indx)
        b_gen = np.copy(genotipos[idx_best])
        b_fen = np.copy(fenotipos[idx_best])
        b_apt = np.copy(aptitudes[idx_best])
        ba[i] = np.copy(aptitudes[idx_best])
        # Seleccion de la siguiente generacion
        genotipos, fenotipos, aptitudes = seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipos, hijos_fenotipo, hijos_aptitudes)
        # Mejor individuo
        """
        nombre_archivo = nombre_generico.format(name="Easom" ,indice=i+1)
        minma = aptitudes[np.argmin(aptitudes)]
        maximo = aptitudes[idx_best]
        media = np.median(aptitudes)
        desviacion = np.std(aptitudes)
        file = open(nombre_archivo, 'a')
        file.write("Minima={min}\n".format(min=minma))
        file.write("Media={med}\n".format(med=media))
        file.write("Maxima={max}\n".format(max=maximo))
        file.write("Desviación Estandar={de}\n".format(de=desviacion))
        file.close()
        file = open(nombre_archivo_t, 'a')
        file.write("----------------------------------")
        file.write("Ejecucion={indx}\n".format(indx=i))
        file.write("Minima={min}\n".format(min=minma))
        file.write("Media={med}\n".format(med=media))
        file.write("Maxima={max}\n".format(max=maximo))
        file.write("Desviación Estandar={de}\n".format(de=desviacion))
        file.write("----------------------------------")
        file.close()
        """
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
ngen = 20
# rastrigin
#print(algoritmo_evolutivo(parallelRastrigin, lb, ub, pc, pm, nvars, npop, ngen))
# ackley
#print(algoritmo_evolutivo(parallelAckley, lb, ub, pc, pm, nvars, npop, ngen))
# rosenbrock
#print(algoritmo_evolutivo(parallelRosenbrock, lb, ub, pc, pm, nvars, npop, ngen))
# eggholder
#print(algoritmo_evolutivo(parallelEggholder, lb, ub, pc, pm, nvars, npop, ngen))
# easom
#print(algoritmo_evolutivo(parallelEasom, lb, ub, pc, pm, nvars, npop, ngen))