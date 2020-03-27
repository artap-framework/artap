from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .individual import GeneticIndividual
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, ParetoDominance, EpsilonDominance

import time
import sys

from copy import deepcopy


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.problem = problem

        self.generator = None
        self.selector = None
        self.mutator = None
        self.crossover = None

        # initial population size
        self.population_size = 0

        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        # self.generator.init(10)

    def gen_initial_population(self, is_archive=False):
        individuals = self.generator.generate()

        # create population
        if is_archive:
            population = Population(individuals, individuals)
        else:
            population = Population(individuals)

        # append to population
        self.problem.populations.append(population)

        # set current size
        self.population_size = len(individuals)
        # evaluate individuals
        self.evaluator.evaluate(individuals)

        return population

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.parameters_length = len(self.problem.parameters)

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=10, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')

    def generate(self, parents, archive=None):
        """ generate two children from two different parents """

        # Preserve bounds of Pareto-Front
        children = []
        while len(children) < self.population_size:
            parent1 = self.selector.select(parents)

            if archive is not None:
                parent2 = self.selector.select(archive)
            else:
                parent2 = self.selector.select(parents)

            while parent1 == parent2:
                parent2 = self.selector.select(parents)

            # crossover
            child1, child2 = self.crossover.cross(parent1, parent2)

            # mutation
            child1 = self.mutator.mutate(child1)
            child2 = self.mutator.mutate(child2)
            if not any(child1 == item for item in children):
                children.append(deepcopy(child1))  # Always create new individual
            if not any(child1 == item for item in children):
                children.append(deepcopy(child2))  # Always create new individual

        # parents.extend(removed_parents)
        return children

    def run(self):
        pass


class NSGAII(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation')

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator.init(self.options['max_population_size'])

        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])

        # set mutator
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])

        # set selector
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population and evaluate individuals
        population = self.gen_initial_population()

        # non-dominated sort of individuals
        self.selector.sorting(population.individuals)
        self.selector.crowding_distance(population.individuals)

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'],
                                    self.options['max_population_number'] * self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(population.individuals)
            # evaluate the offsprings
            population = Population(offsprings)
            self.problem.populations.append(population)
            self.evaluate(offsprings)

            # add the parents to the offsprings
            offsprings.extend(deepcopy(population.individuals))

            # non-dominated truncate on the individuals
            self.selector.sorting(offsprings)
            self.selector.crowding_distance(offsprings)

            # sort offsprings and ### remove duplicates by set!!!
            parents = sorted(set(offsprings), key=lambda x: (x.front_number, -x.crowding_distance))

            # truncate and replace individuals
            population.individuals = parents[:self.population_size]

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))


class EpsMOEA(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="EpsMOEA Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation'),
        self.options.declare(name='epsilons', default=0.01, lower=1e-6,
                             desc='prob_epsilons')

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters,
                                         individual_class=GeneticIndividual)  # the same as in the case of NSGA-II
        self.generator.init(self.options['max_population_size'])

        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])

        # Part A: non-dominated sort of individuals
        # -----
        selector_pareto = TournamentSelector(self.problem.parameters)
        self.selector = TournamentSelector(self.problem.parameters)
        # the same as in the case of NSGA - ii
        # this operator is used to generate the new individuals

        # create initial population and evaluate individuals
        population = self.gen_initial_population(True)  # archiving True

        selector_pareto.sorting(population.individuals)
        selector_pareto.crowding_distance(population.individuals)

        # Part B: eps-dominated sort of the individuals with archiving
        # -----
        selector_epsdom = TournamentSelector(self.problem.parameters,
                                             dominance=EpsilonDominance, epsilons=self.options['epsilons'])
        selector_epsdom.sorting(population.archives)
        selector_epsdom.crowding_distance(population.archives)

        t_s = time.time()
        self.problem.logger.info(
            "Eps-MOEA: {}/{}".format(self.options['max_population_number'], self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate and evaluate the next generation
            children = self.generate(population.individuals, population.archives)

            population = Population(children)
            self.problem.populations.append(population)
            self.evaluate(children)

            arch_child = deepcopy(children)
            # PART A
            # non-dominated sorting of the newly generated and the older guys like in NSGA-ii
            # add the parents to the offsprings
            children.extend(deepcopy(population.individuals))

            # non-dominated truncate on the guys
            self.selector.sorting(children)
            selector_pareto.crowding_distance(children)

            parents = sorted(set(children), key=lambda x: (x.front_number, -x.crowding_distance))
            child = parents[:self.population_size]  # truncate

            # eps dominated truncate on the guys
            selector_epsdom.sorting(arch_child)
            selector_epsdom.crowding_distance(arch_child)

            arch_parents = sorted(set(arch_child), key=lambda x: (x.front_number, -x.crowding_distance))
            population.archives = arch_parents[:self.population_size]  # truncate

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))
