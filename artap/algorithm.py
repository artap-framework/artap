from scipy.optimize import minimize
import numpy as np

class Algorithm:
    """ Base class for optimizaion algorithms. """

    def __init__(self):
        pass

    def run(self):
        pass


class ScipyNelderMead(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self):
        self.name = "Nealder Maed"
        self.method = "nelder-mead"
        self.number_of_objectives = 1
        self.rel_tol = 1e-8

    def run(self, cost_function, initial_vector):        
        x0 = np.array(initial_vector)        
        minimize(cost_function, x0, method="nelder-mead")

        
    
    