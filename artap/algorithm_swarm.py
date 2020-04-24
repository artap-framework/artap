from random import randint
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneticAlgorithm
from .operators import SwarmMutator, DummySelector, RandomGenerator, SwarmMutatorTVIW

import time


class PSO(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmMutator(self.problem.parameters)
        self.selector = DummySelector(self.problem.parameters, self.problem.signs)
        self.features = {'velocity': [],
                         'best_vector': [],
                         'best_costs': []}

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

        population = self.gen_initial_population()
        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        for individual in population.individuals:
            self.mutator.evaluate_best_individual(individual)

        self.selector.fast_nondominated_sorting(population.individuals)

        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))

        i = 0
        while i < self.options['max_population_number']:
            offsprings = self.selector.select(population.individuals)

            pareto_front = []
            for individual in offsprings:
                if individual.features['front_number'] == 1:
                    pareto_front.append(individual)

            for individual in offsprings:
                index = randint(0, len(pareto_front) - 1)  # takes random individual from Pareto front
                best_individual = pareto_front[index]
                if best_individual is not individual:
                    self.mutator.update(best_individual)
                    self.mutator.mutate(individual)

            population = Population(offsprings)
            self.problem.populations.append(population)
            self.evaluator.evaluate(offsprings)
            self.add_features(offsprings)

            for individual in offsprings:
                self.mutator.evaluate_best_individual(individual)

            self.selector.fast_nondominated_sorting(offsprings)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))


class PSO_V1(GeneticAlgorithm):
    """

    X. Li. A Non-dominated Sorting Particle Swarm Optimizer for Multiobjective
    Optimization. In Genetic and Evolutionary Computation - GECCO 2003, volume
    2723 of LNCS, pages 37–48, 2003.

    This algorithm is a variant of the original PSO, published by Eberhart(2000), the origin of this modified algorithm,
    which constriction factor was introduced by Clercs in 1999.

    The code is based on SHI and EBERHARTS algorithm.

    Empirical study of particle swarm optimization,” in Proc. IEEE Int. Congr. Evolutionary Computation, vol. 3,
    1999, pp. 101–106.
    """

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm - with time varieting inertia weight"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmMutatorTVIW(self.problem.parameters, self.options['max_population_number'])
        self.selector = DummySelector(self.problem.parameters, self.problem.signs)

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

        population = self.gen_initial_population()
        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        for individual in population.individuals:
            self.mutator.evaluate_best_individual(individual)  # TODO: all evaluating should be derived from Evaluator class

        self.selector.fast_nondominated_sorting(population.individuals)
        self.problem.populations.append(population)

        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))

        i = 0
        while i < self.options['max_population_number']:
            offsprings = self.selector.select(population.individuals)

            pareto_front = []
            for individual in offsprings:
                if individual.features['front_number'] == 1:
                    pareto_front.append(individual)

            for individual in offsprings:
                index = randint(0, len(pareto_front) - 1)  # takes random individual from Pareto front
                best_individual = pareto_front[index]
                if best_individual is not individual:
                    self.mutator.update(best_individual)
                    self.mutator.mutate(individual)

            self.evaluate(offsprings)
            self.add_features(offsprings)

            for individual in offsprings:
                self.mutator.evaluate_best_individual(individual)

            self.selector.fast_nondominated_sorting(offsprings)
            population = Population(offsprings)
            self.problem.populations.append(population)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))