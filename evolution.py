from utils import NSGA2Utils
from population import Population
import os
import random
import multiprocessing as mp
import threading as thrd


def f_para(obj,new_pop,i):
    """Function to parallel"""
    obj.utils.fast_nondominated_sort(obj.population)
    for front in obj.population.fronts:
        obj.utils.calculate_crowding_distance(front)
    children = obj.utils.create_children(obj.population)
    obj.population.extend(children)
    obj.utils.fast_nondominated_sort(obj.population)
    new_population = Population()
    front_num = 0
    while len(new_population) + len(obj.population.fronts[front_num]) <= obj.num_of_individuals:
        obj.utils.calculate_crowding_distance(obj.population.fronts[front_num])
        new_population.extend(obj.population.fronts[front_num])
        front_num += 1    
    obj.utils.calculate_crowding_distance(obj.population.fronts[front_num])
    obj.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
    new_population.extend(obj.population.fronts[front_num][0:obj.num_of_individuals-len(new_population)])
    
    new_pop[i] = new_population

class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):
        self.utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    

    def evolve(self):
        self.population = self.utils.create_initial_population()
        num_thrd = mp.cpu_count()
        new_pop = [Population()]*num_thrd
        pre_best = []
        
        for gen in range(self.num_of_generations):
            #Divide population1: divide to equal parts after shuffle
                        
            lst = []
            idx = self.utils.num_of_individuals // num_thrd
            tmp = 0
            for j in range(num_thrd - 1):
                evo = Evolution(self.utils.problem, num_of_individuals=idx)
                evo.population = self.utils.assign_pop(self.population, tmp, tmp + idx)
                tmp = tmp + idx
                lst.append(evo)
            evo = Evolution(self.utils.problem, num_of_individuals=idx)
            evo.population = self.utils.assign_pop(self.population, tmp, len(self.population.population))
            lst.append(evo)

            # Divide2: divide to equal parts
            # idx = self.utils.num_of_individuals // num_thrd
            # tmp = 0
            # lst = []
            # for j in range(num_thrd - 1):
            #     evo = Evolution(self.utils.problem, num_of_individuals=idx)
            #     evo.population = self.utils.assign_pop(self.population, tmp, tmp + idx)
            #     tmp = tmp + idx
            #     lst.append(evo)
            # evo = Evolution(self.utils.problem, num_of_individuals=idx)
            # evo.population = self.utils.assign_pop(self.population, tmp, len(self.population.population))
            # lst.append(evo)

            #Divide3
            # lst = [None]*num_thrd
            # idx = self.utils.num_of_individuals // num_thrd
            # for i in range(num_thrd):
            #     lst[i] = Evolution(self.utils.problem, num_of_individuals=idx)
            #     lst[i].population = Population()
            
            # tmp = 0
            # for i in range(0, idx*num_thrd,num_thrd):
            #     tmp = i
            #     for j in range(num_thrd):
            #         lst[j].population.append(self.population.population[tmp])
            #         tmp += 1
            # count = 0
            # while (tmp < len(self.population.population)):
            #     lst[count].population.extend([self.population.population[tmp]])
            #     tmp += 1
            #     count += 1
            

            t = [None]*num_thrd
            i = 0
            
            for evo in lst:
                t[i] = thrd.Thread(target=f_para, args=(evo, new_pop, i))
                t[i].start()
                i = i+1
                
            self.population = Population()
            sub_individuals = []
            best_individual = None
            for i in range(len(t)):
                t[i].join()
                self.utils.fast_nondominated_sort(new_pop[i])
                if gen > 0:
                    if (new_pop[i].fronts[0][0].objectives[0] == pre_best[i]):
                        if pre_best[i] == max(pre_best):
                            best_individual = new_pop[i].fronts[0][0]
                    
                sub_individuals.extend(new_pop[i].fronts[1:3][0])
                pre_best.append(new_pop[i].fronts[0][0].objectives[0])
               
            random.shuffle(sub_individuals)
            for i in range(len(t)):
                if best_individual is not None:
                    # new_pop[i].extend(best_individual)
                    new_pop[i].append(best_individual)
                new_pop[i].extend(sub_individuals[2*i:2*i+2]) 
                self.population.extend(new_pop[i])
        self.utils.fast_nondominated_sort(self.population)
        return self.population.fronts[0]
