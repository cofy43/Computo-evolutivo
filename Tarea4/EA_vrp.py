import random
import math

from numpy import mat
from parser_vrp import Parser

class EA:
    
    def __init__(self, pc, pm, ul, li, ng, customers, vehicles, capacity, locations):
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

    def inicialitation(self):
        rotes = [[self.capacity, []] for _ in range(self.vehicles)]
        for i in range(self.customers):
            idx_vehicle = random.randint(0, self.vehicles-1)
            location = self.locations[i]
            diff = rotes[idx_vehicle][0] - location[0]
            if diff >= 0:
                rotes[idx_vehicle][1].append(location)
                rotes[idx_vehicle][0] = diff
            else:
                i -= 1
        return rotes

    def euclidian_distance(self, p1, p2):
        return math.sqrt( math.pow((p1[0] - p2[0]), 2 ) - math.pow((p1[1], p2[1]), 2))



if __name__ == "__main__":
    #path = "vrp_5_4_1"
    path = "vrp_484_19_1"
    parser = Parser(path)
    customers, vehicles, capacity, locations = parser.get_data()
    ea = EA(0.5,0.8,0,10000,100,customers, vehicles, capacity, locations)
    for v in ea.inicialitation():
        print(v)
        total = 0
        for c in v[1]:
            total += c[0]
        print("total = ", total)
        print()
