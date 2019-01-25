from .problem import Problem
from .population import Population
from .algorithm import Algorithm
from .job import Job


from scipy.optimize import minimize
from multiprocessing import Queue
import numpy as np
import time


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
        queue = Queue()
        job = Job(self.problem, queue=queue)

        # initial vector
        x0 = np.array(self.problem.get_initial_values())

        # optimization
        t_s = time.time()
        self.problem.logger.info("ScipyOpt: {}".format(self.options['algorithm']))
        minimize(job.evaluate_scalar, x0, method=self.options['algorithm'], tol=self.options['tol'])
        t = time.time() - t_s
        self.problem.logger.info("ScipyOpt: elapsed time: {} s".format(t))

        individuals = []
        for item in range(queue.qsize()):
            individuals.append(queue.get())

        population = Population()
        population.individuals = individuals
        self.problem.populations.append(population)
        queue.close()
        queue.join_thread()
