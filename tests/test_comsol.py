import unittest
import os
from context import ComsolExecutor
from context import Problem   
from scipy.optimize import minimize
import getpass

class TestProblem(Problem):

    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1': {'initial_value':10}, 
                           'x_2': {'initial_value':10}}
        self.costs = ['F1']
        
        curr_dir = os.path.abspath(os.curdir)
        input_file =curr_dir + "/tests/parameters.txt"
        output_file =curr_dir + "/tests/max.txt"
        model_file =  curr_dir + "/tests/elstat.java"
        
        self.executor = ComsolExecutor(2, 1, input_file, output_file, model_file)
        super().__init__(name, self.parameters, self.costs)
    
    def eval(self, x):        
        result = self.executor.eval(x)
        return result

class TestSimpleComsolOptimization(unittest.TestCase):
    def test_upper(self):        
                
        problem = TestProblem("LocalComsolProblem")        
        result = problem.eval([1, 1])
        print(result)      
        self.assertAlmostEqual(result, 11.294090668382257)

if __name__ == '__main__':
    unittest.main()