import random
import numpy as np
from math import dist
from parser_vrp import Parser

"""
@author: Alex Fernandez y Martin Espinal
"""

class EA:
    
    def __init__(self, pc, pm, ul, li, ng, np, customers, vehicles, capacity, locations, center):
        """
        pc: Porcentaje de cuza
        pm: Porcentaje de mutacion
        ul: Límite inferior
        li: Límite superior
        ng: Número de generaciones
        np: Número de población
        parser: Parser con información del problema
        customers: Cantidad de consumidores
        vehicles: Cantidad me vehículos
        capacity: Capacidad máxima
        locations: Lista de tuplas donde la primer
                   entrada es la demanda, la segunda
                   entrada es la coordenada x y la tercer
                   entrada es la coordenada y.
        center: Punto de distribucion en el problema.
        """
        self.pc = pc
        self.pm = pm
        self.ul = ul
        self.li = li
        self.ng = ng
        self.np = np
        self.customers = customers
        self.vehicles = vehicles
        self.capacity = capacity
        self.locations = locations
        self.center = center

    def inicialitation(self):
        """
        Funcion que se encarga de asignar aleatoriamente 
        las locaciones a la los vehículos disponibles
        procurando no exceder la capacidad indicada
        """
        #Generamos una lista con dos entradas, la primera
        #representará la capacidad del vehículo e irá
        #actualizando según la locación aleatoriamente
        #seleccionada. La segunda entrada representará la
        #lista de locaciones para un vehículo
        routes = [[self.capacity, []] for _ in range(self.vehicles)]
        for i in range(self.customers-1):
            idx_vehicle = random.randint(0, self.vehicles-1)
            location = self.locations[i]
            diff = routes[idx_vehicle][0] - location[0]
            #Verificamos que la locación seleccionada para un
            #vehículo no exceda la capacidad máxima
            if diff >= 0:
                routes[idx_vehicle][1].append(location)
                routes[idx_vehicle][0] = diff
            else:
            #Si excede repetimos el experimento
                i -= 1
        return routes, routes, self.fitnes(routes)

    def euclidian_distance(self, p1, p2):
        """
        Función auxiliar que se encarga de calcular
        la distancia euclidiana de dos puntos con
        la ayuda de la paqueteria math
        """
        return dist(p1, p2)

    def fitnes(self, routes):
        """
        Funcion encargada de la evaluacion de la
        distancia recorrida por los vehiculos
        """
        apts = []
        for vehicle in routes:
            total = 0
            length = len(vehicle[1])
            #Verificamos que los vehículos tengan
            #asignados al menos una ruta
            if length > 0:
                #Distancia entre el origen y el primer
                #punto de distribucion de i-esimo vehiculo
                p1 = vehicle[1][0][1:]
                total += self.euclidian_distance(self.center, p1)
                for i in range(1, length-1, 2):                    
                    p1 = vehicle[1][i][1:]
                    p2 = vehicle[1][i+1][1:]
                    total += self.euclidian_distance(p1, p2)
                #Como recorremos la lista de puntos de distribucion
                #de los vehículos en pasos de dos podemos caer en 
                #caso de que dicha liste tenga una longitud impar y
                #esta condicion se encarga de cubrir ese caso para que
                #la suma de distacia sea correcta
                if length%2 != 0:
                    p1 = vehicle[1][length-2][1:]
                    p2 = vehicle[1][length-1][1:]
                    total += self.euclidian_distance(p1, p2)
                #Calculamos la distancia del último punto de distribución
                #al punto de origen
                p1 = vehicle[1][length-1][1:]                
                total += self.euclidian_distance(p1, self.center)
            apts.append(total)
        return apts

    def tournament_selection(self, aptitudes, npop):
        parents = []
        temp_aptitudes = aptitudes.copy()
        for _ in range(npop):
            c1 = np.random.randint(low=0, high=len(temp_aptitudes))
            c2 = np.random.randint(0, len(temp_aptitudes))
            
            p1 = temp_aptitudes[c1]
            p2 = temp_aptitudes[c2]
            if p1 > p2:
                parents.append(c1)
            else:
                parents.append(c2)
            temp_aptitudes.pop()
        return parents

    def crossover(self, indx, genotipos, pc):
        """
        Función encargada de realizar la cruza de un punto
        pero por la representación elegida (una lista de
        locaciones), la cruza se realizara de manera individual
        indx: Indices de los padres elegidos
        genotipos: Padres con la siguiente estructura.
                   La primer entrada es la capacidad máxima
                   disponible y la segunda es la lista con
                   las locaciones que recorrerá
        pc: Probabilidad de cruza
        """
        hijos_genitipo = []
        for i in indx:
            print(i)
            flip = np.random.uniform() <= pc
            if flip:
                individuo = genotipos[i]
                ruta = individuo[1]
                punto_cruza = 0
                nueva_ruta = []
                if len(ruta)-1 > 0:
                    punto_cruza = np.random.randint(0, len(ruta)-1)
                    nueva_ruta = [ruta[punto_cruza]] + ruta[0:punto_cruza] + ruta[punto_cruza+1:] + [ruta[punto_cruza+1]]
                nuevo_individuo = [individuo[0], nueva_ruta]
                hijos_genitipo.append(nuevo_individuo)
            else:
                hijos_genitipo.append(genotipos[i])
        return hijos_genitipo

    def mutation(self, genotipos_hijos, pm):
        """
        genotipos_hijos: Resultados de la curza
        pm: Porcentaje de muta
        """
        hijos_genitipo = []
        for gen in genotipos_hijos:
            flip = np.random.uniform() <= pm
            if flip and len(gen[1]) > 0:
                ruta = gen[1]
                i1 = np.random.randint(0, len(ruta))
                i2 = np.random.randint(0, len(ruta))
                temp = ruta[i1]
                ruta[i1] = ruta[i2]
                ruta[i2] = temp
                hijos_genitipo.append([gen[0], ruta])
            else:
                hijos_genitipo.append(gen)
        return hijos_genitipo

    def estadisticas(self, generacion, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes, padres):
        print('---------------------------------------------------------')
        print('Generación:', generacion)
        print('Población:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1,1), genotipos, fenotipos, aptitudes.reshape(-1, 1), aptitudes.reshape(-1, 1)/np.sum(aptitudes)), 1))
        print('Padres:', padres)
        print('frecuencia de padres:', np.bincount(padres))
        #print('Hijos:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1, 1), hijos_genotipo, hijos_fenotipo, hijos_aptitudes.reshape(-1, 1), hijos_aptitudes.reshape(-1, 1)/np.sum(hijos_aptitudes)), 1))
        print('Desempeño en línea para t=1: ', np.mean(aptitudes))
        print('Desempeño fuera de línea para t=1: ', np.max(aptitudes))
        print('Mejor individuo en la generación: ', np.argmax(aptitudes))

    def seleccion_mas(self, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes):
        """
        """
        mitad = int(len(fenotipos)/2)
        nuevo_fenotipo = [[] for _ in range(len(fenotipos))]
        nuevo_aptitudes = [0 for _ in range(len(fenotipos))]
        #ordenamos con el algoritmo insertion sort los
        #padres como los hijos en base a la aptitud
        
        for i in range(len(aptitudes)):
            keyp = aptitudes[i]
            keyfp = fenotipos[i]
            j = i-1
            while j >= 0 and keyp < aptitudes[j]:
                aptitudes[j+1] = aptitudes[j]
                fenotipos[j+1] = fenotipos[j]
                j -= 1
            aptitudes[j+1] = keyp
            fenotipos[j+1] = keyfp
        aptitudes.reverse()
        fenotipos.reverse()
        for i in range(len(hijos_aptitudes)):
            key = hijos_aptitudes[i]
            keyf = hijos_fenotipo[i]
            j = i-1
            while j >= 0 and key < hijos_aptitudes[j]:
                hijos_aptitudes[j+1] = hijos_aptitudes[j]
                hijos_fenotipo[j+1] = hijos_fenotipo[j]
                j -= 1
            hijos_aptitudes[j+1] = key
            hijos_fenotipo[j+1] = keyf
        hijos_fenotipo.reverse()
        hijos_aptitudes.reverse()
        for i in range(mitad):
            nuevo_aptitudes.append(aptitudes[i])
            nuevo_fenotipo.append(fenotipos[i])
        for i in range(int(mitad/2)):
            nuevo_aptitudes.append(hijos_aptitudes[i])
            nuevo_fenotipo.append(hijos_fenotipo[i])
        
        return nuevo_fenotipo, nuevo_fenotipo, nuevo_aptitudes

    def EA(self):
        """
        Ejecución del algoritmo evolutivo
        """
        genotipos, fenotipos, aptitudes = self.inicialitation()
        #minima = np.copy(genotipos[np.argmin(aptitudes)])
        #media = np.median(aptitudes)
        #maximo = np.copy(genotipos[np.argmax(aptitudes)])
        #desviacion = np.std(aptitudes)
        #ba = np.zeros((self.ng, 1))
        for i in range(self.ng):
            #Seleccion de padres
            indx = self.tournament_selection(aptitudes, self.np)
            print(indx)
            #Cruza
            hijos_genotipo = self.crossover(indx,genotipos,self.pc)
            print("hijos_genotipo")
            print(hijos_genotipo)
            #Mutación
            hijos_genotipo = self.mutation(hijos_genotipo, self.pm)
            hijos_fenotipo = hijos_genotipo
            hijos_aptitudes = self.fitnes(hijos_genotipo)
            print("hijos_genotipo")
            print(hijos_genotipo)
            self.estadisticas(i, genotipos, fenotipos, np.array(aptitudes), np.array(hijos_genotipo), np.array(hijos_fenotipo), np.array(hijos_aptitudes), indx)
            #Seleccion de la siguiente generación
            genotipos, fenotipos, aptitudes = self.seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes)


if __name__ == "__main__":
    path = "vrp_5_4_1"
    #path = "vrp_484_19_1"
    parser = Parser(path)
    customers, vehicles, capacity, locations, center = parser.get_data()
    ea = EA(0.5,0.4,0.5,10000,10,vehicles, customers, vehicles, capacity, locations, center)
    ea.EA()