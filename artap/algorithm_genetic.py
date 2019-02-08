from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .operators import RandomGeneration, SimpleCrossover, SimulatedBinaryCrossover, SimpleMutation, \
    PmMutation, TournamentSelection, Selection, ParetoDominance
import time
import sys

EPSILON = sys.float_info.epsilon


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.problem = problem

        self.generator = RandomGeneration(self.problem.parameters)
        self.selector = None
        self.mutator = None
        self.crossover = None

    def gen_initial_population(self):
        pass

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
                             desc='max_population_size')

    def gen_initial_population(self):
        individuals = self.generator.generate(self.options['max_population_size'])
        individuals = self.evaluate(individuals)

        population = Population(individuals)
        return population

    def generate(self, parents):
        """ generate two children from two different parents """

        children = []
        while len(children) < self.options['max_population_size']:
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

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation')

    def run(self):
        # set class
        # self.crossover = SimpleCrossover(self.problem.parameters, self.options['prob_cross'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        # self.mutator = SimpleMutation(self.problem.parameters, self.options['prob_mutation'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])
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
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.options['max_population_size']))

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
            offsprings = parents[:self.options['max_population_size']]

            # write population
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

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
        # set class
        # self.crossover = SimpleCrossover(self.problem.parameters, self.options['prob_cross'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        # self.mutator = SimpleMutation(self.problem.parameters, self.options['prob_mutation'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])
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
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.options['max_population_size']))

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
            offsprings = parents[:self.options['max_population_size']]

            # write population
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))
