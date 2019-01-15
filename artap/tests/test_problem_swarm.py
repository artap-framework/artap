import unittest
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.algorithm_swarm import PSO


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7},
                      'x_2': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-7}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
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
        problem = PSORosenbrock("PSORosenbrock")
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 200
        algorithm.run()
        # results = GraphicalResults(problem)
        # results.plot_populations()


if __name__ == '__main__':
    unittest.main()
