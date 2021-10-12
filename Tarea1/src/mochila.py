import sys
from functools import partial
from time import time
from recocido_simulado import recocido_algoritmo

# Datos obtenidos del archivo leido
elementos = []
# Variables para el algoritmo
t_inicial = 100 
iteraciones = 100

def read_bin_file(fileName):
    try:
        file = open(fileName, "r")
    except OSError:
        print("No se pudo leer el archivo: " + fileName)
        print("Verifica que el nombre del archivo es correcto o existe")
        print("e intentalo nuevamente")
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
    cadena = "Valor:    Peso:   \n"
    cadena += "------------------\n"
    for i in range(casos):
        if int(indices[i]) == 1:
            temp = items[i]
            cadena += "|" + str(temp[0]) + "    |    " + str(temp[1]) + "|\n"
            val_total += temp[0]
            pes_total += temp[1]
    cadena += "------------------\n"
    cadena += "Total:    Total:   \n"
    cadena += str(val_total) + "      " + str(pes_total)
    print(cadena)

def solver(method, casos, capacidad):
    mochila, combinacion = method(casos, capacidad, elementos)
    #print("la mejor solucion es: ", mochila)
    #print("la combinacion es: ", combinacion)
    return mochila, combinacion

if __name__ == "__main__":
    casos, capacidad = read_bin_file("../bin/ks_50_1")
    method = partial(recocido_algoritmo, t_inicial=t_inicial, iteraciones=iteraciones)
    solving_time = 0
    optimo_local, indices = [], []
    print(f"casos: {casos}    Capacidad: {capacidad}")
    for i in range(iteraciones):
        t_start = time()
        optimo_local, indices = solver(method, casos, capacidad)
        t_finish = time()
        solving_time += (t_finish - t_start)
    imprime_elementos(casos, indices, elementos)
    print ("Average solving time: %s sec." % (solving_time / iteraciones))