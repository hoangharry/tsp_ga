from utils import NSGA2Utils
from population import Population

import multiprocessing as mp
import threading 
def parallel_evolve(lock, sub_evolution, sub_population, i):
    children = sub_evolution.utils.create_children(sub_evolution.population,lock)
    sub_evolution.population.extend(children)
    sub_evolution.utils.fast_nondominated_sort(sub_evolution.population)
    new_population = Population()
    front_num = 0
    while len(new_population) + len(sub_evolution.population.fronts[front_num]) <= sub_evolution.num_of_individuals:
        sub_evolution.utils.calculate_crowding_distance(sub_evolution.population.fronts[front_num])
        new_population.extend(sub_evolution.population.fronts[front_num])
        front_num += 1
    
    sub_evolution.utils.calculate_crowding_distance(sub_evolution.population.fronts[front_num])
    sub_evolution.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
    
    new_population.extend(sub_evolution.population.fronts[front_num][0:sub_evolution.num_of_individuals-len(new_population)])
    sub_population[i] = new_population

def thread_task(lock, sub_evolution, sub_population, i):
    lock.acquire()
    parallel_evolve(sub_evolution, sub_population, i)
    lock.release()

class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):
        self.utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    
    def evolve(self):
        #self.population = self.utils.create_initial_population()
        number_of_thread = mp.cpu_count()
        sub_population = [Population()]*4
        sub_individual_counts = self.num_of_individuals // number_of_thread
        sub_evolution = [None]*4
        #divide into subpopulation 
        for i in range(number_of_thread):
            sub_evolution[i] = Evolution(self.utils.problem, num_of_individuals = sub_individual_counts)
            sub_evolution[i].population = self.utils.create_initial_population()
            self.utils.fast_nondominated_sort(sub_evolution[i].population)
            for front in sub_evolution[i].population.fronts:
                self.utils.calculate_crowding_distance(front)

        returned_population = None
        print(self.num_of_generations)
        for gen in range(self.num_of_generations):
            if (gen % 100) == 0:
                print(gen)
            thread = [None]*4
            lock = threading.Lock()
            for i in range(number_of_thread):
                thread[i] = threading.Thread(target=parallel_evolve, args=(lock, sub_evolution[i],sub_population,i, ))
                thread[i].start()
            
            runnerup_individuals = []
            best_individuals = []
            for i in range(number_of_thread):
                thread[i].join()
                

                #print(len(sub_population[i].population))
                # self.utils.fast_nondominated_sort(sub_evolution[i].population)
                # for front in sub_evolution[i].population.fronts:
                #     self.utils.calculate_crowding_distance(front)
                # best_individuals.append(sub_evolution[i].population.fronts[0][0])
                # if len(sub_evolution[i].population.fronts[0]) > 1:
                #     runnerup_individuals.append(sub_evolution[i].population.fronts[0][1])
                #     if len(sub_evolution[i].population.fronts[0]) > 2:
                #         runnerup_individuals.append(sub_evolution[i].population.fronts[0][2])
                #     else:
                #         runnerup_individuals.append(sub_evolution[i].population.fronts[1][0])
                # elif len(sub_evolution[i].population.fronts[1]) < 2:
                #     runnerup_individuals.append(sub_evolution[i].population.fronts[1][0])
                #     runnerup_individuals.append(sub_evolution[i].population.fronts[2][0])
                # else:
                #     runnerup_individuals.extend(sub_evolution[i].population.fronts[1][0:2])

            for i in range(number_of_thread):
                # sub_evolution[i].population.extend(runnerup_individuals) #add runnerup individuals
                # self.utils.fast_nondominated_sort(sub_evolution[i].population)
                # for front in sub_evolution[i].population.fronts:
                #     self.utils.calculate_crowding_distance(front)
                # # check if the best individual 
                # if sub_evolution[i].population.fronts[0][0].objectives[0] == best_individuals[i].objectives[0]:
                #     for j in range(number_of_thread):
                #         if i == j:
                #             continue
                #         else:
                #             sub_evolution[i].population.append(best_individuals[i])
                sub_evolution[i].population = sub_population[i]
                self.utils.fast_nondominated_sort(sub_evolution[i].population)
                for front in sub_evolution[i].population.fronts:
                    self.utils.calculate_crowding_distance(front)
                #print(sub_evolution[i].population.fronts[0][0].objectives[0])



        self.population = Population()
        for pop in sub_population:
            self.population.extend(pop)
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            for f in front:
                if f is not None:
                    print(f.objectives[0])
                print("Next front")
            # if front != []:
            #     print(front.objectives[0])
        return self.population.fronts[0]
