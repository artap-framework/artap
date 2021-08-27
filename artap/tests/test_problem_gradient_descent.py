import unittest

from ..problem import Problem
from ..algorithm_gradient_descent import GradientDescent
from ..results import Results
from ..operators import CustomGenerator


class QuadraticProblem(Problem):
    def set(self):
        self.name = "TestGradientOptimization"
        self.parameters = [{'name': 'x_1', 'bounds': [0, 5]},
                           {'name': 'x_2', 'bounds': [0, 3]}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector
        return [x[0]**2 + x[1]**2]


class TestGradientDescent(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_gradient_descent_custom(self):
        problem = QuadraticProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[2.0, 1.0], [4.0, -1.0]])

        algorithm = GradientDescent(problem, generator=gen)
        algorithm.options["n_iterations"] = 20
        algorithm.options["step"] = 0.25
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=3)
        self.assertAlmostEqual(optimum.vector[1], 0, places=3)
        self.assertAlmostEqual(optimum.costs[0], 0, places=3)

    def test_gradient_descent_random(self):
        problem = QuadraticProblem()

        algorithm = GradientDescent(problem)
        algorithm.options["n_iterations"] = 20
        algorithm.options["step"] = 0.25
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=3)
        self.assertAlmostEqual(optimum.vector[1], 0, places=3)
        self.assertAlmostEqual(optimum.costs[0], 0, places=3)

    def test_gradient_descent_adaptive_custom(self):
        problem = QuadraticProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[2.0, 1.0], [4.0, -1.0]])

        algorithm = GradientDescent(problem, generator=gen)
        algorithm.options["n_iterations"] = 20
        algorithm.options["adaptive"] = True
        algorithm.options["step"] = 1.0
        algorithm.options["minimal_step"] = 1e-6
        algorithm.options["c"] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=3)
        self.assertAlmostEqual(optimum.vector[1], 0, places=3)
        self.assertAlmostEqual(optimum.costs[0], 0, places=3)