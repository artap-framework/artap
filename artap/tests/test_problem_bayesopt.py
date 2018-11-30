import os
import unittest

from artap.problem import Problem
from artap.algorithm_bayesopt import BayesOptSerial, BayesOptParallel

from artap.results import Results

from artap.benchmark_functions import Booth

class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-30, 30], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-30, 30], 'precision': 1e-1}}
        costs = ['F']
        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep

        super().__init__(name, parameters, costs, working_dir=working_dir)
        self.options['save_data'] = False
        self.options['max_processes'] = 1

    def eval(self, x):
        return Booth.eval(x)


class TestBayesOptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_bayesopt_parallel(self):
        problem = MyProblem("LocalPythonProblemBayesOptParallel")
        problem.options["max_processes"] = 1
        algorithm = BayesOptParallel(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 100
        algorithm.run()
        # TODO - multiprocess test

        #results = Results(problem)
        #optimum = results.find_minimum(name='F').costs[0]
        #self.assertAlmostEqual(optimum, 0, places=2)

    def test_local_problem_bayesopt_serial(self):
        problem = MyProblem("LocalPythonProblemBayesOptSerial")
        algorithm = BayesOptSerial(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 200
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum, 0, places=2)

if __name__ == '__main__':
    unittest.main()
