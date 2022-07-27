import time
from .individual import Individual
from .operators import RandomGenerator, SimulatedBinaryCrossover, \
    PmMutator, TournamentSelector, EpsilonDominance, nondominated_truncate, crowding_distance
from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm


class IndividualNSGAII(Individual):

    def __init__(self, vector: list):
        super().__init__(vector)
        self.features['dominate'] = []
        self.features['crowding_distance'] = 0
        self.features['domination_counter'] = 0
        self.features['front_number'] = 0
        self.population_id = 0

    @classmethod
    def from_individual(cls, individual: Individual):
        new_individual = cls(individual.vector)
        return new_individual


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

    def run(self):
        if self.generator is None:
            self.generator = RandomGenerator(self.problem.parameters)
            self.generator.init(self.options['max_population_size'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        self.selector = TournamentSelector(self.problem.parameters)

        # create initial population
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            # append to problem
            individuals.append(IndividualNSGAII(vector))
            # add to population

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
            vectors = self.generate(individuals)
            offsprings = []
            for vector in vectors:
                offsprings.append(IndividualNSGAII(vector))
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
