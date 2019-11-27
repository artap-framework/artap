from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .individual import GeneticIndividual
from .operators import RandomGeneration, SimulatedBinaryCrossover, \
    PmMutation, TournamentSelection, GradientGeneration, ParetoDominance, EpsilonDominance

import time
import sys

from copy import deepcopy

EPSILON = sys.float_info.epsilon


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.problem = problem

        self.generator = None
        self.selector = None
        self.mutator = None
        self.crossover = None

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

        # TODO: Make new class NSGAII with gradients
        self.gradient_generator = None

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator.init(self.options['max_population_size'])

        if self.options['calculate_gradients'] is True:
            self.gradient_generator = GradientGeneration(self.problem.parameters, individual_class=GeneticIndividual)

        # set crossover
        # self.crossover = SimpleCrossover(self.problem.parameters, self.options['prob_cross'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])

        # set mutator
        # self.mutator = SimpleMutation(self.problem.parameters, self.options['prob_mutation'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])

        # set selector
        self.selector = TournamentSelection(self.problem.parameters)

        # create initial population and evaluate individuals
        population = self.gen_initial_population()
        # non-dominated sort of individuals
        self.selector.sorting(population.individuals)
        self.selector.crowding_distance(population.individuals)

        if self.options['calculate_gradients'] is True:
            self.gradient_generator.init(population.individuals)
            gradient_population = Population(self.gradient_generator.generate())
            self.evaluate(gradient_population.individuals)
            self.evaluate_gradient(population.individuals, gradient_population.individuals)

        # write to data store
        self.problem.data_store.write_population(population)

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.options['max_population_number'] * self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(population.individuals)
            # evaluate the offsprings
            self.evaluate(offsprings)

            # if (self.options['calculate_gradients'] is True) and population.number > 20:
            #     population.evaluate_gradients()

            # add the parents to the offsprings
            offsprings.extend(deepcopy(population.individuals))

            # non-dominated truncate on the guys
            self.selector.sorting(offsprings)
            self.selector.crowding_distance(offsprings)

            # sort offsprings and ### remove duplicates by set!!!
            parents = sorted(set(offsprings), key=lambda x: (x.front_number, -x.crowding_distance))

            # truncate
            offsprings = parents[:self.population_size]

            # write population
            population = Population(offsprings)

            if self.options['calculate_gradients'] is True:
                self.gradient_generator.init(population.individuals)
                gradient_population = Population(self.gradient_generator.generate())
                self.evaluate(gradient_population.individuals)
                self.evaluate_gradient(population.individuals, gradient_population.individuals)

            # write popultation
            self.problem.data_store.write_population(population)

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
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)  # the same as in the case of NSGA-II
        self.generator.init(self.options['max_population_size'])

        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])

        # Part A: non-dominated sort of individuals
        # -----
        selector_pareto = TournamentSelection(self.problem.parameters, self.problem.signs)
        self.selector = TournamentSelection(self.problem.parameters, self.problem.signs)
        # the same as in the case of NSGA - ii
        # this operator is used to generate the new individuals

        # create initial population and evaluate individuals
        population = self.gen_initial_population(True)  # archiving True

        selector_pareto.sorting(population.individuals)
        selector_pareto.crowding_distance(population.individuals)

        # Part B: eps-dominated sort of the individuals with archiving
        # -----
        selector_epsdom = TournamentSelection(self.problem.parameters, self.problem.signs,
                                              dominance=EpsilonDominance, epsilons=self.options['epsilons'])
        selector_epsdom.sorting(population.archives)
        selector_epsdom.crowding_distance(population.archives)

        # write to data store
        self.problem.data_store.write_population(population) # TODO: modify the database connection to handle the archives

        t_s = time.time()
        self.problem.logger.info(
            "Eps-MOEA: {}/{}".format(self.options['max_population_number'], self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate and evaluate the next generation
            child = self.generate(population.individuals, population.archives)
            self.evaluate(child)

            arch_child = deepcopy(child)
            # PART A
            # non-dominated sorting of the newly generated and the older guys like in NSGA-ii
            # add the parents to the offsprings
            child.extend(deepcopy(population.individuals))

            # non-dominated truncate on the guys
            self.selector.sorting(child)
            selector_pareto.crowding_distance(child)

            parents = sorted(set(child), key=lambda x: (x.front_number, -x.crowding_distance))
            child = parents[:self.population_size]  # truncate

            # eps dominated truncate on the guys
            selector_epsdom.sorting(arch_child)
            selector_epsdom.crowding_distance(arch_child)

            arch_parents = sorted(set(arch_child), key=lambda x: (x.front_number, -x.crowding_distance))
            arch_child = arch_parents[:self.population_size]  # truncate

            # write population
            population = Population(child, arch_child)
            # TODO: modify the database connection to handle the archives
            self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))
