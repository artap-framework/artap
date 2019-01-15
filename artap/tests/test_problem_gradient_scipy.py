import unittest

from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.algorithm_gradient_descent import GradientDescent


class GradientProblem(Problem):
    """Test of calculation of gradientS"""

    def __init__(self, name):
        parameters = {'x': {'initial_value': 2.13}, 'y': {'initial_value': 2.13}}
        costs = ['F_1']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))

    def eval(self, x):
        return (x[0]-1)**2 + x[1]**2


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = GradientProblem("TestAckleyN2")
        algorithm = GradientDescent(problem)
        algorithm.options["x0"] = [10, 10]
        algorithm.options["n_iterations"] = 11
        algorithm.options["h"] = 0.3
        print(algorithm.run()[-1])


if __name__ == '__main__':
    unittest.main()
