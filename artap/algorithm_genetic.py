import time
from copy import deepcopy

from .algorithm import Algorithm
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, EpsilonDominance, nondominated_truncate, crowding_distance
from .problem import Problem
from .archive import Archive


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm", evaluator_type=None):
        super().__init__(problem, name, evaluator_type)

        self.parameters_length = len(self.problem.parameters)

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=100, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')

        self.problem = problem
        self.__only_single_objective = False
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)

    def update_particles(self, individuals, offsprings):
        for individual in individuals:
            individual.features = self.features.copy()

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):
    def __init__(self, problem: Problem, name="General Genetic-based Algorithm", evaluator_type=None):
        super().__init__(problem, name, evaluator_type)

        self.generator = None
        self.selector = None
        self.mutator = None
        self.crossover = None

    def generate(self, parents, archive=None):
        offsprings = []
        # deepcopy of parents
        for offspring in parents:
            offspring_copy = deepcopy(offspring)
            offspring_copy.population_id = -1
            offsprings.append(offspring_copy)

        while len(offsprings) < 2 * self.options['max_population_size']:
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

            # always create new individual
            if not any(child1 == item for item in offsprings) and len(offsprings) < 2 * self.options['max_population_size']:
                child_copy = deepcopy(child1)
                child_copy.population_id = -1
                offsprings.append(child_copy)
            if not any(child2 == item for item in offsprings) and len(offsprings) < 2 * self.options['max_population_size']:
                child_copy = deepcopy(child2)
                child_copy.population_id = -1
                offsprings.append(child_copy)

        return offsprings

    def run(self):
        pass


class NSGAII(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm", evaluator_type=None):
        """
         NSGA-II implementation as described in

         [1] K. Deb, A. Pratap, S. Agarwal and T. Meyarivan, "A fast and elitist
             multiobjective genetic algorithm: NSGA-II," in IEEE Transactions on Evolutionary Computation,
             vol. 6, no. 2, pp. 182-197, Apr 2002. doi: 10.1109/4235.996017
        """
        super().__init__(problem, name, evaluator_type)

        self.options.declare(name='prob_cross', default=1.0, lower=0,
                             desc='prob_cross')

        self.options.declare(name='prob_mutation', default=1.0 / (len(problem.parameters)), lower=0,
                             desc='prob_mutation')

        # set random generator
        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        self.individual_features['front_number'] = 0

    def run(self):
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)
        self.generator.init(self.options['max_population_size'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population
        individuals = self.generator.generate()

        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        # evaluate
        self.evaluate(individuals)

        # non-dominated sort of individuals
        self.selector.fast_nondominated_sorting(individuals)

        # sync to datastore
        for individual in individuals:
            self.problem.data_store.sync_individual(individual)

        t_s = time.time()
        self.problem.logger.info(
            "NSGA_II: {}/{}".format(self.options['max_population_number'],
                                    self.options['max_population_number'] * self.options['max_population_size']))

        # optimization
        for it in range(self.options['max_population_number']):
            # generate new offsprings
            offsprings = self.generate(individuals)

            # evaluate the offsprings
            self.evaluate(offsprings)

            # make the pareto dominance calculation and calculating the crowding distance
            self.selector.fast_nondominated_sorting(offsprings)

            # truncate
            individuals = nondominated_truncate(offsprings, self.options['max_population_size'])

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()


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

    def __init__(self, problem: Problem, name="EpsMOEA Algorithm", evaluator_type=None):
        super().__init__(problem, name, evaluator_type)

        self.options.declare(name='prob_cross', default=0.6, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.2, lower=0,
                             desc='prob_mutation'),
        self.options.declare(name='epsilons', default=0.01, lower=1e-6,
                             desc='prob_epsilons')

        self.archive = None

        # set random generator
        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        self.individual_features['front_number'] = 0

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)
        self.generator.init(self.options['max_population_size'])
        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # one individual is selected from the archive and one from the population to create a new individual
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population
        individuals = self.generator.generate()

        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        # an archive to collect the eps-dominated solutions
        self.archive = Archive(dominance=EpsilonDominance(epsilons=self.options['epsilons']))

        # evaluate individuals
        self.evaluator.evaluate(individuals)

        # archiving the eps-dominating solutions
        for individual in individuals:
            self.archive.add(individual)

        # sync to datastore
        for individual in individuals:
            self.problem.data_store.sync_individual(individual)

        t_s = time.time()
        self.problem.logger.info(
            "Eps-MOEA: {}/{}".format(self.options['max_population_number'], self.options['max_population_size']))

        for it in range(self.options['max_population_number']):
            # generate and evaluate the next generation
            offsprings = self.generate(individuals, archive=self.archive)

            self.evaluator.evaluate(offsprings)

            # pop-acceptance procedure, the dominating offsprings will be preserved in the population and  in the archive
            for individual in offsprings:
                # pareto dominated solutions
                self.selector.pop_acceptance(individuals, individual)
                # archived solutions
                self.archive.add(individual)

                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            # make a new population from the previous population
            # individuals = offsprings

        t = time.time() - t_s
        self.problem.logger.info("Eps-MOEA: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()

