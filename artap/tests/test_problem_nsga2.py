import unittest

from ..benchmark_functions import AlpineFunction, Ackley
from ..benchmark_pareto import ZDT1
from ..algorithm_genetic import NSGAII
from ..results import Results
from ..quality_indicator import epsilon_add


class TestNSGA2(unittest.TestCase):
    def test_local_problem(self):
        problem = ZDT1()
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 5
        algorithm.options['max_population_size'] = 3
        algorithm.options['max_processes'] = 1
        algorithm.run()

        populations = problem.populations()

        self.assertEqual(len(populations), algorithm.options['max_population_number'] + 1)
        for individuals in populations.values():
            self.assertEqual(len(individuals), algorithm.options['max_population_size'])


class TestZDT1(unittest.TestCase):
    # integration test -- tests the total functionality of nsga2
    # around 11secs according to literature DOI: 10.1007/978-3-642-01020-0_39
    def test_local_problem(self):
        problem = ZDT1()
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 250
        algorithm.options['max_population_size'] = 100    # according to the literature
        algorithm.options['max_processes'] = 1
        algorithm.run()

        results = Results(problem)
        vals = results.pareto_values()
        exact = problem.pareto_front(vals[0])
        self.assertLessEqual(epsilon_add(exact, vals), 0.2)


class TestAckley(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=50):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('F_1')  # Takes last cost function
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
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAlpine::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
