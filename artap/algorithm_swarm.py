from random import randint
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneticAlgorithm, GeneticIndividual
from .operators import SwarmMutation, DummySelection, RandomGeneration, SwarmMutationTVIW

import time


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


class PSO_V1(GeneticAlgorithm):
    """
    This algorithm is a variant of the original PSO, published by Eberhart(2000), the origin of this modified algorithm,
    which constriction factor was introduced by Clercs in 1999.

    The code is based on SHI and EBERHARTS algorithm.

    Empirical study of particle swarm optimization,” in Proc. IEEE Int. Congr. Evolutionary Computation, vol. 3,
    1999, pp. 101–106.
    """

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm - with time varieting inertia weight"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmMutationTVIW(self.problem.parameters, self.options['max_population_number'])
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