from abc import ABCMeta, abstractmethod
from .utils import VectorAndNumbers
from .individual import Individual
from multiprocessing import Queue
import os

from copy import deepcopy


class Job(metaclass=ABCMeta):
    def __init__(self, problem, population):
        self.problem = problem
        self.population = population

    @abstractmethod
    def evaluate(self, x):
        pass

    def evaluate_scalar(self, x):
        # simple individual
        individual = Individual(x)
        self.evaluate(individual)

        return individual.costs[0]


class JobSimple(Job):
    def __init__(self, problem, population=None):
        super().__init__(problem, population)

    def evaluate(self, individual):
        # check the constraints
        constraints = self.problem.evaluate_constraints(individual)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints
        try:
            individual.costs = self.problem.surrogate.evaluate(individual)
            # self.problem.surrogate.evaluate(individual)

            individual.state = individual.State.EVALUATED

        except (TimeoutError, RuntimeError) as e:
            # individual.vector = VectorAndNumbers.gen_vector(self.problem.parameters)
            individual.state = Individual.State.FAILED

        # add to population
        if self.population is not None:
            self.population.individuals.append(individual)

        # write to datastore
        if self.problem.options["save_level"] == "individual":
            self.problem.data_store.write_individual(individual)

