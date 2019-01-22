from .individual import Individual
from .population import Population
from copy import deepcopy
from multiprocessing import Queue
import os


class Job:

    def __init__(self, problem, shared_list=None, queue: Queue = None):
        self.problem = problem
        self.shared_list = shared_list
        self.queue = queue

    def evaluate(self, x, population_id: int = None):
        if self.shared_list is not None:
            for item in self.shared_list:
                if item[0] == os.getpid():
                    individual = deepcopy(item[1])
        else:
            individual = Individual(x, population_id)
        if population_id is None:
            population = Population()
        else:
            population = self.problem.populations[population_id]

        # check the constraints
        constraints = self.problem.evaluate_constraints(individual.vector)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints

        # TODO: find better solution for surrogate
        if self.problem.surrogate:
            costs = self.problem.evaluate_surrogate(individual.vector)
        else:
            # increase counter
            self.problem.eval_counter += 1
            # eval
            costs = self.problem.evaluate(individual.vector)

        individual.costs = costs

        # scipy uses the result number, the genetic algorithms using the property value

        individual.is_evaluated = True
        if self.problem.options['save_level'] == "individual" and self.problem.working_dir:
            self.problem.data_store.write_individual(individual.to_list())

        population.individuals.append(individual)
        self.problem.populations.append(population)

        if self.queue is not None:
            self.queue.put(individual)

        return costs

    # def evaluate_gradient(self):
    #     self.gradient = self.problem.evaluate_gradient(self)
    #     if self.problem.options['max_processes'] > 1:
    #         if Individual.gradients is not None:
    #             Individual.gradients.put([self.number, self.gradient])
    #
    #     return self.gradient

    # def evaluate(self, x, population: Population):
    #     if population is None:
    #         population = Population()
    #     individual = Individual(x, self, population)
    #
    #     # check the constraints
    #     constraints = self.problem.evaluate_constraints(individual.vector)
    #
    #     if constraints:
    #         individual.feasible = sum(map(abs, constraints))
    #
    #     # problem cost function evaluate only in that case when the problem is fits the constraints
    #
    #     # TODO: find better solution for surrogate
    #     if self.problem.surrogate:
    #         costs = self.problem.evaluate_surrogate(individual.vector)
    #     else:
    #         # increase counter
    #         self.problem.eval_counter += 1
    #         # eval
    #         costs = self.problem.evaluate(individual.vector)
    #
    #     individual.costs = costs
    #
    #     # scipy uses the result number, the genetic algorithms using the property value
    #
    #     individual.is_evaluated = True
    #     if self.problem.options['save_level'] == "individual" and self.problem.working_dir:
    #         self.problem.data_store.write_individual(individual.to_list())
    #
    #     if self.problem.options['max_processes'] > 1:
    #         if self.queue is not None:
    #             self.queue.put([individual.id, costs, individual.feasible])
    #
    #     population.individuals.append(individual)
    #     self.problem.populations.append(population)
    #     return costs

    # def evaluate_gradient(self):
    #     self.gradient = self.problem.evaluate_gradient(self)
    #     if self.problem.options['max_processes'] > 1:
    #         if Individual.gradients is not None:
    #             Individual.gradients.put([self.number, self.gradient])
    #
    #     return self.gradient
