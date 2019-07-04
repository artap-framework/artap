import unittest

from artap.problem import Problem
from artap.algorithm_bayesopt import BayesOptSerial, BayesOptParallel

from artap.results import Results
from artap.benchmark_functions import Booth


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-10, 10]},
                      {'name': 'x_2', 'initial_value': 1.5, 'bounds': [-10, 10]}]
        costs = [{'name': 'F'}]

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        return [Booth.eval(x)]


class TestBayesOptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def xtest_local_problem_bayesopt_parallel(self):
        problem = MyProblem("TestBayesOptParallel")
        algorithm = BayesOptParallel(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 100
        algorithm.run()
        # TODO - multiprocess test

        results = Results(problem)
        optimum = results.find_minimum(name='F')
        self.assertAlmostEqual(optimum.costs[0], 0, places=2)

    def test_local_problem_bayesopt_serial(self):
        problem = MyProblem("TestBayesOptSerial")
        algorithm = BayesOptSerial(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 200
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum(name='F')
        self.assertAlmostEqual(optimum.costs[0], 0, places=2)


if __name__ == '__main__':
    unittest.main()
