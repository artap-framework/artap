from artap.problem import Problem
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.results import Results, GraphicalResults

import matplotlib.pyplot as plt


class SpringDesignProblem(Problem):
    """
    Example from K.DEb Multi-objective evolutionary optimization problems, Wiley, 2001.
    pp 435.


    TODO: integer based problem, later


    """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': .5, 'bounds': [0.1, 1.]},
                      'x_2': {'initial_value': .5, 'bounds': [0.0, 5.0]}}

        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        #f1 =
        #f2 =
        return [f1, f2]