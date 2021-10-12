import sys
from functools import partial
from tabulate import tabulate
from recocido_simulado import recocido_algoritmo

# Datos obtenidos del archivo leido
elementos = []
# Variables para el algoritmo
t_inicial = 100 
iteraciones = 5

def read_bin_file(fileName):
    try:
        file = open(fileName, "r")
    except OSError:
        print("No se pudo leer el archivo: " + fileName)
        print("Verifica que el nombre del archivo es correcto, existe")
        print("o se encuentra en la carpeta bin/ e intentalo nuevamente")
        sys.exit()
    with file:
        lines = file.readlines()
        parametros = lines.pop(0).replace("\n", "").split(" ")
        casos = int(parametros[0])
        capacidad = int(parametros[1])
        for line in lines:
            line = line.replace("\n", "").split(" ")
            elementos.append([int(line[0]), int(line[1])])
        file.close()
        #return primer_solucion(casos, capacidad), casos, capacidad
        return casos, capacidad

def imprime_elementos(casos, indices, items):
    val_total = 0
    pes_total = 0
    elementos = []
    for i in range(casos):
        if int(indices[i]) == 1:
            temp = items[i]
            #cadena += "|" + str(temp[0]) + "\t| " + str(temp[1]) + "   \t|\n"
            elementos.append(temp)
            val_total += temp[0]
            pes_total += temp[1]
    print(tabulate(elementos, headers=['Valor', 'Peso'], tablefmt='orgtbl'))
    print(f"\nValor total: {val_total}\t Peso total: {pes_total}\n")

def solver(method, casos, capacidad):
    mochila, combinacion = method(casos, capacidad, elementos)
    return mochila, combinacion

if __name__ == "__main__":

    casos, capacidad = read_bin_file("../bin/ks_10000_0")

    method = partial(recocido_algoritmo, t_inicial=t_inicial, iteraciones=iteraciones)
    solving_time = 0
    optimo_local, indices = [], []

    print(f"Casos: {casos}\t Capacidad: {capacidad}\t Iteraciones: {iteraciones}")

    for i in range(iteraciones):
        optimo_local, indices = solver(method, casos, capacidad)
        # Descomenta estas lineas para las soluciones a cada iteracion
        #print(f"\niteracion {i+1}")
        #imprime_elementos(casos, indices, elementos)
    
    imprime_elementos(casos, indices, elementos)