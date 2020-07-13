import unittest

from ..problem import Problem
from ..algorithm_genetic import NSGAII
from ..results import Results
from random import random


class ParabolicProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "LocalPythonProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-5, 5], 'precision': 1e-1}]
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        x = individual.vector
        result = x[0]**2 + x[1]**2
        if random() > 0.9:
            raise TimeoutError
        return [result]


class TestFailedCalculation(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=20):

        problem = ParabolicProblem()
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = population_number
        algorithm.options['max_population_size'] = 40
        algorithm.options['max_processes'] = 1
        algorithm.run()

        b = Results(problem)
        optimum = b.find_optimum('F_1')  # Takes last cost function
        self.assertAlmostEqual(optimum.costs[0], 0., 2)


if __name__ == '__main__':
    unittest.main()
