import numpy as np
from joblib import Parallel, delayed

# Para definir la paralelización:

# Número de dimensiones
d = 10
pi = np.pi

def rastrigin(x):
    """
    Problema Rastrigin
    Función definida para d dimensiones en donde 
    los mínimos locales se encuentran distribuidos
    uniformemente y el objetivo de esta función es
    encontrar un mínimo obtimo
    """
    return 10*d + np.sum(x**2 - 10*np.cos(2*pi*x))

def parallelRastrigin(pob):
    results = Parallel(n_jobs=-1, verbose=10, backend="threading")(
             map(delayed(rastrigin), pob))
    return results

def ackley(x):
    """
    Problema ACKLEY
    Función que se caracteriza por tener una región
    plana y un gran agujero en el centro donde se
    encuentra el mínimo global.
    Valores utilizados: a = 20, b = 0.2, c = 2 * pi
    """
    sumando1 = -20 * np.exp(-0.2 * np.sqrt(0.5 * np.sum(x**2)))
    sumando2 = np.exp(0.5*np.sum(np.cos(2*pi*x)))
    return  sumando1 - sumando2 + 20 + np.exp(1)

def parallelAckley(pob):
    results = Parallel(n_jobs=-1, verbose=10, backend="threading")(
             map(delayed(ackley), pob))
    return results

def rosenbrock(x):
    """
    Problema ROSENBROCK
    Función con aspecto similar al de una banana
    con la característica de ser unimodal donde
    el mínimo global se encuentra en un valle
    parabólico
    """
    suma = 0
    for i in range(len(x)-1):
        xi = x.item(i)
        xi1 = x.item(i+1)
        suma += 100*((xi1 - (xi**2))**2) + (xi-1)**2
    return suma

def parallelRosenbrock(pob):
    results = Parallel(n_jobs=-1, verbose=10, backend="threading")(
             map(delayed(rosenbrock), pob))
    return results

def eggholder(x):
    """
    Problema EGGHOLDER
    Función con un gran número de mínimos locales 
    """
    x1 = x[0]
    x2 = x[1]
    sumando1 = (x2 + 47)*np.sin(np.sqrt(np.absolute(x2 + (x1/2) + 47)))
    sumando2 = x1*np.sin(np.sqrt(np.absolute(x1-(x2+47))))
    return - sumando1 - sumando2

def parallelEggholder(pob):
    results = Parallel(n_jobs=-1, verbose=10, backend="threading")(
             map(delayed(eggholder), pob))
    return results

def easom(x):
    """
    Problema EASOM
    """
    x1 = x[0]
    x2 = x[0]
    return - np.cos(x1)*np.cos(x2)*np.exp(-(x1 - np.pi)**2 - (x2 - np.pi)**2)

def parallelEasom(pob):
    results = Parallel(n_jobs=-1, verbose=10, backend="threading")(
             map(delayed(easom), pob))
    return results

"""
x = np.array([1,2,3,4,5,6,7,8,9,0])
print("rastrigin")
print(parallelRastrigin(x))
print("ackley")
print(ackley(x))
print("rosenbrock")
print(rosenbrock(x))
print("eggholder")
print(eggholder(x))
print("easom")
print(easom(x))
"""