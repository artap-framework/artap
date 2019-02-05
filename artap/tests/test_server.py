import unittest

from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.benchmark_functions import AckleyN2
from artap.datastore import SqliteDataStore
from artap.results import Results
from artap.datastore import DummyDataStore


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
        self.options['max_processes'] = 1

        # run server
        self.run_server()

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem("TestSimpleOptimization")
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum, 0)


if __name__ == '__main__':
    unittest.main()
