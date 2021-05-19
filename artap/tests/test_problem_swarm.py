import unittest
from ..algorithm_swarm import OMOPSO, SMPSO
from ..results import Results
from ..benchmark_functions import BinhAndKorn, AlpineFunction, Ackley, Rosenbrock
from ..benchmark_pareto import ZDT1
from ..quality_indicator import epsilon_add


class TestAckleyOMOPSO(unittest.TestCase):
    """ Tests that the OMOPSO can find the global optimum. """

    def test_local_problem(self, population_number=50):
        problem = Ackley(**{'dimension': 1})
        algorithm = OMOPSO(problem)
        algorithm.options['max_population_number'] = population_number
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 10
        algorithm.options['epsilons'] = 0.1
        algorithm.run()

        b = Results(problem)
        optimum = b.find_optimum('F_1')  # Takes last cost function
        print(optimum.costs[0], problem.global_optimum)
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)


class TestZDT1OMOPSO(unittest.TestCase):
    # integration test -- tests the total functionality of OMOPSO

    def test_local_problem(self):
        problem = problem = ZDT1()
        algorithm = OMOPSO(problem)
        algorithm.options['max_population_number'] = 500
        algorithm.options['max_population_size'] = 100  # according to the literature
        algorithm.options['max_processes'] = 1
        algorithm.options['epsilons'] = 0.05
        algorithm.run()

        results = Results(problem)
        vals = results.pareto_values(algorithm.archive)
        exact = problem.pareto_front(vals[0])
        self.assertLessEqual(epsilon_add(exact, vals), 0.2)


class TestAckleySMPSO(unittest.TestCase):
    """ Tests that the SMPSO can find the global optimum. """

    def test_local_problem(self, population_number=50):
        problem = Ackley(**{'dimension': 1})
        algorithm = SMPSO(problem)
        algorithm.options['max_population_number'] = population_number
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 10
        algorithm.run()

        b = Results(problem)
        optimum = b.find_optimum('F_1')  # Takes last cost function
        print(optimum.costs[0], problem.global_optimum)
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)


class TestZDT1SMPSP(unittest.TestCase):
    # integration test -- tests the total functionality of SMPSO

    def test_local_problem(self):
        problem = problem = ZDT1()
        algorithm = OMOPSO(problem)
        algorithm.options['max_population_number'] = 500
        algorithm.options['max_population_size'] = 100  # according to the literature
        algorithm.options['max_processes'] = 1
        algorithm.run()

        results = Results(problem)
        vals = results.pareto_values()
        exact = problem.pareto_front(vals[0])
        self.assertLessEqual(epsilon_add(exact, vals), 0.2)


class TestRosenbrockSMPSO(unittest.TestCase):
    # unit-test  benchmarck : Rosenbrock, algorithm : SMPSO
    def test_local_problem(self):
        problem = Rosenbrock(**{'dimension': 1})
        algorithm = SMPSO(problem)
        algorithm.options['max_population_number'] = 200
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 10
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertEqual(optimum.costs[0], problem.global_optimum)


class TestRosenbrockOMOPSO(unittest.TestCase):
    # unit-test   benchmark : Rosenbrock, algorithm: OMOPSO
    def test_local_problem(self):
        problem = Rosenbrock(**{'dimension': 1})
        algorithm = OMOPSO(problem)
        algorithm.options['max_population_number'] = 200
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 1
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertEqual(optimum.costs[0], problem.global_optimum)


class TestAlpineFunctionSMPSO(unittest.TestCase):
    # unit-test   benchmark : AlpineFunction, algorithm : SMPSO
    def test_local_problem(self):
        problem = AlpineFunction(**{'dimension': 1})
        algorithm = SMPSO(problem)
        algorithm.options['max_population_number'] = 200
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 1
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        # print(optimum)
        self.assertEqual(optimum.costs[0], 0.0)


class TestAlpineFunctionOMOPSO(unittest.TestCase):
    # unit-test   benchmark : AlpineFunction, algorithm : OMOPSO
    def test_local_problem(self):
        problem = AlpineFunction(**{'dimension': 1})
        algorithm = OMOPSO(problem)
        algorithm.options['max_population_number'] = 200
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 1
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        self.assertEqual(optimum.costs[0], 0.0)


if __name__ == '__main__':
    unittest.main()
