import unittest

from ..problem import Problem
from ..algorithm_gradient_descent import GradientDescent
from ..results import Results


class QuadraticProblem(Problem):

    def set(self):
        self.name = "TestGradientOptimization"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector
        return [x[0]**2 + x[1]**2]


class TestGradientDescent(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_gradient_descent(self):
        problem = QuadraticProblem()

        algorithm = GradientDescent(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 10
        algorithm.run()



if __name__ == '__main__':
    unittest.main()
