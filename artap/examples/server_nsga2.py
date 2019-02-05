import unittest

# from pygments.lexer import words
# from artap.algorithm_nlopt import opt
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import NSGAII
# from artap.results import Results
from artap.results import GraphicalResults


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
        self.options['max_processes'] = 1

        # self.run_server(daemon=False)

    def evaluate(self, x):
        function = BinhAndKorn()
        return function.eval(x)

    def evaluate_constraints(self, x):
        return BinhAndKorn.constraints(x)


if __name__ == '__main__':
    problem = MyProblem("NSGA2Optimization")
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 20
    algorithm.options['max_population_size'] = 20
    # algorithm.options['calculate_gradients'] = True
    algorithm.run()

    results = GraphicalResults(problem)
    results.plot_scatter('F_1', 'F_2', filename="/tmp/scatter.pdf")
    # results.plot_scatter('x_1', 'x_2')
    # results.plot_individuals('F_1')
