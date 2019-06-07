from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn
from artap.operators import CustomGeneration
from artap.algorithm_sweep import SweepAlgorithm
from artap.datastore import FileDataStore
import numpy as np


class BinhAndKornProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5]},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3]}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        # function = BinhAndKorn()
        # return function.eval(x)
        return [np.sin(x[0]) + np.sin(x[1]), np.cos(x[1])]

    def evaluate_constraints(self, x):
        return BinhAndKorn.constraints(x)


class NewIndividual:
    def __init__(self, **entries):
        self.__dict__.update(entries)


if __name__ == '__main__':

    problem_gradient = BinhAndKornProblem("SweepProblem")
    database_name = "data_gradient.sol"
    problem_gradient.data_store = FileDataStore(problem_gradient, database_name=database_name)
    gen = CustomGeneration(problem_gradient.parameters)
    individuals = [[0, 1], [1, 0]]
    gen.init(individuals)

    algorithm = SweepAlgorithm(problem_gradient, generator=gen)
    algorithm.options['max_processes'] = 10
    algorithm.options['calculate_gradients'] = True
    algorithm.run()
    print(problem_gradient.data_store.populations[0])
