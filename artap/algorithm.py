from .problem import Problem

from scipy.optimize import minimize
import numpy as np

class Algorithm:
    """ Base class for optimizaion algorithms. """

    def __init__(self, problem, name = "Algorithm"):
        self.name = name
        self.problem = problem

    def run(self):
        pass


class ScipyNelderMead(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name = "Nelder-Mead"):
        super().__init__(problem, name)
        
        self.method = "nelder-mead"
        self.number_of_objectives = 1
        self.rel_tol = 1e-8

    def run(self):    
        initial_vector = list(self.problem.parameters.values())

        x0 = np.array(initial_vector)        
        minimize(self.problem.evaluate_individual, x0, method="nelder-mead")

        
    
    