from utils import NSGA2Utils
from population import Population
import os
import random
import multiprocessing as mp
import threading as thrd


def f_para(obj, new_pop, i):
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
        lst = []
        idx = self.utils.num_of_individuals // num_thrd
        tmp = 0
        for j in range(num_thrd - 1):
            evo = Evolution(self.utils.problem, num_of_individuals=idx)
            evo.population = self.utils.assign_pop(self.population, tmp, tmp + idx)
            tmp = tmp + idx
            lst.append(evo)
        evo = Evolution(self.utils.problem, num_of_individuals=self.utils.num_of_individuals - tmp)
        evo.population = self.utils.assign_pop(self.population, tmp, len(self.population.population))
        lst.append(evo)
            
        for gen in range(self.num_of_generations):
            t = [None]*num_thrd
            id_num = 0
            pre_best = []
            for evo in lst:
                t[id_num] = thrd.Thread(target=f_para, args=(evo, new_pop, id_num))
                t[id_num].start()
                id_num = id_num + 1
            runnerup_individuals = []
            best_individuals = []
            for i in range(num_thrd):
                t[i].join()
                self.utils.fast_nondominated_sort(new_pop[i])
                # if gen > 0:
                #     if (new_pop[i].fronts[0][0].objectives[0] == pre_best[i]):
                #         if pre_best[i] == max(pre_best):
                #             best_individual = new_pop[i].fronts[0][0]
                runnerup_individuals.extend(new_pop[i].fronts[1:3][0])
                best_individuals.append(new_pop[i].fronts[0][0])
            # for i in range(len(t)):
            #     if best_individual is not None:
            #         # new_pop[i].extend(best_individual)
            #         new_pop[i].append(best_individual)
            #     new_pop[i].extend(sub_individuals[2*i:2*i+2]) 
            #     self.population.extend(new_pop[i])
            for i in range(num_thrd):
                new_pop[i].extend(runnerup_individuals)
                self.utils.fast_nondominated_sort(new_pop[i])
                if new_pop[i].fronts[0][0].objectives[0] == best_individuals[i].objectives[0]:
                    for j in range(num_thrd):
                        if i == j:
                            continue
                        else:
                            new_pop[j].append(best_individuals[i])

            for i in range(num_thrd):
                self.utils.fast_nondominated_sort(new_pop[i])
                temp_population = Population()
                front_idx = 0
                while len(temp_population) + len(new_pop[i].fronts[front_idx]) <= lst[i].num_of_individuals:
                    self.utils.calculate_crowding_distance(new_pop[i].fronts[front_idx])
                    temp_population.extend(new_pop[i].fronts[front_idx])
                    front_idx +=1
                lst[i].population = temp_population

        self.population = Population()
        for pop in new_pop:
            self.population.extend(pop)
        self.utils.fast_nondominated_sort(self.population)
        return self.population.fronts[0]
