import unittest

from artap.problem import Problem
from ..algorithm_monte_carlo import Monte_Carlo, Numerical_Integrator, ImportanceSampling, Rejection_Sampling
from ..results import Results
from ..benchmark_functions import Sphere, Ackley, BenchmarkFunction, Schwefel
import numpy as np


class Integral_Problem(Problem):
    def set(self, **kwargs):
        """Time-dependent 1D QM wave function of a single particle - squared."""
        # self.set_dimension(**kwargs)
        # self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)
        self.parameters = [{'name': 'x1', 'bounds': [0, 1], 'parameter_type': 'integer'}]
        self.u_b = 3 * np.pi / 2
        self.l_b = 0
        self.sampling_size = 100
        self.global_optimum = -1.0

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, z):
        x = z.vector
        # output = np.exp(-x[0] ** 2) / (np.pi ** 0.5)
        output = np.sin(x[0])
        return [output]


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
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, places=4)


class TestIntegral_MonteCarlo(unittest.TestCase):
    # unit-test  benchmarck : Sphere, algorithm : Integral_Monte_Carlo
    def test_local_problem(self):
        problem = Integral_Problem(**{'dimension': 1})
        algorithm = Numerical_Integrator(problem)
        algorithm.options['max_population_number'] = 50
        algorithm.options['max_population_size'] = 100
        algorithm.options['max_processes'] = 10
        algorithm.run()

        result = Results(problem)
        optimum = result.find_optimum('f_1')
        self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, places=1)


# class TestImpotance_Sampling(unittest.TestCase):
#     # unit-test  benchmarck : Sphere, algorithm : ImportanceSampling
#     def test_local_problem(self):
#         problem = Integral_Problem(**{'dimension': 1})
#         algorithm = ImportanceSampling(problem)
#         algorithm.options['max_population_number'] = 20
#         algorithm.options['max_population_size'] = 10
#         algorithm.run()
#
#         result = Results(problem)
#         optimum = result.find_optimum('f_1')
#         x = "{:0.1f}".format(optimum.costs[0])
#         self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, places=2)
#
#
# class TestRejection_Sampling(unittest.TestCase):
#     # unit-test  benchmarck : Sphere, algorithm : Rejection_Sampling
#     def test_local_problem(self):
#         problem = Sphere(**{'dimension': 1})
#         algorithm = Rejection_Sampling(problem)
#         algorithm.options['max_population_number'] = 20
#         algorithm.options['max_population_size'] = 10
#         algorithm.run()
#         result = Results(problem)
#         optimum = result.find_optimum('f_1')
#         self.assertAlmostEquals(optimum.costs[0], problem.global_optimum, places=2)


if __name__ == '__main__':
    unittest.main()
