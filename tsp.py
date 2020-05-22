import math
import random
import time
from problem import Problem
from utils import NSGA2Utils
from population import Population
from evolution import Evolution
class City:
    def __init__(self, x=None, y=None):
        self.x = None
        self.y = None
        if x is not None:
            self.x = x
        else:
            self.x = int(random.random() * 200)
        if y is not None:
            self.y = y
        else:
            self.y = int(random.random() * 200)
   
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distanceTo(self, city):
        xDistance = abs(self.getX() - city.getX())
        yDistance = abs(self.getY() - city.getY())
        distance = math.sqrt( (xDistance*xDistance) + (yDistance*yDistance) )
        return distance
    
    def __repr__(self):
        return str(self.getX()) + ", " + str(self.getY())


class TourManager:
    destinationCities = []
    
    def addCity(self, city):
        self.destinationCities.append(city)
    
    def getCity(self, index):
        idx = int(index)
        return self.destinationCities[idx]
    
    def numberOfCities(self):
        return len(self.destinationCities)


if __name__ == '__main__':
   
    tourmanager = TourManager()
    
    # Create and add our cities
    city = City(60, 200)
    tourmanager.addCity(city)
    city2 = City(180, 200)
    tourmanager.addCity(city2)
    city3 = City(80, 180)
    tourmanager.addCity(city3)
    city4 = City(140, 180)
    tourmanager.addCity(city4)
    city5 = City(20, 160)
    tourmanager.addCity(city5)
    city6 = City(100, 160)
    tourmanager.addCity(city6)
    city7 = City(200, 160)
    tourmanager.addCity(city7)
    city8 = City(140, 140)
    tourmanager.addCity(city8)
    city9 = City(40, 120)
    tourmanager.addCity(city9)
    city10 = City(100, 120)
    tourmanager.addCity(city10)
    city11 = City(180, 100)
    tourmanager.addCity(city11)
    city12 = City(60, 80)
    tourmanager.addCity(city12)
    city13 = City(120, 80)
    tourmanager.addCity(city13)
    city14 = City(180, 60)
    tourmanager.addCity(city14)
    city15 = City(20, 40)
    tourmanager.addCity(city15)
    city16 = City(100, 40)
    tourmanager.addCity(city16)
    city17 = City(200, 40)
    tourmanager.addCity(city17)
    city18 = City(20, 20)
    tourmanager.addCity(city18)
    city19 = City(60, 20)
    tourmanager.addCity(city19)
    city20 = City(160, 20)
    tourmanager.addCity(city20)
    
    
    # Initialize population
    start_time = time.time()
    
    def f_round(v):
        return int(v + 1) if (v - int(v)) > 0.5 else int(v) 

    def getvalue(idx_lst):

        value = 0
        if len(idx_lst) > len(set(idx_lst)):
            value = 1000000
        for idxf in idx_lst:
            idx = f_round(idxf)
            fromCity = tourmanager.getCity(idx)
            destination = None
            if idx + 1 < len(tourmanager.destinationCities):
                destination = tourmanager.getCity(idx + 1)
            else:
                destination = tourmanager.getCity(idx_lst[0])
            value += fromCity.distanceTo(destination)
        return -value
        
    prob = Problem(num_of_variables=len(tourmanager.destinationCities),
    objectives=[getvalue],
    variables_range=[(0,len(tourmanager.destinationCities) - 1)],
    expand=False
    )
    evo = Evolution(prob, mutation_param = 20, num_of_generations=100)
    evol = evo.evolve()
    print(-evol[0].objectives[0])

