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


class Tour:
    def __init__(self, tourmanager, tour=None):
        self.tourmanager = tourmanager
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for i in range(0, self.tourmanager.numberOfCities()):
                self.tour.append(None)
    
    def __len__(self):
        return len(self.tour)
    
    def __getitem__(self, index):
        return self.tour[index]
    
    def __setitem__(self, key, value):
        self.tour[key] = value
    
    def __repr__(self):
        geneString = "|"
        for i in range(0, self.tourSize()):
            geneString += str(self.getCity(i)) + "|"
        return geneString
    
    def generateIndividual(self):
        for cityIndex in range(0, self.tourmanager.numberOfCities()):
            self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
        random.shuffle(self.tour)
    
    def getCity(self, tourPosition):
        return self.tour[tourPosition]
    
    def setCity(self, tourPosition, city):
        self.tour[tourPosition] = city
        self.fitness = 0.0
        self.distance = 0
    
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.getDistance())
        return self.fitness
    
    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for cityIndex in range(0, self.tourSize()):
                fromCity = self.getCity(cityIndex)
                destinationCity = None
                if cityIndex+1 < self.tourSize():
                    destinationCity = self.getCity(cityIndex+1)
                else:
                    destinationCity = self.getCity(0)
                    tourDistance += fromCity.distanceTo(destinationCity)
            self.distance = tourDistance
        return self.distance
    
    def tourSize(self):
        return len(self.tour)
    
    def containsCity(self, city):
        return city in self.tour

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

