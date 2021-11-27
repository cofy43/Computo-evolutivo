import numpy as np
# -Generar (aleatoriamente) una poblacion 
#  inicial y evaluar
# -Hasta cumplir la condición de paro:
#   -Escalamiento
#   -Selección de padres (probabilísticamente)  
#    con base en su aptitud
#   -Aplicar operadores genéticos y evaluar
#    Seleccionar siguiente población

# Representación: Punto flotante Real
# Escalamiento: Escalamiento Sigma
# Selección de padres: Muestreo determinístico
# Cruza: Intermedia
# Mutación: De límite
# Selección: Más
# Elitismo: 

def inicializa(f, npop, nvar, lb, ub, nvars):
    # Generar población inicial
    genotipos = lb + (ub - lb) * np.random.uniform(low=0.0, high=1.0, size=[npop, nvars])
    # Fenotipos
    fenotipos = genotipos
    # Evaluar población
    aptitudes = f(fenotipos)
    return genotipos,fenotipos,aptitudes

def seleccion_padres(aptitudes):
    aptitud_total = np.sum(aptitudes)
    probabilidades = np.array([])
#    for fi in aptitudes:
#        probabilidades.

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
    genotipos, fenotipos, aptitudes = inicializa(f, npop, nvars)
    for i in range(ngen):
        # Escalamiento
        padres = seleccion_padres(aptitudes)
        # Seleccion de padres
        # Cruza
        # Mutacion
        # Mejor individuo
        # Seleccion de la siguiente generacion