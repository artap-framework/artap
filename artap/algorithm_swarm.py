from random import randint, random
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .operators import SwarmStep, DummySelector, RandomGenerator, SwarmStepTVIW, PmMutator
from .archive import Archive
from copy import copy
import time
import math


class SwarmAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Swarm-based Algorithm"):
        super().__init__(problem, name)

    def init_pvelocity(self, population):
        pass

    def init_gbest(self, population):
        pass

    def update_velocity(self, population):
        pass

    def update_gbest(self, population):
        pass

    def update_position(self, population):
        pass

    def turbulence(self, population):
        pass

    def step(self, population):
        self.update_velocity(population)
        self.update_position(population)
        self.turbulence(population)

        offsprings = copy(population)

        self.evaluator.evaluate(offsprings)

        self.update_global_best(offsprings)
        self.update_particle_best(offsprings)

        self.problem.populations.append(offsprings)

        return offsprings

    def run(self):
        pass


class OMOPSO(SwarmAlgorithm):
    """
    Implementation of OMOPSO, a multi-objective particle swarm optimizer (MOPSO).
    OMOPSO uses Crowding distance, Mutation and ε-Dominance.
    According to [3], OMOPSO is one of the top-performing PSO algorithms.

    [1] Margarita Reyes SierraCarlos A. Coello Coello
        Improving PSO-Based Multi-objective Optimization Using Crowding, Mutation and ∈-Dominance
        DOI https://doi.org/10.1007/978-3-540-31880-4_35

    [2] S. Mostaghim ; J. Teich :
        Strategies for finding good local guides in multi-objective particle swarm optimization (MOPSO)
        DOI: 10.1109/SIS.2003.1202243
    [3] Durillo, J. J., J. Garc�a-Nieto, A. J. Nebro, C. A. Coello Coello, F. Luna, and E. Alba (2009).
        Multi-Objective Particle Swarm Optimizers: An Experimental Comparison.
        Evolutionary Multi-Criterion Optimization, pp. 495-509
    """

    def __init__(self, problem: Problem, name="Particle Swarm Algorithm"):
        super().__init__(problem, name)
        self.n = self.options['max_population_size']
        self.mutator = SwarmStep(self.problem.parameters)
        self.selector = DummySelector(self.problem.parameters, self.problem.signs)
        self.features = {'velocity': [],
                         'pbest': None,
                         'max_speed': []}

        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.leaders = Archive()
        # constants for the speed and the position calculation
        self.c1_min = 1.5
        self.c1_max = 2.5
        self.c2_min = 1.5
        self.c2_max = 2.5
        self.r1_min = 0.0
        self.r1_max = 1.0
        self.r2_min = 0.0
        self.r2_max = 1.0
        self.min_weight = 0.1
        self.max_weight = 0.1
        self.change_velocity1 = -1
        self.change_velocity2 = -1

        # in this algorithm a polynomial mutation used as a turbulence operator
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])

    def __constriction_coefficient(self, c1: float, c2: float) -> float:
        rho = c1 + c2
        if rho <= 4:
            result = 1.0
        else:
            result = 2.0 / (2.0 - rho - (rho**2.0 - 4.0 * rho)**0.5)

        return result

    def init_pvelocity(self, population):
        for individual in population:
            individual.features['velocity'] = [0] * len(individual.vector)

    def init_gbest(self, population):
        for individual in population:
            individual.features['pbest'] = copy(individual)

    def turbulence(self, population):
        for individual in population:
            self.mutator.mutate(individual)

    def update_velocity(self, population):

        for individual in population:
            individual.features['velocity'] = [0] * len(individual.vector)
            individual.features['best_vector'] = [0] * len(individual.vector)

            for i in range(0, len(individual.vector)):
                r1 = 0.1 * random()
                r2 = 0.1 * random()

                vel_cognitive = self.c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
                vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
                individual.features['velocity'][i] = self.w * individual.features['velocity'][i] + vel_cognitive + vel_social

    def update_position(self, population):
        for individual in population:
            for parameter, i in zip(self.parameters, range(len(individual.vector))):
                individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]

                # adjust maximum position if necessary
                if individual.vector[i] > parameter['bounds'][1]:
                    individual.vector[i] = parameter['bounds'][1]

                # adjust minimum position if necessary
                if individual.vector[i] < parameter['bounds'][0]:
                    individual.vector[i] = parameter['bounds'][0]

    def run(self):
        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))
        # initialize the swarm
        population = self.gen_initial_population()
        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        self.initialize_pvelocity(population)
        self.initialize_particle_best(population)
        # self.initialize_global_best(population) not correct to calculate always the crowding distance

        i = 0
        while i < self.options['max_population_number']:
            population = self.step(population)

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))

        # self.generator.init(self.options['max_population_size'])
        # population = self.gen_initial_population()
        #
        # self.evaluate(population.individuals)
        # self.add_features(population.individuals)
        #
        # for individual in population.individuals:
        #     self.mutator.evaluate_best_individual(individual)
        #
        # self.selector.fast_nondominated_sorting(population.individuals)
        #
        # t_s = time.time()
        # self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
        #                                              self.options['max_population_size']))
        #
        # i = 0
        # while i < self.options['max_population_number']:
        #     offsprings = self.selector.select(population.individuals)
        #
        #     pareto_front = []
        #     for individual in offsprings:
        #         if individual.features['front_number'] == 1:
        #             pareto_front.append(individual)
        #
        #     for individual in offsprings:
        #         index = randint(0, len(pareto_front) - 1)  # takes random individual from Pareto front
        #         best_individual = pareto_front[index]
        #         if best_individual is not individual:
        #             self.mutator.update(best_individual)
        #             self.mutator.mutate(individual)
        #
        #     population = Population(offsprings)
        #     self.problem.populations.append(population)
        #     self.evaluator.evaluate(offsprings)
        #     self.add_features(offsprings)
        #
        #     for individual in offsprings:
        #         self.mutator.evaluate_best_individual(individual)
        #
        #     self.selector.fast_nondominated_sorting(offsprings)
        #
        #     i += 1
        #


class PSO_V1(SwarmAlgorithm):
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
        self.mutator = SwarmStepTVIW(self.problem.parameters, self.options['max_population_number'])
        self.selector = DummySelector(self.problem.parameters, self.problem.signs)

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

        population = self.gen_initial_population()
        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        for individual in population.individuals:
            self.mutator.evaluate_best_individual(
                individual)  # TODO: all evaluating should be derived from Evaluator class

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
