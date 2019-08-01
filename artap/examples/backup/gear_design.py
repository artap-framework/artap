from artap.problem import Problem
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.results import Results, GraphicalResults

import matplotlib.pyplot as plt


class GearDesignProblem(Problem):
    """
    Example from K.DEb Multi-objective evolutionary optimization problems, Wiley, 2001.
    pp 434.

    The objective of the task is to finc the optimal turn numbers of a gearbox gear's.
    The gearbox contains for gears, the required gear ratio is 1/6.931

    The first goal function's role is to minimize the  error between the obtained and
    the realized gear ratio:

    Minimize f1 = (1./6.931 - x1*x2/(x3*x4))**2.

    where x is the solution vector, contains the number of the teeths, these numbers
    are strictly integers

    Minimize f2 = max(x1, x2, x3, x4)

    subject to
            x1 e [12, 60] strictly integer
            x2 e [12, 60] strictly integer
            x3 e [12, 60] strictly integer
            x4 e [12, 60] strictly integer

    TODO: integer programming

    """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': .5, 'bounds': [0.1, 1.]},
                      'x_2': {'initial_value': .5, 'bounds': [0.0, 5.0]}}

        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        f1 =
        f2 =
        return [f1, f2]