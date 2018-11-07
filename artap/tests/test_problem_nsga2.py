import os
import unittest

from artap.problem import Problem
from artap.benchmark_functions import Binh_and_Korn
from artap.algorithm_genetic import NSGA_II
from artap.results import GraphicalResults

class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        costs = ['F_1', 'F_2']

        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep

        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)
        self.max_population_number = 10
        self.max_population_size = 100


    def eval(self, x):
        return Binh_and_Korn.eval(x)


class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_nsga2(self):   
        problem = MyProblem("LocalPythonProblemNSGA_II")
        algorithm = NSGA_II(problem)
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
