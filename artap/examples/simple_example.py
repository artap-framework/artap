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

H = 1.
W = 1.
L = 1.

class ArtapProblem(Problem):
    """ Defines the optimization problem """
    def __init__(self, name):
        parameters = {'x': {'initial_value': 0.8, 'bounds': [0., W]}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        function = (x[0] ** 2. + H ** 2.) ** 0.5 + ((W - x[0]) ** 2. + L ** 2.) ** 0.5
        return [function]

class SpyderFlyOptimization():
    """ Tests simple one objective optimization problem."""

    def test_local_problem_nsga2(self):

        problem = ArtapProblem("Spyder on the wall")
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 50
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function

        print('Optimal solution:', optimum) # variable x and the optimal value of the calculation
        print('Difference:',optimum.costs[0] -(((W/2.) ** 2. + H ** 2.) ** 0.5 + ((W - (W/2.)) ** 2. + L ** 2.) ** 0.5))

        ### calculate with scipy as well
    def test_local_problem_scipy(self):

        problem2 = ArtapProblem("Spyder on the wall")
        algorithm2 = ScipyOpt(problem2)
        algorithm2.options['algorithm'] = 'Nelder-Mead'
        algorithm2.options['tol'] = 1e-6
        algorithm2.options['calculate_gradients'] = True
        algorithm2.run()

        results2 = Results(problem2)
        opt = results2.find_minimum('F_1')

        for individual in problem2.data_store.individuals:
            print(individual)

        print("scipy optimum:", opt)
        print('Difference:',
              opt.costs[0] - (((W / 2.) ** 2. + H ** 2.) ** 0.5 + ((W - (W / 2.)) ** 2. + L ** 2.) ** 0.5))


if __name__ == "__main__":
   problem = SpyderFlyOptimization()
   problem.test_local_problem_nsga2()
   problem.test_local_problem_scipy()

   problem2 = ArtapProblem("Spyder on the wall")
   x = np.linspace(0.1, 1, 100)
   y = []
   for number in x:
       y.append(problem2.evaluate([number])[0])
   pl.plot(x, y)
   pl.show()
