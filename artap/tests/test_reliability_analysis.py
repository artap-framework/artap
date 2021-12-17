import unittest
from ..problem import Problem
from artap.reliability_analysis import FORM


class Limit_State(Problem):
    def set(self):
        self.parameters = [{'name': 'x', 'bounds': [0, 1], 'parameter_type': 'float'}]
        self.converged_point = [2.0801, 2.0801]

    def evaluate(self, x1, x2):
        return x1 ** 3 + x2 ** 3 - 18


class Test_FORM(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Integral_Monte_Carlo
    def test_local_problem(self):
        problem = Limit_State()
        algorithm = FORM(problem)
        x, beta, iteration = algorithm.run()

        self.assertAlmostEqual(int(x[0]), int(problem.converged_point[0]))
