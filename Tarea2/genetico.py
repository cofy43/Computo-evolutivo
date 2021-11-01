import numpy as np

# Funcion intermedia para evaluar la apitud de cada fila
def evalua(f, genotipo):
    aptitud = []
    for individuo in genotipo:
        apt = f(individuo)
        aptitud.append(apt)
    return aptitud

def fa(indivuduo):
    x1, x2 = indivuduo[0], indivuduo[1]
    return 418.9829*2 - x1* np.sin(np.sqrt(abs(x1))) - x2* np.sin(np.sqrt(abs(x2)))

def inicializar(f, npop, nvars):
    # Generar población inicial
    genotipos = lb + (ub - lb) * np.random.uniform(low=0.0, high=1.0, size=[npop, nvars])
    # Fenotipos
    fenotipos = genotipos
    # Evaluar población
    aptitudes = evalua(f, fenotipos)
    return genotipos,fenotipos,aptitudes

def seleccion_ruleta(aptitudes, n):
    p = aptitudes/sum(aptitudes)
    cp = np.cumsum(p)
    parents = np.zeros(n)
    for i in range(n):
        X = np.random.uniform()
        parents[i] = np.argwhere(cp > X)[0]
    return parents.astype(int)

def inversion_de_un_bit(genotipo, indx):
    hijos = []
    for i in indx:
        hijos.append(genotipo[i])
        # Falta implementar inversion de un bit
    return np.array(hijos)

def estadisticas(generacion, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes, padres):
    print('---------------------------------------------------------')
    print('Generación:', generacion)
    print('Población:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1,1), genotipos, fenotipos, aptitudes.reshape(-1, 1), aptitudes.reshape(-1, 1)/np.sum(aptitudes)), 1))
    print('Padres:', padres)
    print('frecuencia de padres:', np.bincount(padres))
    print('Hijos:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1, 1), hijos_genotipo, hijos_fenotipo, hijos_aptitudes.reshape(-1, 1), hijos_aptitudes.reshape(-1, 1)/np.sum(hijos_aptitudes)), 1))
    print('Desempeño en línea para t=1: ', np.mean(aptitudes))
    print('Desempeño fuera de línea para t=1: ', np.max(aptitudes))
    print('Mejor individuo en la generación: ', np.argmax(aptitudes))

def mutacion_un_punto(genotipo, idx, pc):
    hijos_genotipo = np.zeros(np.shape(genotipo))
    k = 0
    for i, j in zip(idx[::2], idx[1::2]):
        flip = np.random.uniform()<=pc
        if flip:
            punto_cruza = np.random.randint(0, len(genotipo[0]))
            hijos_genotipo[k] = np.concatenate((genotipo[i,0:punto_cruza], genotipo[j,punto_cruza:]))
            hijos_genotipo[k+1] = np.concatenate((genotipo[j, 0:punto_cruza], genotipo[i, punto_cruza:]))
        else:
            hijos_genotipo[k] = np.copy(genotipo[i])
            hijos_genotipo[k + 1] = np.copy(genotipo[j])
        k += 2
    return hijos_genotipo

def seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes):
    """
    mitad = int(len(fenotipos)/2)
    indices_mejores_padres = np.argpartition(aptitudes, -mitad)[-mitad:]
    indices_mejores_hijos = np.argpartition(hijos_aptitudes, -mitad)[-mitad:]
    print("fenotipos[indices_mejores_padres]", fenotipos[indices_mejores_padres])
    print("hijos_fenotipo[0][indices_mejores_hijos]", hijos_fenotipo[indices_mejores_hijos])
    nuevo_fenotipo = fenotipos[indices_mejores_padres] + hijos_fenotipo[indices_mejores_hijos]
    nuevo_genotipo = nuevo_fenotipo
    nuevo_aptitudes = aptitudes[indices_mejores_padres] + hijos_aptitudes[indices_mejores_hijos]
    return nuevo_fenotipo, nuevo_genotipo, nuevo_aptitudes
    """
    return hijos_genotipo, hijos_fenotipo, hijos_aptitudes

def EA(f, lb, ub, pc, pm, nvars, npop, ngen):
    genotipos, fenotipos, aptitudes = inicializar(f, npop, nvars) #completa
    ba = np.zeros((ngen, 1)) 
    # Hasta condición de paro
    for i in range(ngen):
        # Selección de padres
        indx = seleccion_ruleta(aptitudes, npop) #completo
        # Cruza
        hijos_genotipo = inversion_de_un_bit(genotipos, indx)
        # Mutacion
        #hijos_genotipo = mutacion_un_punto(genotipos, indx, pc) #completo
        hijos_fenotipo = hijos_genotipo
        hijos_aptitudes= evalua(f, hijos_fenotipo)

        # Estadisticas
        #estadisticas(i, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes, indx)

        #Mejor individuo
        idx_best = np.argmax(aptitudes)
        b_gen = np.copy(genotipos[idx_best])
        b_fen = np.copy(fenotipos[idx_best])
        b_apt = np.copy(aptitudes[idx_best])
        ba[i] = np.copy(aptitudes[idx_best])

        #Selección de siguiente generación
        genotipos, fenotipos, aptitudes = seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes)
        print("nuevos")
        print(genotipos, fenotipos, aptitudes)
    print('Tabla de mejores:\n', ba)
    idx = np.argmax(aptitudes)
    return genotipos[idx], fenotipos[idx], aptitudes[idx]

nvars= 2
lb = -500*np.ones(nvars)
ub = 500*np.ones(nvars)
pc = 0.9    
pm = 0.01
npop = 10
ngen = 500

np.set_printoptions(formatter={'float': '{0: 0.6f}'.format})
print(EA(fa, lb, ub, pc, pm, nvars, npop, ngen))