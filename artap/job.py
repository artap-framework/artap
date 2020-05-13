import time
from abc import ABCMeta
from .individual import Individual
from math import inf


class Job(metaclass=ABCMeta):
    def __init__(self, problem, population=None):
        self.problem = problem
        self.population = population

    def evaluate(self, individual):
        # info
        individual.info["start_time"] = time.time()
        t_s = time.time()

        # set in progress
        individual.state = individual.State.IN_PROGRESS

        # check the constraints
        constraints = self.problem.evaluate_constraints(individual)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem fits the constraints
        try:
            costs = self.problem.surrogate.evaluate(individual)
            individual.costs = costs
            if self.problem is not None:
                individual.calc_signed_costs(self.problem.signs)  # the idea is to make this conversion only once

            # set evaluated
            individual.state = individual.State.EVALUATED

        except (TimeoutError, RuntimeError) as e:
            individual.state = Individual.State.FAILED
            if individual.feasible == 0.0:
                individual.feasible = inf # TODO: genetic algorithms uses this information, i dont know the correct solution

        # add to population
        if self.population is not None:
            self.population.individuals.append(individual)
            individual.info["population"] = self.problem.populations.index(self.population)

        # info
        individual.info["finish_time"] = time.time()
