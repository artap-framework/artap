import os
import unittest

from artap.problem import Problem
from artap.benchmark_functions import AckleyN2
from artap.algorithm_genetic import NSGA_II
from artap.results import GraphicalResults, Results


class AckleyN2Test(Problem):
    """Test with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1},
                      'x_2': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1}}
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        return AckleyN2.eval(x)

    def eval_constraints(self, x):
        pass


problem = AckleyN2Test("LocalPythonProblemNSGA_II")
algorithm = NSGA_II(problem)
algorithm.options['max_population_number'] = 15
algorithm.options['max_population_size'] = 100
algorithm.run()

#a = GraphicalResults(problem)
#a.plot_populations()

b = Results(problem)
solution = b.find_minimum('F_1')
#
print('The solution is:', solution, '\n', 'optimum: -200')