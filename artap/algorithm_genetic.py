import time
from copy import deepcopy

from .algorithm import Algorithm
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, EpsilonDominance, nondominated_truncate, crowding_distance
from .population import Population
from .problem import Problem
from .archive import Archive


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

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

        self.problem = problem

        self.generator = None
        self.selector = None
        self.mutator = None
        self.crossover = None

        # initial population size
        self.population_size = 0

        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)

    def add_features(self, individuals):
        for individual in individuals:
            individual.features = self.features.copy()

    def gen_initial_population(self):
        individuals = self.generator.generate()
        population = Population(individuals)

        # append to population
        self.problem.populations.append(population)

        # set current size
        self.population_size = len(individuals)
        return population

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Genetic-based Algorithm"):
        super().__init__(problem, name)

    def generate(self, parents, archive=None):
        offsprings = []
        offsprings.extend(parents)
        while len(offsprings) < 2 * self.population_size:
            parent1 = self.selector.select(parents)

            repeat = True
            while repeat:
                if archive:
                    if len(archive) <= 1:
                        parent2 = self.selector.select(parents)
                    else:
                        parent2 = archive.rand_choice()
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

            # make the pareto dominance calculation and calculating the crowding distance
            self.selector.fast_nondominated_sorting(offsprings)
            population.individuals = nondominated_truncate(offsprings, self.population_size)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))


class EpsMOEA(GeneticAlgorithm):
    """
    EpsMOEA is proposed by Deb et al[1] which is a efficient algorithm with less computer time because it does not
    contain a sort process for non-dominate set. The searching space are divided into several hyper-boxes under
    box dominance concept, when two solutions in same box, only one solution can survive in the hyperbox, EpsMOEA choose
    the solution nearer to the hyperbox corner.

    .. Ref::

    [1] K. Deb, M. Mohan, S. Mishra, Evaluating the epsilon-domination based multiobjective evolutionary algorithm for
        a quick computation of Pareto-optimal solutions, Evolutionary Computation 13(4) (2005) 501 - 525.
    [2] Siwei Jiang, Zhihua Cai: Enhance the Convergence and Diversity for eps-MOPSO by Uniform Design and
                                 Minimum Reduce Hypervolume
    """

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
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])

        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])

        # one individual is selected from the archive and one from the population to create a new individual
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population and evaluate individuals
        population = self.gen_initial_population()

        # an archive to collect the eps-dominated solutions
        self.problem.archive = Archive(dominance=EpsilonDominance(epsilons=self.options['epsilons']))

        self.evaluate(population.individuals)
        self.add_features(population.individuals)

        # archiving the eps-dominating solutions
        for individual in population.individuals:
            self.problem.archive.add(individual)

        t_s = time.time()
        self.problem.logger.info(
            "Eps-MOEA: {}/{}".format(self.options['max_population_number'], self.population_size))

        for it in range(self.options['max_population_number']):
            # generate and evaluate the next generation
            offspring = self.generate(population.individuals, archive=self.problem.archive)

            self.evaluate(offspring)
            self.add_features(offspring)

            # pop-acceptance procedure, the dominating offsprings will be preserved in the population and  in the
            # archive
            population = Population(population.individuals)  # make a new population from the previous population
            self.problem.populations.append(population)
            for individual in offspring:
                self.selector.pop_acceptance(population.individuals, individual)    # pareto dominated solutions
                self.problem.archive.add(individual)                                # archived solutions

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))
