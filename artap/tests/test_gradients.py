import unittest

from ..problem import Problem
from ..algorithm_gradient import GradientAlgorithm


class ParabolicProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "LocalPythonProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1},
                           {'name': 'x_3', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        result = x[0]**3 + x[1]**2 + x[2]**2
        return [result]


def analytic_gradient(individual):
    x = individual.vector
    dx1 = 3 * x[0]**2
    dx2 = 2 * x[1]
    dx3 = 2 * x[2]
    return [dx1, dx2, dx3]


class TestGradients(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = ParabolicProblem()
        algorithm = GradientAlgorithm(problem)
        algorithm.options['max_population_size'] = 10
        algorithm.run()

        for individual in problem.individuals:
            gradient = individual.features['gradient']
            ref_gradient = analytic_gradient(individual)
            for i in range(len(gradient)):
                self.assertAlmostEqual(gradient[i], ref_gradient[i], 2)


if __name__ == '__main__':
    unittest.main()
