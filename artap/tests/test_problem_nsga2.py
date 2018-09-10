import unittest

from artap.problem import Problem
from artap.benchmark_functions import Binh_and_Korn
from artap.algorithm import NSGA_II
from artap.results import GraphicalResults

class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.max_population_number = 3
        self.max_population_size = 50
        self.parameters = {'x_1': { 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                           'x_2': { 'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}} 
                           
        self.get_parameters_list()
        self.costs = ['F_1', 'F_2']
        # working_dir = './workspace'
        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        return Binh_and_Korn(x)

class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_nsga2(self):   
        problem = MyProblem("LocalPythonProblemNSGA_II")
        algorithm = NSGA_II(problem)
        algorithm.run() 
        # results = GraphicalResults(problem)
        #results.plot_populations()

if __name__ == '__main__':
    unittest.main()