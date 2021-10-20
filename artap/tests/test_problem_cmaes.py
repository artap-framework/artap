import unittest

from ..benchmark_functions import AlpineFunction, Ackley, Rosenbrock
from ..algorithm_cmaes import CMA_ES
from ..results import Results


class TestAckley(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=5):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = CMA_ES(problem)
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


class TestAlpine(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=50):
        try:
            problem = AlpineFunction(**{'dimension': 3})
            algorithm = CMA_ES(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAlpine::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


class TestRosenbrock(unittest.TestCase):
    # unit-test  benchmarck : Rosenbrock, algorithm : SMPSO
    def test_local_problem(self):
        problem = Rosenbrock(**{'dimension': 1})
        algorithm = CMA_ES(problem)
        algorithm.options['max_population_number'] = 200
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 10
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertEqual(optimum.costs[0], problem.global_optimum)


if __name__ == '__main__':
    unittest.main()
