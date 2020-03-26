"""
algorithm.py
===========================================
This is base class for all algorithms
"""

from .problem import Problem
from .utils import ConfigDictionary
from abc import ABCMeta
from .operators import Evaluator


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.evaluator = Evaluator(self)
        self.parameters = problem.parameters
        self.options = ConfigDictionary()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')
        self.options.declare(name='calculate_gradients', default=False,
                             desc='Enable calculating of gradients')
        # max(int(2 / 3 * cpu_count(), 1)
        self.options.declare(name='max_processes', default=1,
                             desc='Max running processes')

        self.options.declare(name='n_iterations', default=10,
                             desc='Max number of iterations')

    def evaluate(self, individuals):
        self.evaluator.evaluate(individuals)


class DummyAlgorithm(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, name='DummyAlgorithm'):
        super().__init__(problem, name)

    def run(self):
        pass

