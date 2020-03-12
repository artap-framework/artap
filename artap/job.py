from abc import ABCMeta
from enum import Enum
from .individual import Individual


class Job(metaclass=ABCMeta):
    def __init__(self, problem, population=None):
        self.problem = problem
        self.population = population

    def evaluate(self, individual):
        # set in progress
        individual.state = individual.State.IN_PROGRESS

        # check the constraints
        constraints = self.problem.evaluate_constraints(individual)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints
        try:
            costs = self.problem.surrogate.evaluate(individual)
            if isinstance(costs, list):
                individual.costs = costs
            else:
                raise AssertionError("Costs type must be list.")

            # set evaluated
            individual.state = individual.State.EVALUATED

        except (TimeoutError, RuntimeError) as e:
            # individual.vector = VectorAndNumbers.gen_vector(self.problem.parameters)
            individual.state = Individual.State.FAILED

        # add to population
        if self.population is not None:
            self.population.individuals.append(individual)

    def evaluate_scalar(self, x):
        # simple individual
        individual = Individual(x)
        self.evaluate(individual)

        return individual.costs[0]
