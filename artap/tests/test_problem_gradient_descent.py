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
        algorithm.options["algorithm"] = "fixed"
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
        algorithm.options["algorithm"] = "fixed"
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
        algorithm.options["algorithm"] = "adaptive"
        algorithm.options["step"] = 1.0
        algorithm.options["minimal_step"] = 1e-6
        algorithm.options["c"] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=3)
        self.assertAlmostEqual(optimum.vector[1], 0, places=3)
        self.assertAlmostEqual(optimum.costs[0], 0, places=3)

    def test_gradient_descent_adagrad_custom(self):
        problem = QuadraticProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[2.0, 1.0], [4.0, -1.0]])

        algorithm = GradientDescent(problem, generator=gen)
        algorithm.options["n_iterations"] = 50
        algorithm.options["algorithm"] = "adagrad"
        algorithm.options["step"] = 2.0
        algorithm.options["minimal_step"] = 1e-6
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=3)
        self.assertAlmostEqual(optimum.vector[1], 0, places=3)
        self.assertAlmostEqual(optimum.costs[0], 0, places=3)

    def test_gradient_descent_rmsprop_custom(self):
        problem = QuadraticProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[2.0, 1.0], [4.0, -1.0]])

        algorithm = GradientDescent(problem, generator=gen)
        algorithm.options["n_iterations"] = 50
        algorithm.options["algorithm"] = "rmsprop"
        algorithm.options["step"] = 1.0
        algorithm.options["decay_rate"] = 0.7
        algorithm.options["minimal_step"] = 1e-6
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        self.assertAlmostEqual(optimum.vector[0], 0, places=0)
        self.assertAlmostEqual(optimum.vector[1], 0, places=0)
        self.assertAlmostEqual(optimum.costs[0], 0, places=1)

    def test_gradient_descent_adam_custom(self):
        problem = QuadraticProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[2.0, 1.0], [4.0, -1.0]])

        algorithm = GradientDescent(problem, generator=gen)
        algorithm.options["n_iterations"] = 100
        algorithm.options["algorithm"] = "adam"
        algorithm.options["step"] = 2.0
        algorithm.options["beta1"] = 0.5
        algorithm.options["beta2"] = 0.8
        algorithm.options["minimal_step"] = 1e-6
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum('F_1')
        print(optimum)
        self.assertLessEqual(abs(optimum.vector[0]), 1e-6)
        self.assertLessEqual(abs(optimum.vector[1]), 1.0)
        self.assertLessEqual(abs(optimum.costs[0]), 1.0)
