import unittest

from artap.algorithm_scipy import ScipyOpt
from artap.benchmark_functions import Ackley,GramacyLee,AlpineFunction
from artap.results import Results


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = AlpineFunction(**{'dimension':1, 'initial_value': 1.})
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum.costs[0], 0)


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = Ackley(**{'dimension':1})
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.options['calculate_gradients'] = True
        algorithm.run()

        print(problem.populations[0].individuals[3])

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 3)


if __name__ == '__main__':
    unittest.main()
