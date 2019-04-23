from pygments.lexer import include

from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .operators import RandomGeneration, SimulatedBinaryCrossover,  \
    PmMutation, TournamentSelection, GradientGeneration
import time
import sys

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

    def generate(self, parents):
        """ generate two children from two different parents """

        children = []
        while len(children) < self.population_size:
            parent1 = self.selector.select(parents)
            parent2 = self.selector.select(parents)

            while parent1 == parent2:
                parent2 = self.selector.select(parents)

            # crossover
            child1, child2 = self.crossover.cross(parent1, parent2)

            # mutation
            child1 = self.mutator.mutate(child1)
            child2 = self.mutator.mutate(child2)

            children.append(child1)
            children.append(child2)

        return children.copy()

    def run(self):
        pass


class NSGAII(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

        self.problem.options["save_level"] = "population"

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation')

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

        if self.options['calculate_gradients'] is True:
            self.gradient_generator = GradientGeneration(self.problem.parameters)
            self.gradient_generator.init()

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
        self.selector.non_dominated_sort(population.individuals)
        self.selector.crowding_distance(population.individuals)
        # write to data store

        if self.options['verbose_level'] > 0:
            self.problem.data_store.write_population(population, len(self.problem.data_store.populations))

            if self.options['calculate_gradients'] is True:
                gradient_population = Population(self.gradient_generator.generate(population.individuals))
                gradient_population.individuals = self.evaluate(gradient_population.individuals)
                self.evaluate_gradient(gradient_population.individuals)
                if self.options['verbose_level'] > 0:
                    self.problem.data_store.write_population(gradient_population, len(self.problem.data_store.populations))

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(population.individuals)
            # evaluate the offsprings
            offsprings = self.evaluate(offsprings)

            # if (self.options['calculate_gradients'] is True) and population.number > 20:
            #     population.evaluate_gradients()

            # add the parents to the offsprings
            offsprings.extend(population.individuals)

            # non-dominated truncate on the guys
            self.selector.non_dominated_sort(offsprings)
            self.selector.crowding_distance(offsprings)

            # sort offsprings
            parents = sorted(offsprings, key=lambda x: (x.front_number, -x.crowding_distance))

            # truncate
            offsprings = parents[:self.population_size]

            # write population
            population = Population(offsprings)
            self.problem.data_store.write_population(population, len(self.problem.data_store.populations))

            if self.options['calculate_gradients'] is True:
                gradient_population = Population(self.gradient_generator.generate(population.individuals))
                gradient_population.individuals = self.evaluate(gradient_population.individuals)
                if self.options['verbose_level'] > 0:
                    self.problem.data_store.write_population(gradient_population, len(self.problem.data_store.populations))

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))


class EpsMOEA(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation')

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

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
        self.selector.non_dominated_sort(population.individuals)
        self.selector.crowding_distance(population.individuals)
        # write to data store
        self.problem.data_store.write_population(population)

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(population.individuals)
            # evaluate the offsprings
            offsprings = self.evaluate(offsprings)

            # if (self.options['calculate_gradients'] is True) and population.number > 20:
            #     population.evaluate_gradients()

            # add the parents to the offsprings
            offsprings.extend(population.individuals)

            # non-dominated truncate on the guys
            self.selector.non_dominated_sort(offsprings)
            self.selector.crowding_distance(offsprings)

            # sort offsprings
            parents = sorted(offsprings, key=lambda x: (x.front_number, -x.crowding_distance))

            # truncate
            offsprings = parents[:self.population_size]

            # write population
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))
