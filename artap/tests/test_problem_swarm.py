import unittest
# from artap.results import GraphicalResults
from artap.problem import Problem
# from artap.benchmark_functions import Binh and Korn
from artap.algorithm_swarm import PSO

import os


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7},
                      'x_2': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7}}
        costs = ['F_1', 'F_2']

        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)
        self.options['max_processes'] = 1

    # def eval(self, x):
    #     function = BinhAndKorn()
    #     return function.eval(x)

    def eval(self, x):
        y = 0
        for i in range(len(x)):
            y += x[i]**2
        return [x[0]**2, x[1]**2]


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_pso(self):
        problem = PSORosenbrock("LocalPythonProblemPSO")
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 200
        algorithm.run()
        # results = GraphicalResults(problem)
        # results.plot_populations()


if __name__ == '__main__':
    unittest.main()
