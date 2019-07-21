import unittest
from artap.problem import Problem
from artap.algorithm_gradient_descent import GradientDescent


class GradientProblem(Problem):
    """Test of calculation of gradientS"""

    def set(self):
        self.name = TestAckleyN2
        self.parameters = [{'name': 'x', 'initial_value': 2.13}, {'name': 'y', 'initial_value': 2.13}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector
        return [(x[0]-1)**2 + x[1]**2]


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = GradientProblem()
        algorithm = GradientDescent(problem)
        algorithm.options["x0"] = [10, 10]
        algorithm.options["n_iterations"] = 8
        algorithm.options["h"] = 0.1
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
