from typing import cast
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

def float_bin(number):
    whole, dec = str(number).split(".")
    # esto es por los numeros que incluyen
    # notacion cientifica, en cuyo caso sucede
    # una excepcion si se intenta convertir la parte
    # decimal a binario 
    try:
        notacion_cientifica = str(dec).index("e")
        if notacion_cientifica > 0:
            dec = str(dec)[0:str(dec).index("e")]
    except ValueError:
        dec = dec
    whole = int(whole)
    dec = int (dec)

  
    res = str(bin(whole)) + "." + str(bin(dec))
  
    return res

def mutacion(genotipo, indx, pm):
    hijos = []
    #Seleccionamos los mejores individuos
    for i in indx:
        individuo = genotipo[i]
        binario = [float_bin(individuo[0])]
        binario.append(float_bin(individuo[1]))
        mutado = inversion_de_un_bit(binario, pm)
        hijos.append(mutado)
    return np.array(hijos)

def inversion_de_un_bit(individuo_binario, pm):
    primera_parte = list(individuo_binario[0])
    segunda_parte = list(individuo_binario[1])
    for i in range(len(primera_parte)):
        flip = np.random.uniform() <= pm
        digit = primera_parte[i]
        if flip and digit.isdigit():
            res = (int(digit) + 1) % 2
            primera_parte[i] = str(res)

    for i in range(len(segunda_parte)):
        flip = np.random.uniform() <= pm
        digit = segunda_parte[i]
        if flip and digit.isdigit():
            res = (int(digit) + 1) % 2
            segunda_parte[i] = str(res)

    nuevo_binario_1 = ''.join([str(elem) for elem in primera_parte])
    nuevo_binario_2 = ''.join([str(elem) for elem in segunda_parte])
    mutado = [nuevo_binario_1 , nuevo_binario_2]
    mutado = [binaryToFloat(nuevo_binario_1) , binaryToFloat(nuevo_binario_2)]
    #Regresamos a su representacion real
    return mutado

def binaryToFloat(binary):
    whole, dec = str(binary).replace("b", "").split(".")
    whole = int(whole, 2)
    dec = int(dec, 2)
    return float(str(whole) + "." + str(dec))

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

def cruza_un_punto(genotipo, idx, pc):
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
    # return hijos_genotipo, hijos_fenotipo, hijos_aptitudes

def EA(f, lb, ub, pc, pm, nvars, npop, ngen):
    genotipos, fenotipos, aptitudes = inicializar(f, npop, nvars) #completa
    ba = np.zeros((ngen, 1)) 
    # Hasta condición de paro
    for i in range(ngen):
        # Selección de padres
        indx = seleccion_ruleta(aptitudes, npop) #completo
        # Escalaiento
        # Cruza
        hijos_genotipo = cruza_un_punto(genotipos, indx, pc) #completo
        # Mutacion
        hijos_genotipo = mutacion(genotipos, indx, pm) #completo
        hijos_fenotipo = hijos_genotipo
        hijos_aptitudes= evalua(f, hijos_fenotipo) #completo

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
    print('Tabla de mejores:\n', ba)
    idx = np.argmax(aptitudes)
    return genotipos[idx], fenotipos[idx], aptitudes[idx]

nvars= 2
lb = -500*np.ones(nvars)
ub = 500*np.ones(nvars)
pc = 0.9    
pm = 0.5
npop = 10
ngen = 100

np.set_printoptions(formatter={'float': '{0: 0.6f}'.format})
print(EA(fa, lb, ub, pc, pm, nvars, npop, ngen))