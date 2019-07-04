from artap import individual
from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .individual import Individual
from .operators import RandomGeneration, SimulatedBinaryCrossover,  \
    PmMutation, TournamentSelection, GradientGeneration

from .operators import RandomGeneration, SimulatedBinaryCrossover, \
    PmMutation, TournamentSelection, GradientGeneration, ParetoDominance, EpsilonDominance
from copy import deepcopy
import time
import sys
from random import uniform
from copy import deepcopy

EPSILON = sys.float_info.epsilon


class GeneticIndividual(Individual):
    def __init__(self, vector: list):
        super().__init__(vector)

        self.gradient = []
        self.feasible = 0.0  # the distance from the feasibility region in min norm
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = None  # TODO: make better
        self.crowding_distance = 0  # TODO: deprecated? --
        self.depends_on = None  # For calculating gradients
        self.modified_param = -1
        # For particle swarm optimization
        self.velocity_i = [0] * len(vector)  # particle velocity
        self.best_parameters = []  # best position individual
        self.best_costs = []  # best error individual

        for i in range(0, len(self.vector)):
            self.velocity_i.append(uniform(-1, 1))

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """

        string = "{}, ".format(super().__repr__())

        string += ", front number: {}".format(self.front_number)
        string += ", crowding distance: {}".format(self.crowding_distance)
        string += ", gradient: ["
        for i, number in enumerate(self.gradient):
            string += str(number)
            if i < len(self.vector)-1:
                string += ", "
        string = string[:len(string) - 1]
        string += "]"

        return string

    def sync(self, individual):
        super().sync(individual)

        self.gradient = individual.gradient
        self.feasible = individual.feasible
        self.dominate = individual.dominate
        self.domination_counter = individual.domination_counter
        self.front_number = individual.front_number
        self.crowding_distance = individual.crowding_distance
        self.depends_on = individual.depends_on
        self.modified_param = individual.modified_param
        # For particle swarm optimization
        self.velocity_i = individual.velocity_i
        self.best_parameters = individual.best_parameters
        self.best_costs = individual.best_costs


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

    def generate(self, parents, archive = None):
        """ generate two children from two different parents """

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

        # TODO: Make new class NSGAII with gradients
        self.gradient_generator = None

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator.init(self.options['max_population_size'])

        if self.options['calculate_gradients'] is True:
            self.gradient_generator = GradientGeneration(self.problem.parameters)

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
        # write to data store

        self.problem.data_store.write_population(population)

        if self.options['calculate_gradients'] is True:
            self.gradient_generator.init(population.individuals)
            gradient_population = Population(self.gradient_generator.generate())
            self.evaluate(gradient_population.individuals)
            self.evaluate_gradient(population.individuals, gradient_population.individuals)
            self.problem.data_store.write_population(population)

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'], self.population_size))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(population.individuals)
            # evaluate the offsprings
            self.evaluate(offsprings)

            # if (self.options['calculate_gradients'] is True) and population.number > 20:
            #     population.evaluate_gradients()

            # add the parents to the offsprings
            offsprings.extend(population.individuals)

            # non-dominated truncate on the guys
            self.selector.sorting(offsprings)
            self.selector.crowding_distance(offsprings)

            # sort offsprings
            parents = sorted(offsprings, key=lambda x: (x.front_number, -x.crowding_distance))

            # truncate
            offsprings = parents[:self.population_size]

            # write population
            population = Population(offsprings)
            self.problem.data_store.write_population(population)

            if self.options['calculate_gradients'] is True:
                self.gradient_generator.init(population.individuals)
                gradient_population = Population(self.gradient_generator.generate())
                self.evaluate(gradient_population.individuals)
                self.evaluate_gradient(population.individuals, gradient_population.individuals)
                self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))


class EpsMOEA(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="EpsMOEA Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation')
        self.options.declare(name='epsilons', default=0.01, lower=1e-6,
                             desc='prob_epsilons')

    def run(self):
        # set random generator
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)
        self.generator = RandomGeneration(self.problem.parameters, individual_class=GeneticIndividual)  # the same as in the case of NSGA-II
        self.generator.init(self.options['max_population_size'])

        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])


        # Part A: non-dominated sort of individuals
        # -----
        Selector_Pareto = TournamentSelection(self.problem.parameters)
        self.selector = TournamentSelection(self.problem.parameters)  # the same as in the case of NSGA - ii
        #                                                              # this operator is used to generate the new individuals

        # create initial population and evaluate individuals
        population = self.gen_initial_population(True)  # archiving True

        Selector_Pareto.sorting(population.individuals)
        Selector_Pareto.crowding_distance(population.individuals)

        # Part B: eps-dominated sort of the individuals with archiving
        # -----
        Selector_EpsDom = TournamentSelection(self.problem.parameters, dominance=EpsilonDominance(self.options['epsilons']))
        Selector_EpsDom.sorting(population.archives)
        Selector_EpsDom.crowding_distance(population.archives)

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
            child.extend(population.individuals)

            # non-dominated truncate on the guys
            self.selector.sorting(child)
            Selector_Pareto.crowding_distance(child)

            parents = sorted(child, key=lambda x: (x.front_number, -x.crowding_distance))
            child = parents[:self.population_size] # truncate

            # eps dominated truncate on the guys
            Selector_EpsDom.sorting(arch_child)
            Selector_EpsDom.crowding_distance(arch_child)

            arch_parents = sorted(arch_child, key=lambda x: (x.front_number, -x.crowding_distance))
            arch_child = arch_parents[:self.population_size]  # truncate


            # write population
            population = Population(child, arch_child)
            self.problem.data_store.write_population(population) # TODO: modify the database connection to handle the archives

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))
