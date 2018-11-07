import os
import unittest
from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']
        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        result = 0
        for i in x:
            result += i*i   

        return result


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem(self):           
        problem = MyProblem("LocalPythonProblem")
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()                

        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, 0)


if __name__ == '__main__':
    unittest.main()
