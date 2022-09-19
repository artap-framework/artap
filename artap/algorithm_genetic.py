import time
from copy import deepcopy
from .algorithm import Algorithm
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, EpsilonDominance, nondominated_truncate, crowding_distance
from .problem import Problem
from .archive import Archive
from .individual import Individual


class GeneticAlgorithm(Algorithm):
    def __init__(self, problem: Problem, name="General Genetic-based Algorithm", evaluator_type=None):

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
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator = None
        self.selector = None
        self.mutator = None
        self.crossover = None

    def generate(self, parents, archive=None):

        offsprings = []
        while len(offsprings) < self.options['max_population_size']:
            parent1 = self.selector.select(parents)

            if archive:
                if len(archive) <= 1:
                    parent2 = self.selector.select(parents)
                else:
                    parent2 = archive.rand_choice()
            else:
                parent2 = self.selector.select(parents)

            # crossover
            vector_1, vector_2 = self.crossover.cross(parent1.vector, parent2.vector)
            child1 = parent1.__class__(vector_1)
            child2 = parent1.__class__(vector_2)
            # mutation
            child1.vector = self.mutator.mutate(child1.vector, child2.vector)
            child2.vector = self.mutator.mutate(child2.vector, child1.vector)

            # always create new individual
            if len(offsprings) == 0:
                offsprings.append(child1)

            if any(child1 == offspring for offspring in offsprings) and (len(offsprings) < self.options[
                'max_population_size']):
                pass
            else:
                offsprings.append(child1)

            if any(child2 == offspring for offspring in offsprings) and (len(offsprings) < self.options[
                'max_population_size']):
                pass
            elif len(offsprings) < self.options['max_population_size']:
                offsprings.append(child2)

        return offsprings

    def run(self):
        pass


class IndividualEpsMOEA(Individual):

    def __init__(self, vector: list):
        super().__init__(vector)
        self.features['dominate'] = []
        self.features['crowding_distance'] = 0
        self.features['domination_counter'] = 0
        self.features['front_number'] = 0
        self.population_id = 0


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

    def run(self):
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])
        # set crossover
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # one individual is selected from the archive and one from the population to create a new individual
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(IndividualEpsMOEA(vector))

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
