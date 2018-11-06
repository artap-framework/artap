import os
import unittest

from artap.problem import Problem
from artap.algorithm_bayesopt import BayesOptSerial, BayesOptParallel


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-30, 30], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-30, 30], 'precision': 1e-1}}
        costs = ['F']

        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        result = 0
        for i in x:
            result += i*i

        return result


class TestBayesOptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_bayesopt_parallel(self):
        problem = MyProblem("LocalPythonProblemBayesOptParallel")
        algorithm = BayesOptParallel(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 50
        algorithm.run()
        # TODO: population.find_min

    def test_local_problem_bayesopt_serial(self):
        problem = MyProblem("LocalPythonProblemBayesOptSerial")
        algorithm = BayesOptSerial(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 50
        algorithm.run()
        # TODO: population.find_min


if __name__ == '__main__':
    unittest.main()
