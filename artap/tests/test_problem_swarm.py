import unittest

from artap.problem import Problem
# from artap.benchmark_functions import Rosenbrock
from artap.algorithm_swarm import PSO


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7},
                      'x_2': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    # def eval(self, x):
    #     function = Rosenbrock()
    #     return function.eval(x)

    def eval(self, x):
        y = 0
        for i in range(len(x)):
            y += x[i]**2
        return y


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_pso(self):
        problem = PSORosenbrock("LocalPythonProblemPSO")
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 30
        algorithm.options['max_population_size'] = 100
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
