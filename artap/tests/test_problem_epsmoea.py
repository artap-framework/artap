import unittest

from ..benchmark_functions import Ackley
from ..algorithm_genetic import EpsMOEA
from ..benchmark_pareto import ZDT1
from ..results import Results
from ..quality_indicator import epsilon_add


class TestAckleyN222(unittest.TestCase):
    """ Tests that the eps-moea algorithm can find the global optimum of a function."""

    def test_local_problem(self, population_number=10):
        try:
            problem = Ackley(**{'dimension': 1})
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


class TestZDT1(unittest.TestCase):
    # integration test -- tests the total functionality of eps-MOEA

    def test_local_problem(self):
        problem = problem = ZDT1()
        algorithm = EpsMOEA(problem)
        algorithm.options['max_population_number'] = 500
        algorithm.options['max_population_size'] = 100  # according to the literature
        algorithm.options['max_processes'] = 1
        algorithm.options['epsilons'] = 0.05
        algorithm.run()

        results = Results(problem)
        vals = results.pareto_values(algorithm.archive)
        exact = problem.pareto_front(vals[0])
        self.assertLessEqual(epsilon_add(exact, vals), 0.2)

if __name__ == '__main__':
    unittest.main()
