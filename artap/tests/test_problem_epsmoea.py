import unittest

from artap.benchmark_functions import Ackley
from artap.algorithm_genetic import EpsMOEA
from artap.results import Results


class TestAckleyN222(unittest.TestCase):
    """ Tests that the eps-moea algorithm can find the global optimum of a function."""

    def test_local_problem(self, population_number=10):
        try:
            problem = Ackley(**{'dimension':1})
            algorithm = EpsMOEA(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['epsilons'] = 0.01
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 0)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
