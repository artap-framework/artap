from scipy.optimize import minimize

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
        es = minimize(cost_function, initial_vector, method=self.method, options={'xatol': self.rel_tol, 'disp': True})
        
    
    