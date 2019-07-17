import unittest

from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.benchmark_functions import AckleyN2
from artap.results import Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "TestSimpleOptimization"
        self.parameters = [{'name': 'x_1', 'initial_value': 10}]
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        x = individual.vector
        result = 0
        for i in x:
            result += i*i

        return [result]


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem()
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum.costs[0], 0)


class AckleyN2Problem(Problem):
    """Test with a simple 2 variable Ackley N2 formula"""

    def set(self):
        self.name = "AckleyN2"
        self.parameters = {'x': {'initial_value': 2.13}, 'y': {'initial_value': 2.13}}
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        function = AckleyN2()
        return [function.eval(individual.vector)]


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = AckleyN2Problem()
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.options['calculate_gradients'] = True
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum.costs[0], -200, 3)


if __name__ == '__main__':
    unittest.main()
