import unittest
from artap.algorithm_monte_carlo import Monte_Carlo
from artap.results import Results
from artap.benchmark_functions import Sphere, Ackley


class TestAckley(unittest.TestCase):
    """ Tests that the Monte_Carlo can find the global optimum. """

    def test_local_problem(self, population_number=5):
        try:
            problem = Ackley(**{'dimension': 1})
            n = 10
            algorithm = Monte_Carlo(problem, n)
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            print(optimum.costs[0])
            print(problem.global_optimum)
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


class TestSphere(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Monte_Carlo
    def test_local_problem(self):
        problem = Sphere(**{'dimension': 1})
        n = 10
        algorithm = Monte_Carlo(problem, n)
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum)


if __name__ == '__main__':
    unittest.main()
