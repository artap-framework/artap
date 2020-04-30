import time
from copy import deepcopy

from .algorithm import Algorithm
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, EpsilonDominance, nondominated_truncate, crowding_distance
from .population import Population
from .problem import Problem


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
        return population

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.parameters_length = len(self.problem.parameters)

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=100, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')
        self.features = dict()

    def add_features(self, individuals):
        for individual in individuals:
            individual.features = self.features.copy()

    def generate(self, parents, archive=None):
        offsprings = []
        offsprings.extend(parents)
        while len(offsprings) < 2*self.population_size:
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


class NSGAII(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        """
         NSGA-II implementation as described in

         [1] K. Deb, A. Pratap, S. Agarwal and T. Meyarivan, "A fast and elitist
             multiobjective genetic algorithm: NSGA-II," in IEEE Transactions on Evolutionary Computation,
             vol. 6, no. 2, pp. 182-197, Apr 2002. doi: 10.1109/4235.996017
        """
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=1.0, lower=0,
                             desc='prob_cross')

        self.options.declare(name='prob_mutation', default=1.0 / (len(problem.parameters)), lower=0,
                             desc='prob_mutation')

        self.features = {'dominate': set(),
                         'crowding_distance': 0,
                         'domination_counter': 0,
                         'front_number': 0, }

        self.generator = RandomGenerator(self.problem.parameters)
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        self.selector = TournamentSelector(self.problem.parameters)

    def run(self):
        self.generator.init(self.options['max_population_size'])
        # create initial population and evaluate individuals
        population = self.gen_initial_population()
        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        # non-dominated sort of individuals
        self.selector.fast_nondominated_sorting(population.individuals)
        # self.selector.crowding_distance(population.individuals)

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
            self.add_features(offsprings)

            # add the parents to the offsprings
            #offsprings.extend(deepcopy(population.individuals))

            # make the pareto dominance calculation and calculating the crowding distance
            self.selector.fast_nondominated_sorting(offsprings)
            # self.selector.crowding_distance(offsprings)
            population.individuals = nondominated_truncate(offsprings, self.population_size)

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

        self.features = {'dominate': set(),
                         'crowding_distance': 0,
                         'domination_counter': 0,
                         'front_number': 0}

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)  # the same as in the case of NSGA-II
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
        self.evaluate(population.individuals)
        self.add_features(population.individuals)
        selector_pareto.fast_nondominated_sorting(population.individuals)
        # selector_pareto.crowding_distance(population.individuals)

        # Part B: eps-dominated sort of the individuals with archiving
        # -----
        selector_epsdom = TournamentSelector(self.problem.parameters,
                                             dominance=EpsilonDominance, epsilons=self.options['epsilons'])
        selector_epsdom.fast_nondominated_sorting(population.archives)
        # selector_epsdom.crowding_distance(population.archives)

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
            self.add_features(children)

            arch_child = deepcopy(children)
            # PART A
            # non-dominated sorting of the newly generated and the older guys like in NSGA-ii
            # add the parents to the offsprings
            children.extend(deepcopy(population.individuals))

            # non-dominated truncate on the guys
            self.selector.fast_nondominated_sorting(children)
            # selector_pareto.crowding_distance(children)

            parents = sorted(set(children),
                             key=lambda x: (x.features['front_number'], -x.features['crowding_distance']))
            child = parents[:self.population_size]  # truncate

            # eps dominated truncate on the guys
            selector_epsdom.fast_nondominated_sorting(arch_child)
            # selector_epsdom.crowding_distance(arch_child)

            arch_parents = sorted(set(arch_child),
                                  key=lambda x: (x.features['front_number'], -x.features['crowding_distance']))
            population.archives = arch_parents[:self.population_size]  # truncate

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))
