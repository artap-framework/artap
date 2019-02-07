from random import randint
from .problem import Problem
from .population import Population
# from .individual import Individual
from .algorithm_genetic import GeneticAlgorithm
from .operators import SwarmMutation, DummySelection

import time


class PSO(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmMutation(self.problem.parameters)
        self.selector = DummySelection(self.problem.parameters)

    def run(self):
        population = self.gen_initial_population()

        for individual in population.individuals:
            self.mutator.evaluate_pso(individual)

        self.selector.non_dominated_sort(population.individuals)
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
                    self.mutator.update(self.problem.get_bounds(), best_individual)
                    self.mutator.mutate(individual)

            offsprings = self.evaluate(offsprings)

            for individual in offsprings:
                self.mutator.evaluate_pso(individual)

            self.selector.non_dominated_sort(offsprings)
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))
