import unittest
from artap.problem import Problem
# from artap.datastore import DummyDataStore
from artap.algorithm_swarm import PSO
from artap.benchmark_functions import BinhAndKorn
# from artap.results import GraphicalResults


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5]},
                      'x_2': {'initial_value': 2.5, 'bounds': [0, 3]}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)

    def evaluate(self, x: list):
        function = BinhAndKorn()
        return function.eval(x)


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def xtest_local_problem_pso(self):
        problem = PSORosenbrock("PSORosenbrock")
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 100
        algorithm.run()
        # results = GraphicalResults(problem)
        # results.plot_scatter_vectors('x_1', 'x_2', filename="/tmp/scatter.pdf", population_number=10)
        # results.plot_scatter('F_1', 'F_2', filename="/tmp/scatter.pdf", population_number=None)


if __name__ == '__main__':
    unittest.main()
