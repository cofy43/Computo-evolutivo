import math
import random
 
ALPHA = 0.85

def recocido_algoritmo(casos, capacidad, elementos, t_inicial=100, iteraciones=10):
    primer_solucion = solucion_inicial(elementos, capacidad)
    optimo_local, solucion = simulacion(primer_solucion, elementos, capacidad, t_inicial, iteraciones)
    combinacion = [0] * casos
    for idx in solucion:
        combinacion[idx] = 1
    return optimo_local, combinacion

def solucion_inicial(items, capacidad):
    """
    Tomamos de manera aleatoria elementos mientras no
    exedamos la capacidad maxima de la mochila
    """
    solucion = []
    total_items = len(items)
    indices = [x for x in range(total_items)]
    while capacidad > 0:
        indice = random.randint(0, len(indices) - 1)
        item_seleccionado = indices.pop(indice)
        if cost_peso_actual(solucion + [item_seleccionado], items)[0] <= capacidad:
            solucion.append(item_seleccionado)
            capacidad -= items[item_seleccionado][0]
        else:
            break
    return solucion

def cost_peso_actual(solucion, items):
    """
    calcula el tamaño y peso dada una combinacion
    de elementos para poder saber si se agregan o no
    mas elementos a la solucion local
    """
    costo, peso = 0, 0
    for item in solucion:
        peso += items[item][1]
        costo += items[item][0]
    return costo, peso

def genera_combinacion(solucion, items, capacidad):
    configuraciones = []
    for idx, _ in enumerate(items):
        if idx not in solucion:
            configuracion = solucion[:]
            configuracion.append(idx)
            if cost_peso_actual(configuracion, items)[1] <= capacidad:
                configuraciones.append(configuracion)
    for idx, _ in enumerate(solucion):
        configuracion = solucion[:]
        del configuracion[idx]
        if configuracion not in configuraciones:
            configuraciones.append(configuracion)
    return configuraciones

def simulacion(solucion, items, capacidad, t_inicial, iteraciones):
    """Ejecucion iterativa del algoritmo"""
    temperatura = t_inicial

    optimo_local = solucion
    costo_local = cost_peso_actual(solucion, items)[0]

    optimo_actual = solucion
    while True:
        costo_actual = cost_peso_actual(optimo_local, items)[0]
        for i in range(0, iteraciones):
            configuraciones = genera_combinacion(optimo_actual, items, capacidad)
            idx = random.randint(0, len(configuraciones) - 1)
            config_aleatoria = configuraciones[idx]
            delta = cost_peso_actual(config_aleatoria, items)[0] - costo_local
            if delta > 0:
                optimo_local = config_aleatoria
                costo_local = cost_peso_actual(optimo_local, items)[0]
                optimo_actual = config_aleatoria
            else:
                if math.exp(delta / float(temperatura)) > random.random():
                    optimo_actual = config_aleatoria

        temperatura *= ALPHA
        if costo_actual >= costo_local or temperatura <= 0:
            break
    return costo_local, optimo_local