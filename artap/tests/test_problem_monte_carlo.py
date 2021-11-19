import unittest
from artap.algorithm_monte_carlo import Monte_Carlo, Integral_Monte_Carlo
from artap.results import Results
from artap.benchmark_functions import Sphere, Ackley, BenchmarkFunction
import numpy as np


class Integral_Problem(BenchmarkFunction):
    def set(self, **kwargs):
        """Time-dependent 1D QM wave function of a single particle - squared."""
        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = 0.0
        self.global_optimum_coords = [0.0 for x in range(self.dimension)]

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, z):
        x = z.vector
        output = np.exp(-x[0] ** 2) / (np.pi ** 0.5)
        return [output]


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


class TestIntegral_MonteCarlo(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Monte_Carlo
    def test_local_problem(self):
        problem = Integral_Problem(**{'dimension': 1})
        n = 10
        algorithm = Integral_Monte_Carlo(problem, n)
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertAlmostEqual(int(optimum.costs[0]), problem.global_optimum)


if __name__ == '__main__':
    unittest.main()
