import unittest
from artap.algorithm_monte_carlo import Monte_Carlo, Numerical_Integrator, ImportanceSampling, Rejection_Sampling
from artap.results import Results
from artap.benchmark_functions import Sphere, Ackley, BenchmarkFunction, Schwefel
import numpy as np


class Integral_Problem(BenchmarkFunction):
    def set(self, **kwargs):
        """Time-dependent 1D QM wave function of a single particle - squared."""
        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = 0.50
        self.global_optimum_coords = [0.0 for x in range(self.dimension)]

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, z):
        x = z.vector
        output = np.exp(-x[0] ** 2) / (np.pi ** 0.5)
        return [output]


# class TestAckley(unittest.TestCase):
#     """ Tests that the Monte_Carlo can find the global optimum. """
#
#     def test_local_problem(self, population_number=50):
#         try:
#             problem = Ackley(**{'dimension': 1})
#             algorithm = Monte_Carlo(problem)
#             algorithm.options['max_population_number'] = population_number
#             algorithm.options['max_population_size'] = 100
#             algorithm.run()
#
#             b = Results(problem)
#             optimum = b.find_optimum('f_1')  # Takes last cost function
#             print(optimum.costs[0])
#             print(problem.global_optimum)
#             self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
#         except AssertionError:
#             # stochastic
#             print("TestAckleyN222::test_local_problem", population_number)
#             self.test_local_problem(int(1.5 * population_number))


class TestSphere(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Monte_Carlo
    def test_local_problem(self, population_number=50):
        problem = Sphere(**{'dimension': 1})
        algorithm = Monte_Carlo(problem)
        algorithm.options['max_population_number'] = population_number
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertAlmostEqual(int(optimum.costs[0]), problem.global_optimum)


class TestIntegral_MonteCarlo(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Integral_Monte_Carlo
    def test_local_problem(self):
        problem = Integral_Problem(**{'dimension': 1})
        algorithm = Numerical_Integrator(problem)
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        x = "{:0.1f}".format(optimum.costs[0])
        print(x)
        print(problem.global_optimum)
        self.assertAlmostEqual(float(x), problem.global_optimum)


class TestImpotance_Sampling(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : ImportanceSampling
    def test_local_problem(self):
        problem = Integral_Problem(**{'dimension': 1})
        algorithm = ImportanceSampling(problem)
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        x = "{:0.1f}".format(optimum.costs[0])
        print(x)
        print(problem.global_optimum)
        self.assertAlmostEqual(float(x), problem.global_optimum)


class TestRejection_Sampling(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Rejection_Sampling
    def test_local_problem(self):
        problem = Sphere(**{'dimension': 1})
        algorithm = Rejection_Sampling(problem)
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        print(optimum.costs[0])
        print(problem.global_optimum)
        self.assertAlmostEquals(optimum.costs[0], problem.global_optimum)


if __name__ == '__main__':
    unittest.main()
