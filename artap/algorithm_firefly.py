from numpy.random import random_sample
from .problem import Problem
from .algorithm_swarm import SwarmAlgorithm
from .operators import DummySelector, RandomGenerator, ParetoDominance, crowding_distance, nondominated_truncate, \
    Operator
from math import exp
from random import random
import time


class MoFirefly(SwarmAlgorithm):
    """
    Multi-objective firefly algorithm based on [4].

    The single-objective firefly algorithm is a modification of the original pso algorithms. The idea is that it mimics
    the behaviour of the fireflies, which uses specfic light combinations for hunting and dating. This algorithm mimics
    the dating behaviour of these bugs. The algorithm is originally published by [1]

    The brightest individual attracts the darkest ones, this starts to go to that direction, if there is not an
    existing brighter solutions, the algorithm randomly steps one into another direction.

    This operator makes the following
    ---------------------------------

    - calculates the distance between two points, because its correlates with that value.
    - the brightness of the other point
    - the mutator constant, which contains a damping factor [2]?

    The k+1 th position of the j(th) individual is calculated by the following formula
    ---------------------------------------------------------------------------

        b0=2;               # Attraction Coefficient Base Value
        a=0.2;              # Mutation Coefficient
        ad=0.98;            # Mutation Coefficient Damping Ratio -- decreases the initial value of a after each
                              iteration step
        gamma = 1.          # light absorbtion coefficient

        x(j,k+1) = x(j,k) + b0*exp(-gamma*r^2) + sum_{i<j}[x(j,k) - x(i,k)] + a*(rand[0,1] - 0.5)

    [1] Yang, Xin-She. "Firefly algorithms for multimodal optimization." International symposium on stochastic algorithms.
        Springer, Berlin, Heidelberg, 2009.
    [2] firefly algorithm implementation from www.Yarpiz.com

    [3] https://nl.mathworks.com/matlabcentral/fileexchange/29693-firefly-algorithm

    [4]: Yang, X. S. (2013). Multiobjective firefly algorithm for continuous optimization.
            Engineering with computers, 29(2), 175-184.

     Similarly, alpha should also be linked with scales, the steps should not too large or too small, often steps
     are about 1/10 to 1/100 of the domain size. In addition, alpha should be reduced gradually using
     alpha=alpha_0 delta^t during eteration t.  Typically, delta=0.9 to 0.99 will be a good choice.
    """

    def __init__(self, problem: Problem, name="MOFA Algorithm"):
        super().__init__(problem, name)
        self.options.declare(name='prob_mutation', default=0.1, lower=0,
                             desc='prob_mutation'),
        self.n = self.options['max_population_size']

        self.selector = DummySelector(self.problem.parameters)
        self.dominance = ParetoDominance()

        # set random generator
        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        self.individual_features['front_number'] = 0
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)

        # default parameters
        self.beta = 2.0  # attraction constant
        self.alpha = 0.2  # mutation coefficient --- the original coefficient for the single problem
        self.ad = 0.98  # mutation coefficient -- damping ratio decreases the initial value of a after each
        self.gamma = 1.  # light absorbtion coefficient

        # self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # constants for the speed and the position calculation

    def turbulence(self, particles, current_step=0):
        """ Lévy flight """

        for i in range(len(particles)):
            if i % 6 == 0:
                mutated = self.mutator.mutate(particles[i])
                particles[i].vector = copy(mutated.vector)

    def step(self, current, other):
        """
        If the other firefly is more attractive the current firefly steps one step into the other fireflies direction.
        :return: the new position of the firefly.
        """

        # if it's dominant returns without changing its position
        if self.dominance.compare(current, other) == 1:
            return
        else:
            for i, param in enumerate(self.parameters):
                lb = param['bounds'][0]
                ub = param['bounds'][1]

                # elementary distance of the particle, random walk
                e = random * (ub - lb)
                # distance between the two individuals
                r2 = current.vector[i] ** 2. + other.vector[i] ** 2.
                vel_attraction = self.beta * exp(-self.gamma * r2 ** 2.) * (other.vector[i] - current.vector[i])

                v_rd = self.alpha * (random() - 0.5) * e
                # position i+1
                current.vector[i] += vel_attraction + v_rd
        return

    # def update_position(self, population):
    #
    #     for individual in population:
    #         for parameter, i in zip(self.parameters, range(len(individual.vector))):
    #             individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]
    #
    #             # adjust maximum position if necessary
    #             if individual.vector[i] > parameter['bounds'][1]:
    #                 individual.vector[i] = parameter['bounds'][1]
    #                 individual.features['velocity'][i] *= 0.001
    #
    #             # adjust minimum position if necessary
    #             if individual.vector[i] < parameter['bounds'][0]:
    #                 individual.vector[i] = parameter['bounds'][0]
    #                 individual.features['velocity'][i] *= 0.001

    def update_global_best(self, offsprings):
        """ Manages the leader class in OMOPSO. """

        # the fitness of the particles are calculated by their crowding distance
        crowding_distance(swarm)

        # the length of the leaders archive cannot be longer than the number of the initial population
        self.leaders += swarm
        self.leaders.truncate(self.options['max_population_size'], 'crowding_distance')
        # self.problem.archive += swarm

        return

    def run(self):
        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))
        # initialize the swarm
        self.generator.init(self.options['max_population_size'])
        individuals = self.generator.generate()
        self.evaluate(individuals)
        self.add_features(individuals)

        self.update_global_best(individuals)

        i = 0
        while i < self.options['max_population_number']:
            offsprings = self.selector.select(individuals)

            self.update_velocity(offsprings)
            self.update_position(offsprings)
            self.turbulence(offsprings, i)

            self.evaluate(offsprings)

            self.update_particle_best(offsprings)
            self.update_global_best(offsprings)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))

    # def __init__(self, problem: Problem, name="Particle Swarm Algorithm"):
    #     super().__init__(problem, name)
    #     self.n = self.options['max_population_size']
    #     self.mutator = FireflyStep(self.problem.parameters)
    #     self.selector = DummySelector(self.problem.parameters, self.problem.signs)
    #
    # def run(self):
    #     self.generator = RandomGenerator(self.problem.parameters)
    #     self.generator.init(self.options['max_population_size'])
    #
    #     population = self.gen_initial_population()
    #     self.selector.fast_nondominated_sorting(population.individuals)
    #
    #     t_s = time.time()
    #     self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
    #                                                  self.options['max_population_size']))
    #
    #     nr_gen = 0
    #     non_dominated_sol = []
    #     while nr_gen < self.options['max_population_number']:
    #         offsprings = self.selector.select(population.individuals)
    #         for i, a in enumerate(offsprings):
    #             non_dominated = True
    #             for j, b in enumerate(offsprings):
    #                 if i != j:
    #                     if self.mutator.dominate(a, b):
    #                         # in this case the individual a moves one in the direction b
    #                         # the step size is calculated from the intensity and the attraction
    #                         self.mutator.mutate_ij(a, b)
    #                         non_dominated = False
    #                         # self.evaluate([a]) <- if its not true a new one should be generated, this should be
    #                         #                      managed by the parallelization of the evaluator
    #             if non_dominated:
    #                 non_dominated_sol.append(a) # collects the non-dominated solutions for an iteration
    #
    #         self.evaluate(offsprings)
    #
    #         # to improve the convergence one solution from the pareto front is selected as global best
    #         # generating random weights for the cost function to select the 'global best'
    #         weights = random_sample(len(self.problem.costs))
    #         c = 1. / sum(weights)
    #         weights = [x * c for x in weights]
    #
    #         self.problem.populations[-1] = offsprings
    #
    #         nr_gen += 1
    #
    #     t = time.time() - t_s
    #     self.problem.logger.info("PSO: elapsed time: {} s".format(t))
