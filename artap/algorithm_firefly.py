from numpy.random import random_sample
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneticAlgorithm, GeneticIndividual
from .operators import FireflyMutation, DummySelection, RandomGeneration

import time


class MoFirefly(GeneticAlgorithm):
    """
    Multi-objective firefly algorithm
    """

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = FireflyMutation(self.problem.parameters)
        self.selector = DummySelection(self.problem.parameters, self.problem.signs)

    def run(self):
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator.init(self.options['max_population_size'])

        population = self.gen_initial_population()
        self.selector.sorting(population.individuals)

        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))

        nr_gen = 0
        non_dominated_sol = []
        while nr_gen < self.options['max_population_number']:
            offsprings = self.selector.select(population.individuals)
            for i, a in enumerate(offsprings):
                non_dominated = True
                for j, b in enumerate(offsprings):
                    if i != j:
                        if self.mutator.dominate(a, b):
                            # in this case the individual a moves one in the direction b
                            # the step size is calculated from the intensity and the attraction
                            self.mutator.mutate_ij(a, b)
                            non_dominated = False
                            # self.evaluate([a]) <- if its not true a new one should be generated, this should be
                            #                      managed by the parallelization of the evaluator
                if non_dominated:
                    non_dominated_sol.append(a) # collects the non-dominated solutions for an iteration

            self.evaluate(offsprings)

            # to improve the convergence one solution from the pareto front is selected as global best
            # generating random weights for the cost function to select the 'global best'
            weights = random_sample(len(self.problem.costs))
            c = 1. / sum(weights)
            weights = [x * c for x in weights]

            self.problem.populations[-1] = offsprings

            nr_gen += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))
