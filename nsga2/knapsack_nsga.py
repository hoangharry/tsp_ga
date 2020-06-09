
''' File này sẽ giải bài toán này theo phương pháp NSGA-2.
'''

import json

from problem import Problem
from evolution import Evolution
import time
if __name__ == "__main__":
    with open("D:\Work\GA Practise\data.json", 'r') as file_data:
        data = json.load(file_data)

    MAX_WEIGHT   = data['constants']['max_weight']
    MAX_N_THINGS = len(data['things'])
    things       = data['things']


    def f_activation(v):
        return 1 if v >= 0.5 else 0

    def f_value(values):
        cumulative_val = 0
        for thing, val in zip(things, values):
            cumulative_val += f_activation(val) * thing[1]

        return -cumulative_val
    def f_constraint1(values):
        cumulative_weight = 0
        for thing, val in zip(things, values):
            cumulative_weight += f_activation(val) * thing[0]

        return cumulative_weight - MAX_WEIGHT
    start = time.clock()
    problem = Problem(
        num_of_variables=MAX_N_THINGS,
        objectives=[f_value, f_constraint1],
        variables_range=[(0, 1)],
        same_range=True,
        expand=False)
    evo = Evolution(problem, mutation_param=20, num_of_generations= 1000)
    evol = evo.evolve()
    #print(evol)
    # print(evol[0].features)
    # print(evol[0].objectives)
    print("- Max value the thieft can steal: {:8d}".format(-evol[0].objectives[0]))
    end = time.clock()
    print(start - end)
