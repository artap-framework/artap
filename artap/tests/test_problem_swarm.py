import unittest

from artap.problem import Problem
from artap.benchmark_functions import Rosenbrock
from artap.algorithm_swarm import PSO


class PSO_Rosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock funtion in 2d"""

    def __init__(self, name):
        parameters = {'x': {'initial_value': 5., 'bounds': [0, 5], 'precision': 1e-1},
                      'x': {'initial_value': 5., 'bounds': [0, 5], 'precision': 1e-1}}
        costs = ['F_1']

        working_dir = "./workspace/common_data/"

        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)
        self.max_population_number = 10
        self.max_population_size = 20

    def eval(self, x):
        return Rosenbrock.eval(x)


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_pso(self):
        problem = PSO_Rosenbrock("LocalPythonProblemPSO")
        algorithm = PSO(problem)
        algorithm.run()


if __name__ == '__main__':
    unittest.main()