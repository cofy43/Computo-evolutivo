import sys

casos = 0
capacidad = 0
elementos = []

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
        casos = parametros[0]
        capacidad = parametros[1]
        for line in lines:
            elementos.append(line.replace("\n", "").split(" "))
            
        print("casos: ", casos)
        print("capacidad: ", capacidad)
        print("elementos: ", elementos)
        file.close()
        

read_bin_file("../bin/ks_50_1")