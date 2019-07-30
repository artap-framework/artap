"""
Problem:
--------

A spyder, S, sits in one corner of a cuboid room, measuring 'h' by 'w' by 'l', and a fly, F, sits in the opposite
corner. By travelling on the surfaces of the room the, what is the shortest “straight line” distance from S to F?

The problem formulated as a multiobjective, free optimization problem (without constraints)

Problem parameters are the edges of the cuboid: h, w, l

"""
import numpy as np
import pylab as pl

from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.results import Results
from artap.algorithm_scipy import ScipyOpt

class ArtapProblem(Problem):
    """ Defines the optimization problem """
    def __init__(self, name):

        # wall lengths
        self.H = 1.
        self.W = 1.
        self.L = 1.

        parameters = [{'name':'x', 'initial_value': 0.8, 'bounds': [0., self.W]}]
        costs = [{'name':'F_1'}]

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        function = (x[0] ** 2. + self.H ** 2.) ** 0.5 + ((self.W - x[0]) ** 2. + self.L ** 2.) ** 0.5
        return [function]

### Optimization with NSGA-II algorithm

problem = ArtapProblem("Spyder on the wall")
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 100
algorithm.options['max_population_size'] = 50
algorithm.run()

results = Results(problem)
optimum = results.find_minimum('F_1')

print('Optimal solution (NSGA-II):', optimum)

### Optimization with Nelder-Mead

problem_nlm = ArtapProblem("Spyder on the wall")
algorithm_nlm = ScipyOpt(problem_nlm)
algorithm_nlm.options['algorithm'] = 'Nelder-Mead'
algorithm_nlm.options['tol'] = 1e-2
algorithm_nlm.options['calculate_gradients'] = True
algorithm_nlm.run()

results_nlm = Results(problem_nlm)
opt = results_nlm.find_minimum('F_1')

print('Optimal solution (Nelder-Mead):', opt)

# TODO: TEST to check the examples if sg changing