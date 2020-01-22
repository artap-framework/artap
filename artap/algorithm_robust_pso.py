from random import randint
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneticAlgorithm, GeneticIndividual
from .operators import SwarmMutation, DummySelection, RandomGeneration, SwarmMutationTVIW

import time

global pso_name
global pso_paramaters
global pso_costs
global glob_eval

class SubProblem(Problem):
    """
    Inherits the parameters and the boundaries from the initial main class
    """

    def set(self):
        self.name = pso_name
        self.parameters = pso_paramaters
        self.costs = pso_costs

    def evaluate(self, individual):
        # The individual.vector function contains the problem parameters in the appropriate (previously defined) order

        return glob_eval(individual)


class PSO(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmMutation(self.problem.parameters)
        self.selector = DummySelection(self.problem.parameters, self.problem.signs)

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator.init(self.options['max_population_size'])

        population = self.gen_initial_population()

        for individual in population.individuals:
            self.mutator.evaluate_best_individual(individual)

        self.selector.sorting(population.individuals)
        self.problem.data_store.write_population(population)

        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))

        i = 0
        while i < self.options['max_population_number']:
            offsprings = self.selector.select(population.individuals)

            pareto_front = []
            for individual in offsprings:
                if individual.front_number == 1:
                    pareto_front.append(individual)

            for individual in offsprings:
                index = randint(0, len(pareto_front) - 1)  # takes random individual from Pareto front
                best_individual = pareto_front[index]
                if best_individual is not individual:
                    self.mutator.update(best_individual)
                    self.mutator.mutate(individual)

            self.evaluate(offsprings)

            for individual in offsprings:
                self.mutator.evaluate_best_individual(individual)

            self.selector.sorting(offsprings)
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))

