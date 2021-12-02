import codigo_gray as gray
import real_binaria as rBin
import real_binaria_entera as rBinE
import numpy as np
import math


'''
'''
def parameters(lb, ub, precision, size, q, n, b, pc, pm, nvars, npop, ngen):
    l = "Lower bound: '{}' respecto a cada variable.\n".format(str(lb))
    u = "Upper bound: '{}' respecto a cada variable.\n".format(str(ub))
    p = "Precition: {} respecto a cada variable.\n".format(str(precision))
    s = "Size de la rep. binaria: {} respecto a cada varible.\n".format(str(size))
    q_p = "Parametro q = {} para jerarquias no lineales.\n".format(q)
    n_p = "Parametro n = {} para SBX.\n".format(n)
    b_p = "Parametro b = {} para mutación no uniforme.\n".format(b)
    pc_p = "Parametro pc = {}, probabilidad de cruza.\n".format(pc)
    pm_p = "Parametro pm = {}, probabilidad de mutación.\n".format(pm)
    nvar = "Numero de variables: {}\n".format(nvars)
    npop_p = "Numero de población: {}\n".format(npop)
    ngen_p = "Numero maximo de generaciones: {}\n".format(ngen)
    return ngen_p + npop_p + nvar + u + l + p + s + pm_p + pc_p + q_p + n_p + b_p

def str_lista(lista):
    s = ""
    for x in lista:
        s += str(x) + "\n"
    return s

def str_plot(data):
    s = ""
    for x in data:
        s += str(x[0]) + "\t" + str(x[1]) + "\n"
    return s

def str_gen_fen(genotipos,fenotipos):
    s = ""
    for g,f in zip(genotipos,fenotipos):
        s += "Genotipo: \n" + str(g) + "\nFenotipo:" + str(f) + "\n.................................................\n"
    return s

def str_padres(padre1,padre2,ip1,ip2):
    return ("Padre {}: \n" + str(padre1) + "\nPadre {}:\n" + str(padre2)).format(ip1,ip2)

def str_hijos(hijo1,hijo2):
    return "Hijo 1: \n" + str(hijo1) + "\nHijo 2:\n" + str(hijo2) + "\n"


def poblacion(genotipos, fenotipos):
    print("Población: \n" + str_gen_fen(genotipos,fenotipos))

def padres(padres):
    print('Indices de los Padres:', padres)
    print('frecuencia de padres:', np.bincount(padres),"\n")

def hijos(hijos_genotipo, hijos_fenotipo):
    print('Hijos:\n' + str_gen_fen(hijos_genotipo,hijos_fenotipo))

#   Función auxiliar para crear arreglos de numpy a partir de una lista.
def l_A(list):
    return np.array(list)

#   Función problema
def f(x,ub,lb):
    aptitudes = []
    for p in x:
        aptitudes.append(f_aux(p,ub,lb))
    return aptitudes

def f_aux(x,ub,lb):
    if x[0] < lb[0] or x[0] > ub[0]:
        return math.inf
    if x[1] < lb[1] or x[1] > ub[1]:
        return math.inf
    return (418.9829*2) - x[0]*math.sin(math.sqrt(abs(x[0]))) - x[1]*math.sin(math.sqrt(abs(x[1])))
    #return math.pow(x[0],2)+math.pow(x[1],2)


#   Dado un vector de reales se codifica a la representación del genoma (representación binaria)
def codificar(muestras,ub,lb,precision,size,nvar):
    genotipos = []
    for i in range(0,npop):
        genotipos.append(gray.bin_Gray(rBinE.rep_vector_bin(muestras[i],ub,lb,precision,size,nvar)))
    return genotipos

#   Se decodifica el genotipo al fenotipo.
def decodificar(genotipos, lb, precision, size, nvar):
    fenotipos = []
    for x in genotipos:
        fenotipos.append(rBinE.rep_vector_real(gray.Gray_bin(x),lb,precision,size,nvar))
    return fenotipos

#   Incilización de la población a partir de muestras aleaotrias que estan en el espacio a trabajar.
def inicializar(f,npop, nvars, ub, lb, precision, size):
    # Generar población inicial
    muestras = lb + (ub - lb) * np.random.uniform(low=0.0, high=1.0, size=[npop, nvars])
    # Genotipos
    genotipos = codificar(muestras, ub, lb, precision, size, nvars)
    # Fenotipos
    fenotipos = decodificar(genotipos, lb, precision, size, nvars)
    # Evaluar población
    aptitudes = f(fenotipos,ub,lb)
    return genotipos,fenotipos,aptitudes

def sobrante_estocastico_asignacion_entera(Pr,E,aptitudes,n):
    #print("Sobrante estocastico asignacion entera...\n")
    apt_padres = []
    for i in range(len(Pr)):
        entera = int(math.floor(E[i]))
        #print("Individio con E = {:.4f} y P = {:.4f} se seleccionara {} veces".format(E[i],Pr[i],entera))
        if entera > 0:
            for j in range(entera):
                apt_padres.append(aptitudes[i])
            E[i] -= entera
    return apt_padres[:n]

def sobrante_estocastico_asignacion_decimal(E,aptitudes,n):
    #print("Sobrante estocastico asignacion decimal...\n")
    apt_padres = []
    n_p = 0
    while n_p < n:
        i = 0
        while i < len(E) and n_p < n:
            r = np.random.uniform(0,1)
            #print("E({}) = {} >= {}".format(i,E[i],r))
            if E[i] >= r:
                apt_padres.append(aptitudes[i])
                n_p += 1
            i += 1
    return apt_padres
        

#   Selección
def sobrante_estocastico(aptitudes,n,q):
    #print("Proceso de seleccion de padres...\n")
    apt_padres = []
    apt = aptitudes
    #print("Aptitudes:\n",str_lista(apt))
    Pr = jerarquia_no_lineal(apt,q)
    E = list(map(lambda x: x*n,Pr))
    apt_padres += sobrante_estocastico_asignacion_entera(Pr,E,apt,n)
    #print("Aptitudes de los padres seleccionados por la asignación entera:\n",str_lista(apt_padres))
    p_e = len(apt_padres)
    n -= len(apt_padres)
    apt_padres += sobrante_estocastico_asignacion_decimal(E,apt,n)
    #print("Aptitudes de los padres seleccionados por la asignación decimal:\n",str_lista(apt_padres[p_e:]))
    return apt_padres



#   Probalidad de cada indivio a ser seleccionado
def jerarquia_no_lineal(aptitudes,q):
    jerarquia = aptitudes
    jerarquia.sort()
    #print("Aptitudes ordenadas:\n",str_lista(jerarquia))
    Pr = []
    c = 1 / (1 - math.pow((1 - q),len(jerarquia)))
    #print("c = {}".format(c))
    for i in range(0,len(jerarquia)):
        p = c * q * math.pow((1 - q),i)
        Pr.append(p)
    #print("Probabilidades respectivamente a las aptitudes ordenadas:\n",str_lista(Pr))
    return Pr


def SBX_alelo_hijo1(alelo_padre1,alelo_padre2,b):
    return 0.5*((alelo_padre1 + alelo_padre2) - (b*(abs(alelo_padre2-alelo_padre1))))

def SBX_alelo_hijo2(alelo_padre1,alelo_padre2,b):
    return 0.5*((alelo_padre1 + alelo_padre2) + (b*(abs(alelo_padre2-alelo_padre1))))

def SBX_hijo1(padre1,padre2,b):
    #print("Proceso de cruza hijo 1 con SBX...")
    #print(str_padres(padre1,padre2,1,2))
    hijo1 = []
    for alelo_padre1, alelo_padre2 in zip(padre1,padre2):
        hijo1.append(SBX_alelo_hijo1(alelo_padre1, alelo_padre2,b))
    #print("Hijo 1",str(hijo1))
    return hijo1

def SBX_hijo2(padre1,padre2,b):
    #print("Proceso de cruza hijo 2 con SBX...")
    #print(str_padres(padre1,padre2,1,2))
    hijo2 = []
    for alelo_padre1, alelo_padre2 in zip(padre1,padre2):
        hijo2.append(SBX_alelo_hijo1(alelo_padre1, alelo_padre2,b))
    #print("Hijo 2",str(hijo2))
    return hijo2


def SBX(genotipos, idx, pc, n, ub, lb,precision,size,nvars):
    #print("Proceso de cruza....\n")
    hijos_genotipo = []
    k = 0
    no_cruzas = 0
    for i, j in zip(idx[::2], idx[1::2]):
        flip = np.random.uniform()<=pc
        #print(str_padres(genotipos[i],genotipos[j],i,j))
        padre1 = rBinE.rep_vector_real(gray.Gray_bin(genotipos[i]),lb,precision,size,nvars)
        padre2 = rBinE.rep_vector_real(gray.Gray_bin(genotipos[j]),lb,precision,size,nvars)
        if flip:
            no_cruzas += 1
            u = np.random.uniform()
            if u <= 0.5:
                b = math.pow(2*u,1/(n+1))
            else:
                b = math.pow(1/(2*(1-u)),1/(n+1))
            #print("Beta = {}".format(b))
            h1 = SBX_hijo1(padre1,padre2,b)
            h2 = SBX_hijo2(padre1,padre2,b)
        else:
            #print("No hubo cruza")
            h1 = padre1.copy()
            h2 = padre2.copy()
        h1 = gray.bin_Gray(rBinE.rep_vector_bin(h1,ub,lb,precision,size,nvars))
        h2 = gray.bin_Gray(rBinE.rep_vector_bin(h2,ub,lb,precision,size,nvars))
        hijos_genotipo.append(h1)
        hijos_genotipo.append(h2)
        #print(str_hijos(h1,h2))
    #print("Numero de cruzas: {}\n".format(no_cruzas))
    return hijos_genotipo


def no_uniform_mutation_gen(genotipo,ub,lb,g_actual,g_max,b,pm):
    genotipo_mutado = []
    #print("Rep. vectorial\n",str(genotipo))
    for j in range(len(genotipo)):
        flip = np.random.uniform() <= pm
        if flip:
            #print("Alelo {} '{}' a mutar".format(j,genotipo[j]))
            alelo_mutado = no_uniform_mutation_alelo(genotipo[j],ub[j],lb[j],g_actual,g_max,b)
            #print("Alelo mutado {}".format(alelo_mutado))
            genotipo_mutado.append(alelo_mutado)
        else:
            genotipo_mutado.append(genotipo[j])
    return genotipo_mutado    

def no_uniform_mutation_alelo(alelo,ub,lb,g_actual,g_max,b):
    X = np.random.uniform()
    if X >= 0.5:
        alelo_mutado = alelo + mutation_extension(g_actual,ub-alelo,g_max,b)
    else:
        alelo_mutado = alelo - mutation_extension(g_actual,alelo-lb,g_max,b)
    return alelo_mutado

def mutation_extension(g_actual,y,g_max,b):
    r = np.random.uniform()
    m_e = y*(1-math.pow(r,math.pow(1-(g_actual/g_max),b)))
    #print("Delta(t,y) = {}".format(m_e))
    return m_e


def no_uniform_mutation(genotipos,ub,lb,g_actual,g_max,b,pm,precision,size,nvars):
    #print("Proceso de mutación...\n")
    genotipos_mutados = []
    no_mutaciones = 0
    for i in range(len(genotipos)):
        #print("Genotipo a mutar\n","Rep. binaria\n",str(genotipos[i]))
        genotipo = rBinE.rep_vector_real(gray.Gray_bin(genotipos[i]),lb,precision,size,nvars)
        genotipo_mutado = no_uniform_mutation_gen(genotipo,ub,lb,g_actual,g_max,b,pm)
        if genotipo != genotipo_mutado:
            #print("Genotipo mutado\n","Rep. vectorial\n",str(genotipo_mutado))
            genotipo_mutado = gray.bin_Gray(rBinE.rep_vector_bin(genotipo_mutado,ub,lb,precision,size,nvars))
            #print("Rep. binaria\n",str(genotipo_mutado),"\n")
            no_mutaciones += 1
        else:
            genotipo_mutado = genotipos[i]
            #print("No hubo mutación.\n")
        genotipos_mutados.append(genotipo_mutado)
    #print("Número de mutaciones: {}\n".format(no_mutaciones))
    return genotipos_mutados

def seleccion_coma(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes):
    return hijos_genotipo, hijos_fenotipo, hijos_aptitudes



def EA(f, lb, ub, precision, size, q, n, b, pc, pm, nvars, npop, ngen):
    print("Inicio del algoritmo evolutivo... \n")
    bg = []
    bf = []
    ba = []
    plot = []
    espacio_buscado = {}
    genotipos, fenotipos, aptitudes = inicializar(f, npop, nvars,ub,lb,precision,size)
    for generation in range(ngen):
        # Seleccion de padres
        print("Generación: {}".format(generation))
        espacio_busqueda(espacio_buscado,genotipos)
        poblacion(genotipos,fenotipos)
        apt_padres = sobrante_estocastico(aptitudes.copy(),npop,q)
        mean = np.mean(l_A(apt_padres))
        plot.append((generation,mean))
        #print("Aptitudes de los padres:\n",str_lista(apt_padres))
        idx = list(map(lambda x: aptitudes.index(x),apt_padres))
        padres(idx)
        hijos_genotipo = SBX(genotipos, idx, pc, n, ub, lb,precision,size,nvars)
        hijos_genotipo = no_uniform_mutation(hijos_genotipo,ub,lb,generation,ngen,b,pm,precision,size,nvars)
        hijos_fenotipo = decodificar(hijos_genotipo,lb,precision,size,nvars)
        hijos_aptitudes = f(hijos_fenotipo,ub,lb)
        hijos(hijos_genotipo,hijos_fenotipo)
        #Mejor individuo
        idx_best = np.argmin(l_A(aptitudes))
        bg.append(genotipos[idx_best].copy())
        bf.append(fenotipos[idx_best].copy())
        ba.append(aptitudes[idx_best])
        print("Aptitud del mejor indiviuo: {}".format(aptitudes[idx_best]))
        print("Genotipo del mejor indivio: {}".format(genotipos[idx_best]))
        print("Estadisticas sobre las aptitudes:")
        print("Maximo: {}".format(np.max(l_A(aptitudes))))
        print("Minimo: {}".format(np.min(l_A(aptitudes))))
        print("Media: {}".format(np.mean(l_A(aptitudes))))
        print("Desviacion estandar: {}".format(np.std(l_A(aptitudes))))
        #Selección de la siguiene generación
        genotipos, fenotipos, aptitudes = seleccion_coma(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes)
        print("------------------------------------------------------")
        #Fin del ciclo
    #-print('Tabla de mejores:\n', ba)
    #Regresar mejor solución
    idx = np.argmin(l_A(ba))
    print("EL mejor de todas la generaciones:")
    print("Aptitud: {}".format(ba[idx]))
    print("Fenotipo: {}".format(bf[idx]))
    print("Genotipo: {}".format(bg[idx]))
    print("Mediana: {}".format(np.median(l_A(ba))))

    est_espacio_buscado = estimacion_espacio_buscado(espacio_buscado,s_fieldsearching)
    print("Estimación de espacio buscado: {:5f}".format(est_espacio_buscado))
    na_ba = l_A(ba)
    return np.max(l_A(na_ba)), np.min(l_A(na_ba)), np.mean(l_A(na_ba)), np.median(l_A(na_ba)), np.std(l_A(na_ba)), plot


def espacio_busqueda(espacio_buscado,genotipos):
    for x in genotipos:
        n = rBinE.rep_entera(x)
        espacio_buscado[n] = 0

def size_fieldsearching(ub,lb,precision,nvars):
    s_fs = 1
    for i in range(nvars):
        u = int(rBinE.fix_precision(ub[i],precision[i])*math.pow(10,precision[i]))
        l = int(rBinE.fix_precision(lb[i],precision[i])*math.pow(10,precision[i]))
        s_fs *= u-l
    return s_fs

def estimacion_espacio_buscado(espacio_buscado,s_fieldsearching):
    return len(list(espacio_buscado.keys()))/s_fieldsearching


 #-------------------------------PARAMETROS------------------------------------------------------------   

nvars= 2 #número de variables
lb = -5000*np.ones(nvars) #lb de cada variable
ub = 5000*np.ones(nvars) #ub de cada variable
precision = [5]*nvars   #presición para variable
size = rBinE.size_rep_bin_vector(ub,lb,precision,nvars) #tamaño de la representación
q = 0.75    #parametro para jerarquias no lineales      #binaria para cada variable
n = 5      #parametro para SBX; Se recomienda 2, 5 o 20 a 30.
b = 5       #parametro para mutación no uniforme; Se recomienda 5
pc = 0.9    #prob. de cruza
pm = 0.5   #prob. de mutación
npop = 6  #número de población 50
ngen = 2  #número de generaciones 500
espacio_buscado = {}
s_fieldsearching = size_fieldsearching(ub,lb,precision,nvars)


#------------------------------------------------------------------------------------------------------
#'''
if __name__ == "__main__":
    import os
    import sys
    print(parameters(lb, ub, precision, size, q, n, b, pc, pm, nvars, npop, ngen))
    max, min, mean, median, std, plot = EA(f, lb, ub, precision, size, q, n, b, pc, pm, nvars, npop, ngen)
    ss = ("max {}\n"+"min {}\n"+"mean {}\n"+"median {}\n"+"std {}\n>\n").format(max,min,mean,median,std)
    sp = str_plot(plot) + ">\n"
    root = os.path.abspath("./")
    s_root = root + "/docs/out/stats"
    g_root = root + "/docs/out/plots"
    r_sfile = os.path.join(s_root,sys.argv[1])
    r_pfile = os.path.join(g_root,sys.argv[1])
    if not os.path.exists(r_sfile):
        sc_s = open(r_sfile,"w")
    else:
        sc_s = open(r_sfile,'a')
    if not os.path.exists(r_pfile):
        sc_p = open(r_pfile,"w")
    else:
        sc_p = open(r_pfile,'a')
    sc_s.write(ss)
    sc_s.flush()
    sc_s.close()
    sc_p.write(sp)
    sc_p.flush()
    sc_p.close()

#'''
