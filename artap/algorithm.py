"""
algorithm.py
===========================================
This is base class for all algorithms
"""

from .problem import Problem
from .utils import ConfigDictionary
from abc import ABCMeta
from .operators import Evaluator, GradientEvaluator, WorstCaseEvaluator

from enum import Enum
from uuid import uuid1


class EvaluatorType(Enum):
    SIMPLE = 0
    GRADIENT = 1
    WORST_CASE = 2


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm", evaluator_type=EvaluatorType.SIMPLE):
        self.uuid = uuid1().hex
        self.name = name
        self.problem = problem
        if evaluator_type == EvaluatorType.SIMPLE or evaluator_type is None:
            self.evaluator = Evaluator(self)
        elif evaluator_type == EvaluatorType.GRADIENT:
            self.evaluator = GradientEvaluator(self)
        elif evaluator_type == EvaluatorType.WORST_CASE:
            self.evaluator = WorstCaseEvaluator(self)

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

        self.individual_features = dict()

    def evaluate(self, individuals):
        # set algorithm id
        for individual in individuals:
            individual.algorithm_id = self.uuid

        self.evaluator.evaluate(individuals)

    def evaluate_scalar(self, individual):
        # set algorithm id
        individual.algorithm_id = self.uuid

        self.evaluator.evaluate_scalar(individual)
        return individual.costs[0]


class DummyAlgorithm(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, name='DummyAlgorithm'):
        super().__init__(problem, name)

    def run(self):
        pass

