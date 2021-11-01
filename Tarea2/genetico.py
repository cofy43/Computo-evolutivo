import numpy as np

# Funcion intermedia para evaluar la apitud de cada fila
def evalua(f, genotipo):
    aptitud = []
    for individuo in genotipo:
        aptitud.append(f(individuo))
    return aptitud

def fa(indivuduo):
    x1, x2 = indivuduo[0], indivuduo[1]
    return 418.9829*2 - x1* np.sin(np.sqrt(abs(x1))) - x2* np.sin(np.sqrt(abs(x2)))

def inicializar(f, npop, nvars):
    # Generar población inicial
    # La razon por la que npop se multiplica por dos es que al ser f una funcion de
    # aptitud de dos variables entonces necesitamos que cada individuo este conformado
    # por dos variables y por tanto necesitamos un arreglo de dos veces el tamaño de la
    # poblacion
    genotipos = lb + (ub - lb) * np.random.uniform(low=-500, high=500, size=[npop*2, nvars])
    #print(genotipos)
    # Fenotipos
    fenotipos = genotipos
    # Evaluar población
    aptitudes = evalua(f, fenotipos)
    print(aptitudes)
    return genotipos,fenotipos,aptitudes

#def ruleta()

def EA(f, lb, ub, pc, pm, nvars, npop, ngen):
    genotipos, fenotipos, aptitudes = inicializar(f, npop, nvars)

nvars= 2
lb = 0*np.ones(nvars)
ub = 100*np.ones(nvars)
pc = 0.9    
pm = 0.01
npop = 200
ngen = 500

np.set_printoptions(formatter={'float': '{0: 0.3f}'.format})
print(EA(fa, lb, ub, pc, pm, nvars, npop, ngen))