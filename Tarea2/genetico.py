import numpy as np

# Funcion intermedia para evaluar la apitud de cada fila
def evalua(f, genotipo):
    aptitud = []
    for individuo in genotipo:
        apt = f(individuo)
        print("apt", apt)
        aptitud.append(apt)
    return aptitud

def fa(indivuduo):
    x1, x2 = indivuduo[0], indivuduo[1]
    return 418.9829*2 - x1* np.sin(np.sqrt(abs(x1))) - x2* np.sin(np.sqrt(abs(x2)))

def inicializar(f, npop, nvars):
    # Generar población inicial
    print("lb")
    print(lb)
    print("ub")
    print(ub)
    genotipos = lb + (ub - lb) * np.random.uniform(low=0.0, high=1.0, size=[npop, nvars])
    print("genotipos")
    print(genotipos)
    print("-----------------------")
    # Fenotipos
    fenotipos = genotipos
    # Evaluar población
    aptitudes = evalua(f, fenotipos)
    print("aptitudes")
    print(aptitudes)
    print("-----------------------")
    return genotipos,fenotipos,aptitudes

def seleccion_ruleta(aptitudes, n):
    p = aptitudes/sum(aptitudes)
    cp = np.cumsum(p)
    parents = np.zeros(n)
    for i in range(n):
        X = np.random.uniform()
        parents[i] = np.argwhere(cp > X)[0]
    return parents.astype(int)


def EA(f, lb, ub, pc, pm, nvars, npop, ngen):
    genotipos, fenotipos, aptitudes = inicializar(f, npop, nvars)
    # Hasta condición de paro
    indx = seleccion_ruleta(aptitudes, npop)
    print("indices")
    print(indx)

nvars= 2
lb = -500*np.ones(nvars)
ub = 500*np.ones(nvars)
pc = 0.9    
pm = 0.01
npop = 10
ngen = 500

np.set_printoptions(formatter={'float': '{0: 0.3f}'.format})
print(EA(fa, lb, ub, pc, pm, nvars, npop, ngen))