import unittest
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.algorithm_swarm import PSO
from artap.benchmark_functions import BinhAndKorn


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7},
                      'x_2': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def evaluate(self, x: list):
        function = BinhAndKorn()
        return function.eval(x)


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def disabled_test_local_problem_pso(self):
        problem = PSORosenbrock("PSORosenbrock")
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 20
        algorithm.options['max_population_size'] = 100
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
