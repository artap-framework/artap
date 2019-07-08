from abc import ABCMeta, abstractmethod
from .utils import VectorAndNumbers
from .individual import Individual, GeneticIndividual
from .population import Population
from copy import deepcopy
from multiprocessing import Queue
import os

from random import uniform
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
        constraints = self.problem.evaluate_constraints(individual.vector)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints
        individual.costs = self.problem.surrogate.evaluate(individual.vector)
        # self.problem.surrogate.evaluate(individual)

        # add to population
        if self.population is not None:
            self.population.individuals.append(individual)

        # write to datastore
        if self.problem.options["save_level"] == "individual":
            self.problem.data_store.write_individual(individual)

        individual.is_evaluated = True


class JobQueue(Job):
    def __init__(self, problem, shared_list, queue: Queue, population=None):
        super().__init__(problem, population)

        self.shared_list = shared_list
        self.queue = queue

    def evaluate(self, individual):
        # global individual
        for item in self.shared_list:
            if item[0] == os.getpid():
                individual_local = deepcopy(item[1])
        """
        if self.shared_list is not None:
            for item in self.shared_list:
                if item[0] == os.getpid():
                    individual = deepcopy(item[1])
        else:
            individual = Individual(x)
        """
        while not individual_local.is_evaluated:
            # check the constraints
            constraints = self.problem.evaluate_constraints(individual.vector)

            if constraints:
                individual_local.feasible = sum(map(abs, constraints))

            # problem cost function evaluate only in that case when the problem is fits the constraints
            try:
                individual_local.costs = self.problem.surrogate.evaluate(individual.vector)
            except TimeoutError:
                individual_local.vector = VectorAndNumbers.gen_vector(self.problem.parameters)
                continue

            individual_local.is_evaluated = True

        if self.queue is not None:
            self.queue.put(individual_local)

        # add to population
        if self.population is not None:
            self.population.individuals.append(individual)