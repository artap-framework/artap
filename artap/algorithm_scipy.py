from artap.problem import Problem
from artap.population import Population
from artap.algorithm import Algorithm

from scipy.optimize import minimize
import numpy as np

class ScipyNelderMead(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name = "Nelder-Mead"):
        super().__init__(problem, name)
        
        self.method = "nelder-mead"
        self.number_of_objectives = len(self.problem.costs)
        self.rel_tol = 1e-8
        self.save_all = True

    def run(self):            
        population = Population(self)
        self.problem.populations.append(population)
        
        initial_vector = self.problem.get_initial_values
        # TODO: parameters (tol=1e-3)
        
        x0 = np.array(initial_vector)        
        minimize(self.problem.evaluate_individual, x0, method="nelder-mead")
