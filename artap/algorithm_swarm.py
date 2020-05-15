from random import randint
from .problem import Problem
from .population import Population
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .operators import SwarmMutator, DummySelector, RandomGenerator, SwarmMutatorTVIW

import time


class SwarmAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Swarm-based Algorithm"):
        super().__init__(problem, name)

    def iterate(self, parents, archive=None):
        """
        Calculates the speed and the new position of the individuals.
        :param parents:
        :param archive:
        :return:
        """
        offsprings = []
        offsprings.extend(parents)
        while len(offsprings) < 2 * self.population_size:
            parent1 = self.selector.select(parents)

            repeat = True
            while repeat:
                if archive:
                    parent2 = self.selector.select(archive)
                else:
                    parent2 = self.selector.select(parents)

                if parent1 is not parent2:
                    repeat = False

            # crossover
            child1, child2 = self.crossover.cross(parent1, parent2)

            # mutation
            child1 = self.mutator.mutate(child1)
            child2 = self.mutator.mutate(child2)

            if not any(child1 == item for item in offsprings):
                offsprings.append(deepcopy(child1))  # Always create new individual
            if not any(child1 == item for item in offsprings):
                offsprings.append(deepcopy(child2))  # Always create new individual

        # parents.extend(removed_parents)
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
        self.mutator = SwarmMutator(self.problem.parameters)
        self.selector = DummySelector(self.problem.parameters, self.problem.signs)
        self.features = {'velocity': [],
                         'best_position': [],
                         'max_speed': []}

        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)

    def run(self):

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
