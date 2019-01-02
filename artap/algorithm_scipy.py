from artap.problem import Problem
from artap.population import Population
from artap.algorithm import Algorithm

from scipy.optimize import minimize
import numpy as np


_algorithm = ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov']

class ScipyOpt(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name="ScipyOpt"):
        super().__init__(problem, name)

        self.options.declare(name='algorithm', default='Nelder-Mead', values=_algorithm,
                             desc='Algorithm')
        self.options.declare(name='tol', default=1e-6, lower=0.0,
                             desc='tol')

        self.save_all = True

    def run(self):            
        population = Population(self.problem)
        self.problem.populations.append(population)

        # initial vector
        x0 = np.array(self.problem.get_initial_values())

        # optimization
        minimize(self.problem.evaluate_individual, x0, method=self.options['algorithm'], tol=self.options['tol'])
