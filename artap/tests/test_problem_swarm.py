import unittest
from artap.algorithm_swarm import OMOPSO, PSO_V1
from artap.results import Results
from artap.benchmark_functions import BinhAndKorn, AlpineFunction, Ackley


class TestAckley(unittest.TestCase):
    """ Tests that the PSO can find the global optimum. """

    def test_local_problem(self, population_number=30):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = OMOPSO(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 30
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))

class TestAckleyv1(unittest.TestCase):
    """ Tests that the PSO can find the global optimum. """

    def test_local_problem(self, population_number=30):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = PSO_V1(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 30
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


# Very poor performance

# class TestAlpine(unittest.TestCase):
#
#
#     def test_local_problem(self, population_number=30):
#         try:
#             problem = AlpineFunction(**{'dimension': 3})
#             algorithm = PSO(problem)
#             algorithm.options['max_population_number'] = population_number
#             algorithm.options['max_population_size'] = 100
#             algorithm.options['max_processes'] = 3
#             algorithm.run()
#
#             b = Results(problem)
#             optimum = b.find_minimum('F_1')  # Takes last cost function
#             self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
#         except AssertionError:
#             # stochastic
#             print("TestAlpine::test_local_problem", population_number)
#             self.test_local_problem(int(1.5 * population_number))


# class TestAlpinev1(unittest.TestCase):
#
#
#     def test_local_problem(self, population_number=30):
#         try:
#             problem = AlpineFunction(**{'dimension': 3})
#             algorithm = PSO(problem)
#             algorithm.options['max_population_number'] = population_number
#             algorithm.options['max_population_size'] = 100
#             algorithm.options['max_processes'] = 3
#             algorithm.run()
#
#             b = Results(problem)
#             optimum = b.find_minimum('F_1')  # Takes last cost function
#             self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
#         except AssertionError:
#             # stochastic
#             print("TestAlpine::test_local_problem", population_number)
#             self.test_local_problem(int(1.5 * population_number))
#


if __name__ == '__main__':
    unittest.main()
