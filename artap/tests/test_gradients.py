import unittest

from artap.problem import Problem
from artap.algorithm_gradient import GradientAlgorithm


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "LocalPythonProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1},
                           {'name': 'x_3', 'initial_value': 2.5, 'bounds': [5, 5], 'precision': 1e-1}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        result = x[0] * x[0] + x[1] * x[1] + x[2] * x[2]
        return [result]


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem()
        algorithm = GradientAlgorithm(problem)
        algorithm.options['max_population_size'] = 4
        algorithm.run()

        for individual in problem.populations[0].individuals:
            print(individual.features['gradient'])
            print(individual.vector)


if __name__ == '__main__':
    unittest.main()
