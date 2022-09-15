from random import uniform
from .individual import Individual
from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from .operators import RandomGenerator, PmMutator, ParetoDominance, EpsilonDominance, crowding_distance, \
    NonUniformMutation, UniformMutator, CopySelector, SimulatedBinaryCrossover, TournamentSelector
from .archive import Archive
from copy import copy
import time


class IndividualSwarm(Individual):

    def __init__(self, vector: list = None):
        super().__init__(vector)
        self.features['dominate'] = []
        self.features['crowding_distance'] = 0
        self.features['domination_counter'] = 0
        self.features['front_number'] = -1
        self.features['velocity'] = [0] * len(self.vector)
        self.features['best_cost'] = None
        self.features['best_vector'] = None
        self.population_id = -1

    def copy(self):
        new_individual = self.__class__(self.vector)
        new_individual.features['best_cost'] = self.features['best_cost']
        new_individual.features['best_vector'] = self.features['best_vector']
        return new_individual


class SwarmAlgorithm(GeneticAlgorithm):
    def __init__(self, problem: Problem, name="General Swarm-based Algorithm"):
        super().__init__(problem, name)
        # self.options.declare(name='v_max', default=, lower=0., desc='maximum_allowed_speed')
        self.global_best = None  # swarm algorithms share the information, who is the leader
        self.dominance = ParetoDominance()  # some dominance should be defined for every kind of multi-opbjective swarm
        # constants for the speed and the position calculation
        self.c1_min = 1.5
        self.c1_max = 2.0
        self.c2_min = 1.5
        self.c2_max = 2.0
        self.r1_min = 0.0
        self.r1_max = 1.0
        self.r2_min = 0.0
        self.r2_max = 1.0
        self.min_weight = 0.1
        self.max_weight = 0.5

    def init_pvelocity(self, population):
        pass

    @staticmethod
    def init_pbest(population):
        for individual in population:
            individual.features['best_cost'] = individual.costs_signed
            individual.features['best_vector'] = individual.vector

    @staticmethod
    def khi(c1: float, c2: float) -> float:
        """
        Constriction coefficient [1].
        [1] Ebarhart and Kennedym Empirical study of particle swarm optimization,” in Proc. IEEE Int. Congr.
        Evolutionary Computation, vol. 3, 1999, pp. 101–106.

        :param c1: specific parameter to control the particle best component.
        :param c2: specific parameter to control the global best component.
        :return: float, constriction coefficient
        """
        rho = c1 + c2
        if rho <= 4:
            result = 1.0
        else:
            result = 2.0 / (2.0 - rho - (rho ** 2.0 - 4.0 * rho) ** 0.5)

        return result

    @staticmethod
    def speed_constriction(velocity, u_bound, l_bound) -> float:
        """
        Velocity constriction factor [1].

        .. Ref:
        [1] Nebro, Antonio J., et al. "SMPSO: A new PSO-based metaheuristic for multi-objective optimization."
            2009 IEEE Symposium on Computational Intelligence in Multi-Criteria Decision-Making (MCDM). IEEE, 2009.

        :param velocity: parameter velocity for the i^th component
        :param u_bound: upper bound
        :param l_bound: lower bound
        :return:
        """

        delta_i = (u_bound - l_bound) / 2.
        # user defined max speed
        velocity = min(velocity, delta_i)
        velocity = max(velocity, -delta_i)

        return velocity

    def select_leader(self):
        pass

    def inertia_weight(self):
        pass

    def update_global_best(self, offsprings):
        pass

    def update_velocity(self, individuals):
        for individual in individuals:
            individual.features['velocity'] = [0] * len(individual.vector)
            global_best = self.select_leader()

            r1 = round(uniform(self.r1_min, self.r1_max), 1)
            r2 = round(uniform(self.r2_min, self.r2_max), 1)
            c1 = round(uniform(self.c1_min, self.c1_max), 1)
            c2 = round(uniform(self.c2_min, self.c2_max), 1)

            for i in range(0, len(individual.vector)):
                momentum = self.inertia_weight() * individual.vector[i]
                v_cog = c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
                v_soc = c2 * r2 * (global_best.vector[i] - individual.vector[i])

                v = self.khi(c1, c2) * (momentum + v_cog + v_soc)
                individual.features['velocity'][i] = self.speed_constriction(v, self.parameters[i]['bounds'][1],
                                                                             self.parameters[i]['bounds'][0])

    def update_position(self, population):
        pass

    def update_particle_best(self, population):
        for particle in population:
            flag = self.dominance.compare(particle.costs_signed, particle.features['best_cost'])
            if flag != 2:
                particle.features['best_cost'] = particle.costs_signed
                particle.features['best_vector'] = particle.vector

    def turbulence(self, particles, current_step=0):
        pass

    def run(self):
        pass


class OMOPSO(SwarmAlgorithm):
    """
    Implementation of OMOPSO, a multi-objective particle swarm optimizer (MOPSO).
    OMOPSO uses Crowding distance, Mutation and ε-Dominance.
    According to [3], OMOPSO is one of the top-performing PSO algorithms.

    [1] Margarita Reyes SierraCarlos A. Coello Coello
        Improving PSO-Based Multi-objective Optimization Using Crowding, Mutation and ∈-Dominance
        DOI https://doi.org/10.1007/978-3-540-31880-4_35
    [2] S. Mostaghim ; J. Teich :
        Strategies for finding good local guides in multi-objective particle swarm optimization (MOPSO)
        DOI: 10.1109/SIS.2003.1202243
    [3] Durillo, J. J., J. Garcia-Nieto, A. J. Nebro, C. A. Coello Coello, F. Luna, and E. Alba (2009).
        Multi-Objective Particle Swarm Optimizers: An Experimental Comparison.
        Evolutionary Multi-Criterion Optimization, pp. 495-509
    """

    def __init__(self, problem: Problem, name="OMOPSO"):
        super().__init__(problem, name)
        self.options.declare(name='prob_mutation', default=0.1, lower=0,
                             desc='prob_mutation'),
        self.options.declare(name='epsilons', default=0.01, lower=1e-6,
                             desc='prob_epsilons')
        self.n = self.options['max_population_size']

        self.selector = CopySelector(self.problem.parameters)
        self.dominance = ParetoDominance()

        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.leaders = Archive()
        self.archive = Archive(dominance=EpsilonDominance(epsilons=self.options['epsilons']))

        self.non_uniform_mutator = NonUniformMutation(self.problem.parameters, self.options['prob_mutation'],
                                                      self.options['max_population_number'])
        self.uniform_mutator = UniformMutator(self.problem.parameters, self.options['prob_mutation'],
                                              self.options['max_population_number'])


    def inertia_weight(self):
        return uniform(self.min_weight, self.max_weight)

    def turbulence(self, particles, current_step=0):
        """
        OMOPSO applies a combination of uniform and nonuniform
        mutation to the particle swarm(uniform mutation to the first 30 % of
        the swarm, non-uniform to the next 30 %, and no mutation on the particles)
        """

        for i in range(len(particles)):
            if i % 3 == 0:
                mutated = self.uniform_mutator.mutate(particles[i].vector)
            else:
                mutated = self.non_uniform_mutator.mutate(particles[i].vector, current_step)
            particles[i].vector = mutated.copy()
        return

    def update_position(self, individuals):
        for individual in individuals:
            for parameter, i in zip(self.parameters, range(len(individual.vector))):
                individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]

                # adjust maximum position if necessary
                if individual.vector[i] > parameter['bounds'][1]:
                    individual.vector[i] = parameter['bounds'][1]
                    individual.features['velocity'][i] *= -1

                # adjust minimum position if necessary
                if individual.vector[i] < parameter['bounds'][0]:
                    individual.vector[i] = parameter['bounds'][0]
                    individual.features['velocity'][i] *= -1

    def update_global_best(self, swarm):
        """ Manages the leader class in OMOPSO. """

        # the fitness of the particles are calculated by their crowding distance

        # crowding_distance(swarm)

        self.selector.fast_nondominated_sorting(swarm)
        # the length of the leaders archive cannot be longer than the number of the initial population
        pareto = []
        for particle in swarm:
            if particle.features['front_number'] == 1:
                pareto.append(particle)
        for item in pareto:
            self.leaders.append(item)
        self.leaders.truncate(self.options['max_population_size'], 'crowding_distance')
        self.archive += swarm

        return

    def select_leader(self):
        """
        There are different possibilities to select the global best solution.
        The leader class in this concept contains everybody after the initialization, every individual expected as a
        leader, we select 2 from them and select the non-dominated as the global best.

        :return:
        """

        if self.leaders.size() == 1:
            return self.leaders.rand_choice()

        candidates = self.leaders.rand_sample(2)

        # randomly favourize one of them
        # best_global = choice(candidates)

        # should select those which has bigger fitness
        # # if one of them dominates, it will be selected as global best
        # dom = self.dominance.compare(candidates[0].costs_signed, candidates[1].costs_signed)
        #
        # if dom == 1:
        #     best_global = candidates[0]
        #
        # if dom == 2:
        #     best_global = candidates[1]

        if candidates[1].features['crowding_distance'] > candidates[0].features['crowding_distance']:
            best_global = candidates[1]
        else:
            best_global = candidates[0]
        return best_global

    def run(self):
        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))
        # update mutators
        self.non_uniform_mutator = NonUniformMutation(self.problem.parameters, self.options['prob_mutation'],
                                                      self.options['max_population_number'])
        self.uniform_mutator = UniformMutator(self.problem.parameters, self.options['prob_mutation'],
                                              self.options['max_population_number'])
        # initialize the swarm
        self.generator.init(self.options['max_population_size'])
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(IndividualSwarm(vector))

        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        self.evaluate(individuals)
        self.init_pbest(individuals)
        self.update_global_best(individuals)

        # sync to datastore
        for individual in individuals:
            self.problem.data_store.sync_individual(individual)

        it = 0
        while it < self.options['max_population_number']:
            offsprings = self.selector.select(individuals)

            self.update_velocity(offsprings)
            self.update_position(offsprings)
            self.turbulence(offsprings, it)

            self.evaluate(offsprings)

            self.update_particle_best(offsprings)
            self.update_global_best(offsprings)

            # update individuals
            individuals = offsprings

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            it += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()


class SMPSO(SwarmAlgorithm):
    """
    Implementation of SMPSP, a multi-objective particle swarm optimizer (MOPSO).
    OMOPSO uses Crowding distance, Mutation and ε-Dominance.
    According to [3], SMPSP is one of the top-performing PSO algorithms. There are 3 key-differences between OMOPS§ and
    SMPSO, the mutator is polynomial mutation, the moment component of the velocity is constant, the values of the C1
    and C2 values are [1.5, 2.5], while in the case of OMOPSO they are selected from [1.5, 2.0].
    Here, instead of reversing the values from the borders, their speed are reduced by multiplying it by
    0.001 [3].

    Both of the SMPSO and OMOPSO can be defined with and without epsilon-dominance archive.

    [1] Margarita Reyes SierraCarlos A. Coello Coello
        Improving PSO-Based Multi-objective Optimization Using Crowding, Mutation and ∈-Dominance
        DOI https://doi.org/10.1007/978-3-540-31880-4_35
    [2] S. Mostaghim ; J. Teich :
        Strategies for finding good local guides in multi-objective particle swarm optimization (MOPSO)
        DOI: 10.1109/SIS.2003.1202243
    [3] Durillo, J. J., J. Garcia-Nieto, A. J. Nebro, C. A. Coello Coello, F. Luna, and E. Alba (2009).
        Multi-Objective Particle Swarm Optimizers: An Experimental Comparison.
        Evolutionary Multi-Criterion Optimization, pp. 495-509
    """

    def __init__(self, problem: Problem, name="SMPSO Algorithm"):
        super().__init__(problem, name)
        self.options.declare(name='prob_mutation', default=0.1, lower=0,
                             desc='prob_mutation'),
        self.n = self.options['max_population_size']

        self.individual_features['velocity'] = dict()
        self.individual_features['best_cost'] = dict()
        self.individual_features['best_vector'] = dict()
        # Add front_number feature
        self.individual_features['front_number'] = 0

        self.selector = CopySelector(self.problem.parameters)
        self.dominance = ParetoDominance()
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.leaders = Archive()
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # constants for the speed and the position calculation

        self.c1_min = 1.5
        self.c1_max = 2.5
        self.c2_min = 1.5
        self.c2_max = 2.5
        self.r1_min = 0.0
        self.r1_max = 1.0
        self.r2_min = 0.0
        self.r2_max = 1.0
        self.min_weight = 0.1
        self.max_weight = 0.1

    def inertia_weight(self):
        return uniform(self.min_weight, self.max_weight)

    def init_pvelocity(self, individuals):
        """
        Inits the particle velocity and its allowed maximum speed.
        :param population: list of individuals
        :return
        """
        for individual in individuals:
            # the initial speed is set to zero
            individual.features['velocity'] = [0] * len(individual.vector)

        return

    def turbulence(self, particles, current_step=0):
        """ SMPSO applies polynomial mutation on 15% of the particles """

        for i in range(len(particles)):
            if i % 6 == 0:
                particles[i].vector = self.mutator.mutate(particles[i].vector)

    def update_position(self, individuals):
        for individual in individuals:
            for parameter, i in zip(self.parameters, range(len(individual.vector))):
                individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]

                # adjust maximum position if necessary
                if individual.vector[i] > parameter['bounds'][1]:
                    individual.vector[i] = parameter['bounds'][1]
                    individual.features['velocity'][i] *= 0.001

                # adjust minimum position if necessary
                if individual.vector[i] < parameter['bounds'][0]:
                    individual.vector[i] = parameter['bounds'][0]
                    individual.features['velocity'][i] *= 0.001

    def update_global_best(self, swarm):
        """ Manages the leader class in OMOPSO. """

        # the fitness of the particles are calculated by their crowding distance
        crowding_distance(swarm)

        # the length of the leaders archive cannot be longer than the number of the initial population
        self.leaders += swarm
        self.leaders.truncate(self.options['max_population_size'], 'crowding_distance')
        # self.problem.archive += swarm

        return

    def select_leader(self):
        """
        There are different possibilities to select the global best solution.
        The leader class in this concept contains everybody after the initialization, every individual expected as a
        leader, we select 2 from them and select the non-dominated as the global best.

        :return:
        """

        if self.leaders.size() == 1:
            return self.leaders.rand_choice()

        candidates = self.leaders.rand_sample(2)

        # randomly favourize one of them
        # best_global = choice(candidates)

        # should select those which has bigger fitness
        # # if one of them dominates, it will be selected as global best
        # dom = self.dominance.compare(candidates[0].costs_signed, candidates[1].costs_signed)
        #
        # if dom == 1:
        #     best_global = candidates[0]
        #
        # if dom == 2:
        #     best_global = candidates[1]

        if candidates[1].features['crowding_distance'] > candidates[0].features['crowding_distance']:
            best_global = candidates[1]
        else:
            best_global = candidates[0]
        return best_global

    def run(self):
        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))
        # initialize the swarm
        self.generator.init(self.options['max_population_size'])
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(Individual(vector))

        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        self.evaluate(individuals)

        self.init_pvelocity(individuals)
        self.init_pbest(individuals)
        self.update_global_best(individuals)

        # sync to datastore
        for individual in individuals:
            self.problem.data_store.sync_individual(individual)

        it = 0
        while it < self.options['max_population_number']:
            offsprings = self.selector.select(individuals)

            self.update_velocity(offsprings)
            self.update_position(offsprings)
            self.turbulence(offsprings, it)

            self.evaluate(offsprings)

            self.update_particle_best(offsprings)
            self.update_global_best(offsprings)

            # update individuals
            individuals = offsprings

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            it += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()


class PSOGA(SwarmAlgorithm):
    """
    Implementation a hybrid of PSO-GA
    """

    def __init__(self, problem: Problem, name="PSOGA Algorithm"):
        super().__init__(problem, name)
        self.options.declare(name='prob_cross', default=1.0, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.1, lower=0,
                             desc='prob_mutation'),
        self.n = self.options['max_population_size']

        self.individual_features['velocity'] = None
        self.individual_features['best_cost'] = None
        self.individual_features['best_vector'] = None

        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        # Add front_number feature
        self.individual_features['front_number'] = 0

        self.offspring_selector = CopySelector(self.problem.parameters)
        self.selector = TournamentSelector(self.problem.parameters)
        self.dominance = ParetoDominance()
        # set random generator
        self.generator = RandomGenerator(self.problem.parameters)
        self.leaders = Archive()
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # constants for the speed and the position calculation
        self.c1_min = 1.5
        self.c1_max = 2.5
        self.c2_min = 1.5
        self.c2_max = 2.5
        self.r1_min = 0.0
        self.r1_max = 1.0
        self.r2_min = 0.0
        self.r2_max = 1.0
        self.min_weight = 0.1
        self.max_weight = 0.1
        self.distribution_index = 1
        self.probability = 1

    def inertia_weight(self):
        return uniform(self.min_weight, self.max_weight)

    def init_pvelocity(self, individuals):
        for individual in individuals:
            individual.features['velocity'] = [0] * len(individual.vector)

    def update_velocity(self, individuals):
        """
        update velocity : w * v(i -1) + c1 * r1 * (best_vector - pos(i)) + c2 * r2 * (global_best - pos(i))
        @param individuals:
        @return: update individual.features['velocity']
        """

        for individual in individuals:
            individual.features['velocity'] = [0] * len(individual.vector)
            global_best = self.select_leader()

            r1 = round(uniform(self.r1_min, self.r1_max), 1)
            r2 = round(uniform(self.r1_min, self.r1_max), 1)
            c1 = round(uniform(self.c1_min, self.c1_max), 1)
            c2 = round(uniform(self.c1_min, self.c1_max), 1)

            for i in range(0, len(individual.vector)):
                lb = self.parameters[i]['bounds'][0]
                ub = self.parameters[i]['bounds'][1]
                w = self.khi(c1, c2)
                momentum = w * individual.vector[i]
                v_cog = c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
                v_soc = c2 * r2 * (global_best.vector[i] - individual.vector[i])

                v = momentum + v_cog + v_soc
                individual.features['velocity'][i] = self.speed_constriction(v, ub, lb)

    def select_leader(self):

        if self.leaders.size() == 1:
            return self.leaders.rand_choice()

        candidates = self.leaders.rand_sample(2)

        if candidates[1].features['crowding_distance'] > candidates[0].features['crowding_distance']:
            best_global = candidates[1]
        else:
            best_global = candidates[0]
        return best_global

    def update_position(self, individuals):
        for individual in individuals:
            for parameter, i in zip(self.parameters, range(len(individual.vector))):
                individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]

                if individual.vector[i] > parameter['bounds'][1]:
                    individual.vector[i] = parameter['bounds'][1]
                    individual.features['velocity'][i] *= -1

                if individual.vector[i] < parameter['bounds'][0]:
                    individual.vector[i] = parameter['bounds'][0]
                    individual.features['velocity'][i] *= -1

            # self.makeinteger(individual.vector)

    def update_global_best(self, swarm):
        crowding_distance(swarm)

        self.leaders += swarm
        self.leaders.truncate(self.options['max_population_size'], 'crowding_distance')
        return

    def run(self):
        start = time.time()
        self.problem.logger.info("PSOGA: {}/{}".format(self.options['max_population_number'],
                                                       self.options['max_population_size']))
        # initialization of swarm
        self.generator.init(self.options['max_population_size'])
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(IndividualSwarm(vector))

        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)

            # add to population
            individual.population_id = 0

            self.problem.data_store.sync_individual(individual)

        self.evaluate(individuals)
        self.init_pvelocity(individuals)
        self.init_pbest(individuals)
        self.update_global_best(individuals)

        it = 0
        while it < self.options['max_population_number']:
            offsprings = self.offspring_selector.select(individuals)

            # PSO operators
            self.update_velocity(offsprings)
            self.update_position(offsprings)
            self.evaluate(offsprings)

            # GA operators
            first_selected = self.selector.select(offsprings)
            second_selected = self.selector.select(offsprings)
            vector1, vector2 = self.crossover.cross(first_selected.vector, second_selected.vector)
            vector1 = self.mutator.mutate(vector1)
            vector2 = self.mutator.mutate(vector2)

            # ToDo: Make it clean
            offspring1 = IndividualSwarm(vector1)
            offspring2 = IndividualSwarm(vector2)
            offspring1.features = first_selected.features
            offspring2.features = second_selected.features
            offsprings.append(offspring1)
            offsprings.append(offspring2)

            self.evaluate(offsprings)
            self.update_particle_best(offsprings)
            self.update_global_best(offsprings)

            # update individuals
            individuals = offsprings

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            it += 1
        t = time.time() - start
        self.problem.logger.info("PSOGA: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()
