from .problem import Problem
from .algorithm import Algorithm

from scipy.optimize import minimize
import numpy as np
import time


_algorithm = ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'dogleg', 'trust-ncg', 'trust-exact', 'trust-krylov']


class ScipyOpt(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name="ScipyOpt", evaluator_type=None):
        super().__init__(problem, name, evaluator_type)

        self.options.declare(name='algorithm', default='Nelder-Mead', values=_algorithm,
                             desc='Algorithm')
        self.options.declare(name='tol', default=1e-6, lower=0.0,
                             desc='tol')
        self.options.declare(name='bounds', default=None, desc='bounds')

        self.save_all = True

    def run(self):
        # initial vector
        x0 = self.problem.get_initial_values()

        # optimization
        t_s = time.time()

        self.problem.logger.info("ScipyOpt: {}".format(self.options['algorithm']))
        minimize(self.evaluator.evaluate_scalar, x0, method=self.options['algorithm'], tol=self.options['tol'],
                 bounds=self.options['bounds'], options={'maxiter': self.options['n_iterations']})

        t = time.time() - t_s
        self.problem.logger.info("ScipyOpt: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()
