import unittest

from artap.problem import Problem
from artap.algorithm_sensitivity import Sensitivity


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "LocalPythonProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [2.2, 2.4], 'precision': 1e-1},
                           {'name': 'x_3', 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        result = x[0] * x[0] + 0.1 * x[1] * x[1] + x[2] * x[2]
        return [result]


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem()
        algorithm = Sensitivity(problem, ['x_2', 'x_3'])
        algorithm.options['max_population_size'] = 10
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
