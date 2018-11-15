import os
import unittest

from artap.problem import Problem
from artap.benchmark_functions import Binh_and_Korn
from artap.algorithm_genetic import NSGA_II
from artap.results import GraphicalResults, Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        costs = ['F_1', 'F_2']

        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep

        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=True)
        # self.max_population_number = 10
        # self.max_population_size = 100

    def eval(self, x):
        return Binh_and_Korn.eval(x)

    def eval_constraints(self, x):
        return Binh_and_Korn.constraints(x)


problem = MyProblem("LocalPythonProblemNSGA_II")
algorithm = NSGA_II(problem)
algorithm.options['max_population_number'] = 50
algorithm.options['max_population_size'] = 100
algorithm.run()

a = GraphicalResults(problem)
a.plot_populations()

b = Results(problem)
solution = b.pareto_values()
#print(*solution[0], sep="\n")

x, y = zip(*solution)

count = 0
wrong = 0
for sol in solution:
    if sol[0]>10. and sol[0]<100:
        count += 1
        if abs(Binh_and_Korn.approx(sol[0])-sol[1]) > 1.:
            print(sol[0], Binh_and_Korn.approx(sol[0]), sol[1], abs(Binh_and_Korn.approx(sol[0])-sol[1]))
            wrong += 1

print('Nr of solutions [10,1000],', count)
print('Wrong solutions', wrong)

#print(*solution, sep=', ')


#print(problem.populations[0].individuals[0].dominate)

#results = problem.populations[-1].individuals[-1].dominate
#print(results)
#a = [x.costs[0] for x in results]
#b = [y.costs[1] for y in results]

#matplotlib.pyplot.scatter([x.costs[0] for x in results],[y.costs[1] for y in results])
#matplotlib.pyplot.show()
#for population in problem.populations:
#    print(len(population[0].individuals[0].dominate))
