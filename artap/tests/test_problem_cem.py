import unittest

from ..benchmark_functions import Ackley
from ..algorithm_cem import CEM
from ..results import Results


class TestAckley1(unittest.TestCase):
    """ Tests that the CEM can find the global optimum. """

    def test_local_problem(self, population_number=5):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = CEM(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 10
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
