import unittest 
from context import Problem
from context import ScipyNelderMead   
from context import Sensitivity
from scipy.optimize import minimize

class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 10
        self.parameters = {'x_1': { 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                           'x_2': { 'initial_value': 2.5, 'bounds': [2.2, 2.4], 'precision': 1e-1},
                           'x_3': { 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1}
        }
        self.costs = ['F_1']

        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        result = 0
        result += x[0] * x[0] + 0.1 * x[1] * x[1] + x[2] * x[2]   

        # print(result)
        return result

class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem(self):   
        problem = MyProblem("LocalPythonProblem")
        algorithm = Sensitivity(problem, ['x_2', 'x_3'])
        algorithm.run()        
        problem.read_from_database()

if __name__ == '__main__':
    unittest.main()
    

