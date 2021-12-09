import matplotlib.pyplot as plt
"""
@author: Martin Felipe Espinal Cruces
Pequeño script para generar las gráficas de convergencia
dado un archivo con la siguiente estructura:
...
----------------------------------
Minima=0.0011142833743145867
Media=10.881775063329597
Maxima=0.00207233857703679
Desviación Estandar=11.138195662798797
------------------------------------
...
Así como la generación de tablas en formato latex para el 
reporte
"""

def genera_grafica_convergencia(nombre, problema):
    # Se optienen los datos de los archivos guardados previamente
    generaciones = [x+1 for x in range(20)]
    medianas = []
    try:
        f = open(nombre, 'rb')
    except OSError:
        print("Ocurrio un error al leer el archivo:", nombre)
        print("Por tanto se omitiran los datos de dicho archivo en la grafica")
    with f:
        for line in f:
            line = str(line)
            if "Media" in line:
                valor = line.split("=")[1].replace("\\n", "")
                valor = valor.replace("\'", "")
                medianas.append(float(valor))
    #construccion de la grafica
    _, ax = plt.subplots()
    #Colocamos una etiqueta en el eje Y
    ax.set_ylabel('Medianas')
    #Colocamos una etiqueta en el eje X
    ax.set_xlabel('Generaciones')
    #Colocamos una titulo
    ax.set_title('Grafica de convergencia')
    #Creamos la grafica de barras utilizando 'paises' como eje X y 'ventas' como eje y.
    # plt.subplot(len(medianas))
    plt.plot(generaciones, medianas, color = "c")
    plt.savefig('{name}.png'.format(name=problema))

def genera_reporte_latex(archivo):
    medianas = []
    minimas = []
    maxima = []
    desviasciones = []
    try:
        f = open(archivo, 'rb')
    except OSError:
        print("Ocurrio un error al leer el archivo:", archivo)
        print("Por tanto se omitiran los datos de dicho archivo en la grafica")
    with f:
        for line in f:
            line = str(line)
            if "Minima" in line:
                valor = line.split("=")[1].replace("\\n", "")
                valor = valor.replace("\'", "")
                minimas.append(float(valor))
            elif "Media" in line:
                valor = line.split("=")[1].replace("\\n", "")
                valor = valor.replace("\'", "")
                medianas.append(float(valor))
            elif "Maxima" in line:
                valor = line.split("=")[1].replace("\\n", "")
                valor = valor.replace("\'", "")
                maxima.append(float(valor))
            elif not "-" in line:
                valor = line.split("=")[1].replace("\\n", "")
                valor = valor.replace("\'", "")
                desviasciones.append(float(valor))
        print("\\begin{tabular}{| c | c | c | c | c |}")
        print("\t\\hline")
        print("\tGeneracion &Mínima &Media &Maxima &Desviación \\\\")
        print("\t\\hline")
        for i in range(20):
            print("\t {g} &{min} &{med} &{max} &{des} \\\\".format(g=i+1, min=minimas[i], med=medianas[i], max=maxima[i], des=desviasciones[i] ))
            print("\t\\hline")
        print("\t Promedio &{min} &{med} &{max} &{des} \\\\".format(min=sum(minimas)/len(minimas), med=sum(medianas)/len(medianas), max=sum(maxima)/len(maxima), des=sum(desviasciones)/len(desviasciones) ))
        print("\t\\hline")
        print("\\end{tabular}")

genera_grafica_convergencia("Resultados/Ackley/Resultados_problema_Ackley_total.txt", "Ackley")
genera_reporte_latex("Resultados/Ackley/Resultados_problema_Ackley_total.txt")
print()
print()
genera_grafica_convergencia("Resultados/Eggholder/Resultados_problema_Eggholder_total.txt", "Eggholder")
genera_reporte_latex("Resultados/Eggholder/Resultados_problema_Eggholder_total.txt")
print()
print()
genera_grafica_convergencia("Resultados/Rastrigin/Resultados_problema_Rastrigin_total.txt", "Rastrigin")
genera_reporte_latex("Resultados/Rastrigin/Resultados_problema_Rastrigin_total.txt")
print()
print()
genera_grafica_convergencia("Resultados/Rosenbrock/Resultados_problema_Rosenbrock_total.txt", "Rosenbrock")
genera_reporte_latex("Resultados/Rosenbrock/Resultados_problema_Rosenbrock_total.txt")