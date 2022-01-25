import random
from math import dist
from parser_vrp import Parser

"""
@author: Alex Fernandez y Martin Espinal
"""

class EA:
    
    def __init__(self, pc, pm, ul, li, ng, customers, vehicles, capacity, locations, center):
        """
        pc: Porcentaje de cuza
        pm: Porcentaje de mutacion
        ul: limite inferior
        li: limite superior
        ng: numero de generaciones
        parser: Parser object
        customers: cantidad de consumidores
        vehicles: cantidad me vehiculos
        capacity: capacidad maxima
        locations: lista de tuplas donde la primer
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

    def EA(self):
        """
        Ejecución del algoritmo evolutivo
        """
        genotipos, fenotipos, aptitudes = self.inicialitation()
        



if __name__ == "__main__":
    #path = "vrp_5_4_1"
    path = "vrp_484_19_1"
    parser = Parser(path)
    customers, vehicles, capacity, locations, center = parser.get_data()
    ea = EA(0.5,0.8,0,10000,100,customers, vehicles, capacity, locations, center)
    ea.EA()