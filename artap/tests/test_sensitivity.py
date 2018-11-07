import unittest 

from artap.problem import Problem
from artap.algorithm import Sensitivity


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 10
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 2.5, 'bounds': [2.2, 2.4], 'precision': 1e-1},
                      'x_3': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1}}
        costs = ['F_1']
        # working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep
        # super().__init__(name, parameters, costs, working_dir=working_dir)

        super().__init__(name, parameters, costs)
        self.save_data = False  # For tests is not necessary to save data

    def eval(self, x):
        result = 0
        result += x[0] * x[0] + 0.1 * x[1] * x[1] + x[2] * x[2]
        return result


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem(self):   
        problem = MyProblem("LocalPythonProblem")
        algorithm = Sensitivity(problem, ['x_2', 'x_3'])
        algorithm.run()        
        

if __name__ == '__main__':
    unittest.main()
