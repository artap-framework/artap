from .problem import Problem
from .algorithm import Algorithm
from .config import artap_root
from .job import JobSimple

import time
import numpy as np

import os

import sys
sys.path.append(artap_root + os.sep + "lib" + os.sep)
import bayesopt

from multiprocessing import Process, Pipe, Queue, Manager
# from multiprocessing.managers import BaseManager

_l_type = ['L_FIXED', 'L_EMPIRICAL', 'L_DISCRETE', 'L_MCMC', 'L_ERROR']
_sc_type = ['SC_MTL', 'SC_ML', 'SC_MAP', 'SC_LOOCV', 'SC_ERROR']
_surr_name = ["sGaussianProcess", "sGaussianProcessML", "sGaussianProcessNormal", "sStudentTProcessJef", "sStudentTProcessNIG"]


# Python module to get run BayesOpt library in a OO pattern.
# The objective module should inherit this one and override evaluateSample.
class BayesOptContinuous(object):

    # Let's define the vector.
    #
    # For different options: see vector.h and vector.cpp .
    # If a parameter is not defined, it will be automatically set
    # to a default value.
    def __init__(self, n_dim):
        ## Library vector
        self.params = {}
        ## n dimensions
        self.n_dim = n_dim
        ## Lower bounds
        self.lb = np.zeros((self.n_dim,))
        ## Upper bounds
        self.ub = np.ones((self.n_dim,))

    @property
    def parameters(self):
        return self.params

    @parameters.setter
    def parameters(self, params):
        self.params = params

    @property
    def lower_bound(self):
        return self.lb

    @lower_bound.setter
    def lower_bound(self, lb):
        self.lb = lb

    @property
    def upper_bound(self):
        return self.ub

    @upper_bound.setter
    def upper_bound(self, ub):
        self.ub = ub

    ## Function for testing.
    # It should be overriden.
    def evaluateSample(self, x_in):
        raise NotImplementedError("Please Implement this method")

    ## Main function. Starts the optimization process.
    def optimize(self):
        min_val, x_out, error = bayesopt.optimize(self.evaluateSample, self.n_dim,
                                                  self.lb, self.ub,
                                                  self.params)

        return min_val, x_out, error


class BayesOpt(Algorithm):
    """ BayesOpt algorithms """

    def __init__(self, problem: Problem, name="BayesOpt"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='l_type', default='L_EMPIRICAL', values=_l_type,
                             desc='Type of learning for the kernel params')
        self.options.declare(name='sc_type', default='SC_MAP', values=_sc_type,
                             desc='Type of learning for the kernel params')
        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum BayesOpt evaluations')
        self.options.declare(name='init_method', default=1,
                             desc='Init method') # 1-LHS, 2-Sobol
        self.options.declare(name='n_init_samples', default=10, lower=1,
                             desc='Number of samples before optimization')
        self.options.declare(name='n_iter_relearn', default=10, lower=1,
                             desc='Number of samples before relearn kernel')
        self.options.declare(name='surr_name', default='sGaussianProcessML', values=_surr_name,
                             desc='Name of the surrogate function')
        self.options.declare(name='surr_noise', default=1e-10, lower=0.0,
                             desc='Variance of observation noise')


class BayesOptClassSerial(BayesOptContinuous):
    def __init__(self, algorithm):
        n = len(algorithm.problem.parameters)
        super().__init__(n)

        # algorithm
        self.algorithm = algorithm

        # Size design variables.
        self.lb = np.empty((n,))
        self.ub = np.empty((n,))
        self.params = {}

        self.job = JobSimple(self.algorithm.problem)

    def evaluateSample(self, x):
        return self.job.evaluate_scalar(x)


class BayesOptSerial(BayesOpt):
    """ BayesOpt algorithms """

    def __init__(self, problem: Problem, name="BayesOpt"):
        super().__init__(problem, name)

        self.bo = BayesOptClassSerial(self)

    def run(self):
        # Figure out bounds vectors.
        i = 0
        for parameter in self.problem.parameters:
            bounds = parameter['bounds']

            self.bo.lb[i] = bounds[0]
            self.bo.ub[i] = bounds[1]

            i += 1

        # set bayesopt
        self.bo.params['n_iterations'] = self.options['n_iterations']
        self.bo.params['n_init_samples'] = self.options['n_init_samples']
        self.bo.params['n_iter_relearn'] = self.options['n_iter_relearn']
        self.bo.params['surr_name'] = self.options['surr_name']
        self.bo.params['surr_noise'] = self.options['surr_noise']
        self.bo.params['init_method'] = self.options['init_method']
        self.bo.params['l_type'] = self.options['l_type']
        self.bo.params['sc_type'] = self.options['sc_type']
        self.bo.params['verbose_level'] = self.options['verbose_level']

        t_s = time.time()
        self.problem.logger.info("BayesOpt: surr_name{}".format(self.options['surr_name']))
        mvalue, x_out, error = self.bo.optimize()
        t = time.time() - t_s
        self.problem.logger.info("BayesOpt: elapsed time: {} s".format(t))

        if error != 0:
            print('Optimization FAILED.')
            print("Error", error)
            print('-' * 35)
        else:
            pass
            # print('Optimization Complete, %f seconds' % (clock() - start))
            # print("Result", x_out, mvalue)
            # print('-' * 35)


class BayesOptClassParallel(Process, BayesOptContinuous):
    def __init__(self, pipe, n, problem: Problem):
        Process.__init__(self)
        BayesOptContinuous.__init__(self, n)

        # output
        self.mvalue = -1.0
        self.x_out = -1.0
        self.error = 0

        self.pipe = pipe
        self.problem = problem

        # Size design variables.
        self.lb = np.empty((n,))
        self.ub = np.empty((n,))
        self.params = {}

    def run(self):
        mvalue, x_out, error = self.optimize()
        self.pipe.send('STOP')

        # set output values
        self.mvalue = mvalue
        self.x_out = x_out
        self.error = error

        # output
        print(self.mvalue)
        print(self.x_out)
        print(self.error)

    def evaluateSample(self, x):
        self.pipe.send(x)
        result = self.pipe.recv()
        return result


def worker(pipe, problem):
    x = None
    while True:
        x = pipe.recv()
        if str(x) == 'STOP':
            break

        job = JobSimple(problem)
        result = job.evaluate_scalar(x)
        pipe.send(result)


class BayesOptParallel(BayesOpt):
    """ BayesOpt algorithms """

    def __init__(self, problem: Problem, name="BayesOpt"):
        super().__init__(problem, name)

        self.pipe_par, self.pipe_child = Pipe()
        self.bo = BayesOptClassParallel(self.pipe_child, len(self.problem.parameters), problem)

    def run(self):
        # Figure out bounds vectors.
        i = 0
        for id in self.problem.parameters:
            bounds = self.problem.parameters[id]['bounds']

            self.bo.lb[i] = bounds[0]
            self.bo.ub[i] = bounds[1]

            i += 1

        # set bayesopt
        self.bo.params['n_iterations'] = self.options['n_iterations']
        self.bo.params['n_init_samples'] = self.options['n_init_samples']
        self.bo.params['n_iter_relearn'] = self.options['n_iter_relearn']
        self.bo.params['surr_name'] = self.options['surr_name']
        self.bo.params['surr_noise'] = self.options['surr_noise']
        self.bo.params['init_method'] = self.options['init_method']
        self.bo.params['l_type'] = self.options['l_type']
        self.bo.params['sc_type'] = self.options['sc_type']
        self.bo.params['verbose_level'] = self.options['verbose_level']

        process = Process(target=worker, args=(self.pipe_par, self.problem))

        self.bo.start()
        process.start()

        self.bo.join()
        process.join()

        print(self.bo.mvalue)
        print(self.bo.x_out)
        print(self.bo.error)

        # self.result = self.mvalue
        """
        if self.bo.error != 0:
            print('Optimization FAILED.')
            print("Error", self.bo.error)
            print('-' * 35)
        else:
            print('Optimization Complete, %f seconds' % (clock() - start))
            print("Result", self.bo.x_out, self.bo.mvalue)
            print('-' * 35)
            
        """