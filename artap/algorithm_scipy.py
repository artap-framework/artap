from .problem import Problem
from .utils import *
from .algorithm import Algorithm

from scipy.optimize import minimize
import numpy as np

class ScipyNelderMead(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name = "Nelder-Mead"):
        super().__init__(problem, name)
        
        self.method = "nelder-mead"
        self.number_of_objectives = len(self.problem.costs)
        self.rel_tol = 1e-8

    def run(self):    
        initial_vector = self.problem.parameters_values
        # TODO: parameters (tol=1e-3)
        
        x0 = np.array(initial_vector)        
        minimize(self.problem.evaluate_individual, x0, method="nelder-mead")
