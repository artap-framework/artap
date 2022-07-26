from .algorithm_genetic import GeneticAlgorithm
from .individual import Individual
import time
import random


class SweepAlgorithm(GeneticAlgorithm):
    """
    Sweep Analysis
    """

    def __init__(self, problem, generator, name='SweepAlgorithm'):
        super().__init__(problem, name)
        self.generator = generator

    def run(self):
        t_s = time.time()

        # create initial population
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(Individual(vector))
        # append to problem
        for individual in individuals:
            self.problem.individuals.append(individual)

        # evaluate individuals
        self.evaluate(individuals)

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()
