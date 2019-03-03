import unittest

from artap.problem import Problem
from artap.algorithm_sensitivity import Sensitivity
from artap.datastore import DummyDataStore


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 2.5, 'bounds': [2.2, 2.4], 'precision': 1e-1},
                      'x_3': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1}}
        costs = ['F']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        result = 0
        result += x[0] * x[0] + 0.1 * x[1] * x[1] + x[2] * x[2]
        return [result]


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem("LocalPythonProblem")
        algorithm = Sensitivity(problem, ['x_2', 'x_3'])
        algorithm.options['max_population_size'] = 10
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
