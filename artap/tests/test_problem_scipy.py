import unittest

from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.benchmark_functions import AckleyN2
from artap.results import Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    # def evaluate_individual(self, individual):
    #     result = 0
    #     for i in individual.vector:
    #         result += i*i
    #
    #     individual.costs = [result]

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem("TestSimpleOptimization")
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum.costs[0], 0)


class AckleyN2Problem(Problem):
    """Test with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        parameters = {'x': {'initial_value': 2.13}, 'y': {'initial_value': 2.13}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        function = AckleyN2()
        return [function.eval(x)]


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = AckleyN2Problem("AckleyN2")
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
