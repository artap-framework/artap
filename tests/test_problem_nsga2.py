import unittest
from context import Problem
from context import Binh_and_Korn
# from context import GeneticAlgorithm
#from artap.algorithm_nsga2 import *
from context import NSGA_II
from scipy.optimize import minimize

class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.max_population_number = 3
        self.max_population_size = 50
        self.parameters = {'x_1': { 'initial_value': 0, 'bounds': [0, 5], 'precision': 1e-9},
                           'x_2': { 'initial_value': 0, 'bounds': [0, 3], 'precision': 1e-9}} 
                           
        
        self.costs = ['F_1', 'F_2']

        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        return Binh_and_Korn(x)

class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_nsga2(self):   
        problem = MyProblem("LocalPythonProblem")        
        algorithm = NSGA_II(problem)
        algorithm.run()        

if __name__ == '__main__':
     unittest.main()


