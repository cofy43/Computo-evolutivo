import matplotlib.pyplot as plt

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

genera_grafica_convergencia("Resultados/Ackley/Resultados_problema_Ackley_total.txt", "Ackley")
genera_grafica_convergencia("Resultados/Eggholder/Resultados_problema_Eggholder_total.txt", "Eggholder")
genera_grafica_convergencia("Resultados/Rastrigin/Resultados_problema_Rastrigin_total.txt", "Rastrigin")
genera_grafica_convergencia("Resultados/Rosenbrock/Resultados_problema_Rosenbrock_total.txt", "Rosenbrock")