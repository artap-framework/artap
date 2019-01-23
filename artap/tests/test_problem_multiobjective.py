import unittest

from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.algorithm_genetic import GeneticAlgorithm


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01},
                      'x_2': {'initial_value': 10, 'bounds': [-10, -5], 'precision': 1e-6},
                      'x_3': {'initial_value': 10, 'bounds': [0, 5], 'precision': 0.01}}

        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))

    def evaluate(self, x):
        f1 = 0

        for i in x:
            f1 += i*i

        f2 = -(abs(x[0] - x[1]) + abs(x[1] - x[2]) + abs(x[2] - x[1]))

        return [f1, f2]


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_genetic(self):
        problem = MyProblem("LocalPythonProblem")
        algorithm = GeneticAlgorithm(problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 10
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
