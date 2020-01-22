from abc import abstractmethod, ABC
import sys
import random
import math
import itertools
import numpy as np
from math import exp
from .individual import Individual
from .utils import VectorAndNumbers
from .doe import build_box_behnken, build_lhs, build_full_fact, build_plackett_burman
from copy import copy

EPSILON = sys.float_info.epsilon


class Operation(ABC):

    def __init__(self):
        pass

    @staticmethod
    def clip(value, min_value, max_value):
        return max(min_value, min(value, max_value))


class Generation(Operation):

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__()
        self.parameters = parameters
        self.individual_class = individual_class

    def create_individual(self, vector: list = []):
        return self.individual_class(vector)

    @abstractmethod
    def generate(self):
        pass


class CustomGeneration(Generation):

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)
        self.vectors = []

    def init(self, vectors):
        self.vectors = vectors

    def generate(self):
        individuals = []
        for vector in self.vectors:
            individuals.append(self.create_individual(vector))
        return individuals


class RandomGeneration(Generation):

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)
        self.number = 0

    def init(self, number):
        self.number = number

    def generate(self):
        individuals = []
        for i in range(self.number):
            vector = VectorAndNumbers.gen_vector(self.parameters)
            individuals.append(self.create_individual(vector))
        return individuals


class FullFactorGeneration(Generation):
    """
    Create a general full-factorial design
    Number of experiments (2 ** len(parameters) - without center, 3 ** len(parameters - with center)
    """

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)
        self.center = False

    def init(self, center):
        self.center = center

    def generate(self):
        dict_vars = {}
        for parameter in self.parameters:
            name = parameter['name']
            l_b = parameter['bounds'][0]
            u_b = parameter['bounds'][1]

            if self.center:
                dict_vars[name] = [l_b, (l_b + u_b) / 2.0, u_b]
            else:
                dict_vars[name] = [l_b, u_b]

        df = build_full_fact(dict_vars)

        individuals = []
        for vector in df:
            individuals.append(self.create_individual(vector))
        return individuals


class PlackettBurmanGeneration(Generation):
    """
    Create a general full-factorial design
    Number of experiments (2 ** len(parameters) - without center, 3 ** len(parameters - with center)
    """

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)

    def generate(self):
        dict_vars = {}
        for parameter in self.parameters:
            name = parameter['name']
            l_b = parameter['bounds'][0]
            u_b = parameter['bounds'][1]
            dict_vars[name] = [l_b, u_b]

        df = build_plackett_burman(dict_vars)
        # print(df)

        individuals = []
        for vector in df:
            individuals.append(self.create_individual(vector))
        return individuals


class BoxBehnkenGeneration(Generation):
    """
    Create a general full-factorial design
    # 3 params = 13 experiments
    # 4 params = 25 experiments
    # 5 params = 41 experiments
    # 6 params = 49 experiments
    # 7 params = 57 experiments
    # 8 params = 113 experiments
    https://en.wikipedia.org/wiki/Box%E2%80%93Behnken_design
    """

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class, )

    def generate(self):
        dict_vars = {}
        for parameter in self.parameters:
            name = parameter['name']
            l_b = parameter['bounds'][0]
            u_b = parameter['bounds'][1]
            dict_vars[name] = [l_b, u_b]

        df = build_box_behnken(dict_vars)
        # print(df)

        individuals = []
        for vector in df:
            individuals.append(self.create_individual(vector))
        return individuals


class LHSGeneration(Generation):
    """
    Builds a Latin Hypercube design dataframe from a dictionary of factor/level ranges.
    """

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)
        self.number = 0

    def init(self, number):
        self.number = number

    def generate(self):
        dict_vars = {}
        for parameter in self.parameters:
            name = parameter["name"]
            l_b = parameter['bounds'][0]
            u_b = parameter['bounds'][1]
            dict_vars[name] = [l_b, u_b]

        df = build_lhs(dict_vars, num_samples=self.number)
        # print(df)

        individuals = []
        for vector in df:
            individuals.append(self.create_individual(vector))
        return individuals


class GradientGeneration(Generation):

    def __init__(self, parameters=None, individual_class=Individual):
        super().__init__(parameters, individual_class)
        self.delta = 1e-6
        self.individuals = None

    def init(self, individuals):
        self.individuals = individuals

    def generate(self):
        new_individuals = []
        k = 0
        for individual in self.individuals:
            for i in range(len(individual.vector)):
                vector = individual.vector.copy()
                vector[i] -= self.delta
                new_individuals.append(self.create_individual(vector))
                new_individuals[-1].depends_on = k
                new_individuals[-1].modified_param = i
            k += 1
        return new_individuals


class Mutation(Operation):

    def __init__(self, parameters, probability):
        super().__init__()
        self.parameters = parameters
        self.probability = probability

    @abstractmethod
    def mutate(self, p):
        pass


class SimpleMutation(Mutation):
    def __init__(self, parameters, probability):
        super().__init__(parameters, probability)

    def mutate(self, p):
        """ uniform random mutation """
        mutation_space = 0.1
        vector = []

        for i, parameter in enumerate(self.parameters):
            if random.uniform(0, 1) < self.probability:
                l_b = parameter['bounds'][0]
                u_b = parameter['bounds'][1]

                para_range = mutation_space * (u_b - l_b)
                mutation = random.uniform(-para_range, para_range)
                # vector.append(self.clip(p.vector[i] + mutation, l_b, u_b))
                vector.append(p.vector[i] + mutation)
            else:
                vector.append(p.vector[i])

        p_new = p.__class__(vector)
        return p_new


class PmMutation(Mutation):
    """
    PmMutation -- for nsga2 and epsMoEA

    This operator can handle real, integer and boolean optimization parameters.
    The class contains two-kind of operators as the original (Deb's [...]) implementation .

    This is a difference between Artap and Platypus, where the Integer numbers are encoded (Gray-encoding) and handled
    as binary numbers with the Bitflip operator.
    """

    def __init__(self, parameters, probability, distribution_index=20):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index

    def mutate(self, parent):
        vector = []

        for i, parameter in enumerate(self.parameters):
            if isinstance(parent.vector[i], list):
                vector.append(self.bitflip(parent.vector[i]))

            else:
                if random.uniform(0, 1) < self.probability:
                    l_b = parameter['bounds'][0]
                    u_b = parameter['bounds'][1]

                    if isinstance(parent.vector[i], float):
                        vector.append(self.pm_mutation(parent.vector[i], l_b, u_b))

                    if isinstance(parent.vector[i], int):
                        vector.append(int(self.pm_mutation(parent.vector[i], l_b, u_b)))
                else:
                    vector.append(parent.vector[i])

        p_new = parent.__class__(vector)
        return p_new

    def pm_mutation(self, x, lb, ub):
        """
        Polynomial mutation for float and integer parameters.

        :param x: represents one parameter of the problem
        :param lb: lower bound
        :param ub: upper bound
        :return:
        """
        u = random.uniform(0, 1)
        dx = ub - lb

        if u < 0.5:
            bl = (x - lb) / dx
            b = 2.0 * u + (1.0 - 2.0 * u) * pow(1.0 - bl, self.distribution_index + 1.0)
            delta = pow(b, 1.0 / (self.distribution_index + 1.0)) - 1.0
        else:
            bu = (ub - x) / dx
            b = 2.0 * (1.0 - u) + 2.0 * (u - 0.5) * pow(1.0 - bu, self.distribution_index + 1.0)
            delta = 1.0 - pow(b, 1.0 / (self.distribution_index + 1.0))

        x = x + delta * dx
        x = self.clip(x, lb, ub)

        return x

    def bitflip(self, x: list):

        for j in range(1, len(x)):
            if random.uniform(0.0, 1.0) <= self.probability:
                x[j] = not x[j]

        return x


class SwarmMutation(Mutation):
    """
    This swarm mutator operator is made for the original PSO algorithm, which defined by Kennedy and Eberhart in 1995

    PSO shares many similarities with evolutionary computation. Both algorithms start with a group of a randomly
    generated population. Both update the population iteratively and search for the optimum with stochastic techniques.
    The main difference between them is in the information sharing mechanism. In EA, only the individuals of current
    generation share information with each other, and any individual has a chance to give out information to others.
    In PSO, actually not the current individuals share information with each other, but the individuals of previous
    generation (the optimal particles) give out information to the current ones. In other words, the information sharing
    is one-way in PSO.
    """

    def __init__(self, parameters, probability=1):
        super().__init__(parameters, probability)
        self.w = 0.1  # constant inertia weight (how much to weigh the previous velocity)
        self.c1 = 2.  # cognitive constant
        self.c2 = 1.  # social constant
        self.best_individual = None

    def evaluate_best_individual(self, individual):
        """ Determines the best individual in the swarm """
        dominates = True

        for i in range(len(individual.best_costs)):
            if individual.costs[i] > individual.best_costs[i]:
                dominates = False

        # check to see if the current position is an individual best
        if dominates:
            individual.best_vector = individual.vector
            individual.best_costs = individual.costs

    # update new particle velocity
    def update_velocity(self, individual):

        for i in range(0, len(individual.vector)):
            r1 = 0.1 * random.random()
            r2 = 0.1 * random.random()

            vel_cognitive = self.c1 * r1 * (individual.best_vector[i] - individual.vector[i])
            vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
            individual.velocity_i[i] = self.w * individual.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, individual):

        for parameter, i in zip(self.parameters, range(len(individual.vector))):
            individual.vector[i] = individual.vector[i] + individual.velocity_i[i]

            # adjust maximum position if necessary
            if individual.vector[i] > parameter['bounds'][1]:
                individual.vector[i] = parameter['bounds'][1]

            # adjust minimum position if necessary
            if individual.vector[i] < parameter['bounds'][0]:
                individual.vector[i] = parameter['bounds'][0]

    def update(self, best_individual):
        self.best_individual = best_individual

    def mutate(self, p):
        self.update_velocity(p)
        self.update_position(p)
        return p


class SwarmMutationTVIW(SwarmMutation):
    """
    This is an improvement of the original PSO algorithm with Time Varying Inertia Weight operators.

    Empirical study of particle swarm optimization,” in Proc. IEEE Int. Congr. Evolutionary Computation, vol. 3,
    1999, pp. 101–106.

    Shi and Eberhart have observed that the optimal solution can be improved by varying the inertia weight value from
    0.9 (at the beginning of the search) to 0.4 (at the end of the search) for most problems. This modification to the
    original PSO concept has been considered as the basis for two novel strategies introduced in this paper. Hereafter,
    in this paper, this version of PSO is referred to as time-varying inertia weight factor method

    Contras:
    -------
    - PSO-TVIW concept is not very effective for tracking dynamic systems

    - its ability to fine tune the optimum solution is comparatively weak, mainly due
      to the lack of diversity at the end of the search

    R. C. Eberhart and Y. Shi, “Tracking and optimizing dynamic systems with particle swarms,” in Proc. IEEE Congr.
    Evolutionary Computation 2001, Seoul, Korea, 2001, pp. 94–97
    """

    def __init__(self, parameters, probability=1, nr_maxgen=100):
        super().__init__(parameters, probability)
        self.w1 = 0.9  # inertia weight is calculated from w1 and w2
        self.w2 = 0.4
        self.c1 = 2.  # cognitive constant
        self.c2 = 1.  # social constant
        self.best_individual = None

        # new parameters
        self.max_nr_generations = nr_maxgen
        self.current_iter = 0.

    # update new particle velocity
    def update_velocity(self, individual):
        """
        :param nr_generations: total number of generations, during the calculation, MAXITER
        :param iteration_nr: actual generation
        """
        for i in range(0, len(individual.vector)):
            r1 = 0.1 * random.random()
            r2 = 0.1 * random.random()

            # (w1-w2)*(MAX_ITER-iter)/MAX_ITER
            w = (self.w1 - self.w2) * (self.max_nr_generations - self.current_iter) / self.max_nr_generations + self.w2

            vel_cognitive = self.c1 * r1 * (individual.best_vector[i] - individual.vector[i])
            vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
            individual.velocity_i[i] = w * individual.velocity_i[i] + vel_cognitive + vel_social

            self.current_iter += 1.


class SwarmMutationRandIW(SwarmMutation):
    """
    In this variation, the inertia weght is changing randomly,the mean value of the inertia weight is 0.75.
    This modification was inspired by Clerc’s constriction factor concept,  in which the inertia weight is
    kept constant at 0.729 and both acceleration coefficients are kept constant at 1.494.
    Therefore, when random inertia weight factor method is used the acceleration coefficients are kept constant at 1.494.

    Contras:
    -------
    """

    def __init__(self, parameters, probability=1):
        super().__init__(parameters, probability)
        self.w = 0.5  # inertia weight -> changed randomly
        self.c1 = 2.  # cognitive constant
        self.c2 = 1.  # social constant
        self.best_individual = None

    # update new particle velocity
    def update_velocity(self, individual):
        """
        :param nr_generations: total number of generations, during the calculation, MAXITER
        :param iteration_nr: actual generation
        """
        for i in range(0, len(individual.vector)):
            r1 = 0.1 * random.random()
            r2 = 0.1 * random.random()

            # (w1-w2)*(MAX_ITER-iter)/MAX_ITER
            w = self.w * random.random() / 2.

            vel_cognitive = self.c1 * r1 * (individual.best_vector[i] - individual.vector[i])
            vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
            individual.velocity_i[i] = w * individual.velocity_i[i] + vel_cognitive + vel_social


class FireflyMutation(SwarmMutation):
    """
    Firefly algorithm is a modification of the original pso algorithms. The idea is that it mimics the behaviour of
    the fireflies, which uses specfic light combinations for hunting and dating. This algorithm mimics the dating
    behaviour of these bugs. The algorithm is originally published by [1]

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

     Similarly, alpha should also be linked with scales, the steps should not too large or too small, often steps
     are about 1/10 to 1/100 of the domain size. In addition, alpha should be reduced gradually using
     alpha=alpha_0 delta^t during eteration t.  Typically, delta=0.9 to 0.99 will be a good choice.
    """

    def __init__(self, parameters, probability=0.05):
        super().__init__(parameters, probability)

        self.beta = 2.0
        self.alpha = 0.2
        self.ad = 0.98
        self.gamma = 1.

        self.best_individual = None

    def dominate(self, current, other):
        """True if other dominates over current """
        dominates = True

        for i in range(len(current.costs)):
            if other.signed_costs[i] > current.signed_costs[i]:
                dominates = False

        return dominates

    def update_coefficient_a(self):
        """ Updates the mutation coefficient with the damping factor, after each iteration step """
        self.alpha *= self.ad
        return

    # update new particle velocity
    def update_velocity_ij(self, current, other):
        """
        This algorithm has a two-layered hierarchy, because every individual calculates an approximative next position
        from the light intensity between two selected points.
        """
        r2 = 0.  # euclidean distance

        for i, param in enumerate(self.parameters):

            lb = param['bounds'][0]
            ub = param['bounds'][1]

            # elementary distance of the particle
            e = self.probability * (ub - lb)
            # distance between the two individuals
            r2 += current.vector[i] ** 2. + other.vector[i] ** 2.
            vel_attraction = self.beta * exp(-self.gamma * r2 ** 2.)

            v_rd = self.alpha * (random.random() - 0.5) * e
            current.velocity_i[i] = vel_attraction + v_rd

            # for individual in offsprings:
            #     for other in offsprings:
            #         dominates = False
            #
            #         if individual is not other:
            #             dominates = True
            #
            #         for i in range(len(individual.signed_costs)):
            #             if individual.signed_costs[i] > offsprings.signed_costs[i]:
            #                 dominates = False
            #
            #         if dominates:
            #
            #             r2 = 0
            #             for i, param in enumerate(self.parameters):
            #                 l_b = param['bounds'][0]
            #                 u_b = param['bounds'][1]
            #
            #                 # elementary distance of the particle (to do not )
            #                 e = self.probability*(u_b-l_b)
            #                 # distance between the two individuals
            #                 r2 += individual.vector[i]**2. + other.vector[i]**2.
            #
            #                 vel_attraction = self.beta*exp(-self.gamma*r2**2.)
            #
            #                 v_rd = self.alpha * (random.random() - 0.5) * e
            #                 individual.velocity_i[i] = vel_attraction + v_rd
            #
            #                 temp = copy(individual)
            #                 self.evaluate(temp)
            #
            #                 dom = True
            #                 for j in range(len(individual.best_costs)):
            #                     if individual.signed_costs[j] > offsprings.signed_costs[j]:
            #                         dom = False
            #
            #                 if dom is True:
            #                     individual = copy(temp)

            return

    def mutate_ij(self, p, q):
        """
        For firefly algorithm, because of the two-layered hierarchy.

        :param p:
        :param q:
        :return:
        """
        self.update_velocity_ij(p,q)
        self.update_position(p)
        return


class SwarmMutationTVAC(SwarmMutation):
    """
    Time-varying acceleration coefficients as a new parameter automation strategy for the PSO concept.

    An improved optimum solution for most of the benchmarks was observed when changing c1 from 2.5 to 0.5
    and changing c2 from 0.5 to 2.5, over the full range of the search.
    Therefore, these values are used for the rest of the work. With this modification, a significant improvement of
    the optimum value and the rate of convergence were observed, particularly for unimodal functions, compared with
    the PSO-TVIW. However, it has been observed that the performance of the PSO-TVAC method is similar or poor
    for multimodal functions. In contrast, compared with the PSO-RANDIW method an improved performance has been
    observed with the PSO-TVAC for multimodal functions.
    However, for unimodal functions, the PSO-RANDIW method showed significantly quick convergence to a good solution
    compared with the PSO-TVAC method. The results are presented and discussed in Section V.

    Pros: improved convergence rate in case of multi-modal functions

    Cons: significantly slower convergence rate than PSO-RandIW for unimodal functions
    """

    def __init__(self, parameters, probability=1):
        super().__init__(parameters, probability)
        self.w = 0.9  # inertia weight
        self.c1i = 0.5  # cognitive constant initial value
        self.c1f = 2.5  # cognitive constant final value
        self.c2i = 2.5  # social constant initial value
        self.c2f = 0.5  # social constant final value
        self.best_individual = None

    # update new particle velocity
    def update_velocity(self, individual, nr_generations, iteration_nr):
        """
        :param nr_generations: total number of generations, during the calculation, MAXITER
        :param iteration_nr: actual generation
        """
        for i in range(0, len(individual.vector)):
            r1 = 0.1 * random.random()
            r2 = 0.1 * random.random()

            # (c1f-c1i)*(MAX_ITER-iter)/MAX_ITER +
            c1 = (self.c1f - self.c1i) * (nr_generations - iteration_nr) / nr_generations + self.c1i
            c2 = (self.c2f - self.c2i) * (nr_generations - iteration_nr) / nr_generations + self.c2i

            vel_cognitive = c1 * r1 * (individual.best_vector[i] - individual.vector[i])
            vel_social = c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
            individual.velocity_i[i] = self.w * individual.velocity_i[i] + vel_cognitive + vel_social


class Selection(Operation):

    def __init__(self, parameters, part_num=2):
        super().__init__()
        self.parameters = parameters
        # self.signs = signs
        self.part_num = part_num
        self.comparator = ParetoDominance()

    @abstractmethod
    def select(self, population):
        pass

    def is_dominate(self, p, q):
        """
        :param p: current solution
        :param q: candidate
        :return: True if the candidate is better than the current solution
        """
        dominate = False

        # The cost function can be a float or a list of floats
        for i in range(0, len(p.costs)):
            if p.costs[i] > q.costs[i]:
                return False
            if p.costs[i] <= q.costs[i]:
                dominate = True
        return dominate

    def non_dominated_sort(self, population):
        pareto_front = []
        front_number = 1

        for p in population:
            p.domination_counter = 0
            p.front_number = None
            p.dominate = set()

            for q in population:
                if p is q:
                    continue
                if self.comparator.compare(p, q) == 1:  # TODO: simplify
                    p.dominate.add(q)
                elif self.comparator.compare(q, p) == 1:
                    p.domination_counter = p.domination_counter + 1

            if p.domination_counter == 0:
                p.front_number = front_number
                pareto_front.append(p)

        while not len(pareto_front) == 0:
            front_number += 1
            temp_set = []
            for p in pareto_front:
                for q in p.dominate:
                    q.domination_counter -= 1
                    if q.domination_counter == 0 and q.front_number is None:
                        q.front_number = front_number
                        temp_set.append(q)
            pareto_front = temp_set

    def sort_by_coordinate(self, population, dim):
        population.sort(key=lambda x: x.costs[dim])
        return population

    def crowding_distance(self, population):
        infinite = float("inf")
        n = len(population[0].costs)
        for dim in range(0, n):
            new_list = self.sort_by_coordinate(population, dim)

            new_list[0].crowding_distance += infinite
            new_list[-1].crowding_distance += infinite
            max_distance = new_list[0].vector[dim] - new_list[-1].vector[dim]
            for i in range(1, len(new_list) - 1):
                distance = new_list[i - 1].vector[dim] - new_list[i + 1].vector[dim]
                if max_distance == 0:
                    new_list[i].crowding_distance = 0
                else:
                    new_list[i].crowding_distance += distance / max_distance

        for p in population:
            p.crowding_distance = p.crowding_distance / n


class DummySelection(Selection):

    def __init__(self, parameters, part_num=2):
        super().__init__(parameters, part_num)

    def select(self, individuals):
        selection = []
        for individual in individuals:
            candidate = individual.__class__(individual.vector)
            candidate.costs = individual.costs
            candidate.front_number = individual.front_number
            candidate.best_vector = individual.best_vector
            candidate.best_costs = individual.best_costs

            selection.append(candidate)

        return selection


class Dominance(ABC):
    def __init__(self):
        pass

    def compare(self, p, q):
        raise NotImplementedError("method not implemented")


class EpsilonDominance(Dominance):
    """
    Epsilon dominance.

        Similar to Pareto dominance except if the two solutions are contained
        within the same epsilon-box, the solution closer to the optimal corner
        or the box is preferred.
    """

    def __init__(self, epsilons):
        super(EpsilonDominance, self).__init__()

        if hasattr(epsilons, "__getitem__"):
            self.epsilons = epsilons
        else:
            self.epsilons = [epsilons]

    def same_box(self, p, q):
        # first check constraint violation
        if p.feasible != q.feasible:
            if p.feasible == 0:
                return False
            elif q.feasible == 0:
                return False
            elif p.feasible < q.feasible:
                return False
            elif q.feasible < p.feasible:
                return False

        # then use epsilon dominance on the objectives
        dominate1 = False
        dominate2 = False

        for i in range(len(p.costs)):
            o1 = p.costs[i]
            o2 = q.costs[i]

            # in artap we cannot change the direction of the optimization in this way
            # if problem.directions[i] == Problem.MAXIMIZE:
            #    o1 = -o1
            #    o2 = -o2

            epsilon = float(self.epsilons[i % len(self.epsilons)])
            i1 = math.floor(o1 / epsilon)
            i2 = math.floor(o2 / epsilon)

            if i1 < i2:
                dominate1 = True
                if dominate2:
                    return False
            elif i1 > i2:
                dominate2 = True
                if dominate1:
                    return False

        if not dominate1 and not dominate2:
            return True
        else:
            return False

    def compare(self, p, q):
        # first check constraint violation
        if p.feasible != q.feasible:
            if p.feasible == 0:
                return 2
            elif q.feasible == 0:
                return 1
            elif p.feasible < q.feasible:
                return 2
            elif q.feasible < p.feasible:
                return 1

        # then use epsilon dominance on the objectives
        dominate1 = False
        dominate2 = False

        for i in range(len(p.costs)):
            o1 = p.costs[i]
            o2 = q.costs[i]

            epsilon = float(self.epsilons[i % len(self.epsilons)])
            i1 = math.floor(o1 / epsilon)
            i2 = math.floor(o2 / epsilon)

            if i1 < i2:
                dominate1 = True

                if dominate2:
                    return 0
            elif i1 > i2:
                dominate2 = True

                if dominate1:
                    return 0

        if not dominate1 and not dominate2:
            dist1 = 0.0
            dist2 = 0.0

            for i in range(len(p.costs)):
                o1 = p.costs[i]
                o2 = q.costs[i]

                epsilon = float(self.epsilons[i % len(self.epsilons)])
                i1 = math.floor(o1 / epsilon)
                i2 = math.floor(o2 / epsilon)

                dist1 += math.pow(o1 - i1 * epsilon, 2.0)
                dist2 += math.pow(o2 - i2 * epsilon, 2.0)

            if dist1 < dist2:
                return -1
            else:
                return 1
        elif dominate1:
            return -1
        else:
            return 1


class ParetoDominance(Dominance):
    # from platypus core
    """Pareto dominance with constraints.

    If either solution violates constraints, then the solution with a smaller
    constraint violation is preferred.  If both solutions are feasible, then
    Pareto dominance is used to select the preferred solution.
    """

    def __init__(self, epsilons=None):
        super(ParetoDominance, self).__init__()
        # self.signs = signs deprecated

    # @jit
    def compare(self, p: list, q: list):
        """
        Here, p and q are tuples, which contains the (feasibility index, cost vector)
        """

        # first check constraint violation
        if p[-1] != q[-1]:
            if p[-1] == 0:
                return 1
            elif q[-1] == 0:
                return 2
            elif p[-1] < q[0]:
                return 1
            elif q[-1] < p[0]:
                return 2

        # if p.feasible != q.feasible:
        #     if p.feasible == 0:
        #         return 1
        #     elif q.feasible == 0:
        #         return 2
        #     elif p.feasible < q.feasible:
        #         return 1
        #     elif q.feasible < p.feasible:
        #         return 2

        # The cost function can be a float or a list of floats
        # Check the pareto dominance on every value of the calculated vectors

        # numpy makes the calculation elementwise, so we are calculating the result vector at first
        # and checks that is p can dominate q
        # res = p>q
        #
        # dominate_p = False
        # dominate_q = False
        #
        # for i in res[:-1]:
        #     if i:
        #         dominate_q = True
        #         if dominate_p:
        #             return 0
        #     else:
        #         dominate_p = True
        #         if dominate_q:
        #             return 0
        #
        # if dominate_p == dominate_q:
        #     return 0
        #
        # elif dominate_p:
        #     return 1
        # else:
        #     return 2

        # the old solution
        # dominate_p = False
        # dominate_q = False
        #
        # for (p_costs, q_costs, sign) in zip(p.costs, q.costs, self.signs):
        #
        #     if sign * p_costs > sign * q_costs:
        #         dominate_q = True
        #         if dominate_p:
        #             return 0
        #     else:
        #         dominate_p = True
        #         if dominate_q:
        #             return 0
        #
        # if dominate_q == dominate_p:
        #     return 0
        # elif dominate_p:
        #     return 1
        # else:
        #     return 2

        dominate_p = False
        dominate_q = False

        for (p_costs, q_costs) in zip(p[:-1], q[:-1]):

            if p_costs > q_costs:
                dominate_q = True
                if dominate_p:
                    return 0
            else:
                dominate_p = True
                if dominate_q:
                    return 0

        if dominate_q == dominate_p:
            return 0
        elif dominate_p:
            return 1
        else:
            return 2


class Selection(Operation):

    def __init__(self, parameters, sign=None, part_num=2, dominance=ParetoDominance):
        """

        :param parameters:
        :param sign: one value from now, because its goal is to tell the direction of the optimum min or max
        :param part_num:
        :param dominance:
        """
        super().__init__()
        self.parameters = parameters
        self.part_num = part_num
        self.comparator = dominance()  # ParetoDominance()
        self.signs = sign

    @abstractmethod
    def select(self, population):
        pass

    def is_dominate(self, p, q):
        """
        :param p: current solution
        :param q: candidate
        :return: True if the candidate is better than the current solution
        """
        # The cost function can be a float or a list of floats
        for p_costs, q_costs in zip(p.costs, q.costs):
            if p_costs > q_costs:
                return False
            else:
                return True

    def sorting(self, generation):
        """
        This shoring can be dominated or non-dominated.
        :param generation: means the list of the population, it can be list of the individuals or the archive.
        :return:
        """
        pareto_front = []
        front_number = 1

        for p in generation:
            p.domination_counter = 0
            p.front_number = None
            p.dominate = set()

            for q in generation:
                if p is q:
                    continue
                if self.comparator.compare(p.signed_costs, q.signed_costs) == 1:  # TODO: simplify
                    p.dominate.add(q)
                elif self.comparator.compare(q.signed_costs, p.signed_costs) == 1:
                    p.domination_counter += 1

            if p.domination_counter == 0:
                p.front_number = front_number
                pareto_front.append(p)

        while not len(pareto_front) == 0:
            front_number += 1
            temp_set = []
            for p in pareto_front:
                for q in p.dominate:
                    q.domination_counter -= 1
                    if q.domination_counter == 0 and q.front_number is None:
                        q.front_number = front_number
                        temp_set.append(q)
            pareto_front = temp_set
        return

    def sort_by_coordinate(self, population, dim):
        population.sort(key=lambda x: x.costs[dim])
        return population

    def crowding_distance(self, population):
        infinite = float("inf")
        n = len(population[0].costs)
        for dim in range(0, n):
            new_list = self.sort_by_coordinate(population, dim)

            new_list[0].crowding_distance += infinite
            new_list[-1].crowding_distance += infinite
            max_distance = new_list[0].vector[dim] - new_list[-1].vector[dim]
            for i in range(1, len(new_list) - 1):
                distance = new_list[i - 1].vector[dim] - new_list[i + 1].vector[dim]
                if max_distance == 0:
                    new_list[i].crowding_distance = 0
                else:
                    new_list[i].crowding_distance += distance / max_distance

        for p in population:
            p.crowding_distance = p.crowding_distance / n


class DummySelection(Selection):

    def __init__(self, parameters, sign, part_num=2):
        super().__init__(parameters, sign, part_num)

    def select(self, individuals):
        selection = []
        for individual in individuals:
            candidate = individual.__class__(individual.vector)
            candidate.costs = individual.costs
            candidate.front_number = individual.front_number
            candidate.best_vector = individual.best_vector
            candidate.best_costs = individual.best_costs

            selection.append(candidate)
        return selection


class TournamentSelection(Selection):

    def __init__(self, parameters, dominance=ParetoDominance, epsilons=None):
        super().__init__(parameters)
        self.dominance = dominance(epsilons=epsilons)
        # self.signs = sign
        # self.dominance = EpsilonDominance([0.01])

    def select(self, population):
        """
        Binary tournament selection:
        An individual is selected in the rank is lesser than the other or if crowding distance is greater than the other
        """

        # participants = random.sample(population, 2)
        # return min(participants, key=lambda x: (x.front_number, -x.crowding_distance))

        winner = random.choice(population)

        for _ in range(self.part_num - 1):
            candidate = random.choice(population)

            flag = self.dominance.compare(winner.signed_costs, candidate.signed_costs)

            if flag > 0:
                winner = candidate

        return winner

        # participants = random.sample(parents, part_num)
        # return min(participants, key=lambda x: (x.front_number, -x.crowding_distance))


class Archive(object):
    """An archive only containing non-dominated solutions."""

    def __init__(self, signs, dominance=ParetoDominance):
        super(Archive, self).__init__()
        self._dominance = dominance(signs=signs)
        self._contents = []

    def add(self, solution):
        flags = [self._dominance.compare(solution, s) for s in self._contents]
        dominates = [x > 0 for x in flags]
        nondominated = [x == 0 for x in flags]

        if any(dominates):
            return False
        else:
            self._contents = list(itertools.compress(self._contents, nondominated)) + [solution]
            return True

    def append(self, solution):
        self.add(solution)

    def extend(self, solutions):
        for solution in solutions:
            self.append(solution)

    def remove(self, solution):
        try:
            self._contents.remove(solution)
            return True
        except ValueError:
            return False

    def __len__(self):
        return len(self._contents)

    def __getitem__(self, key):
        return self._contents[key]

    def __iadd__(self, other):
        if hasattr(other, "__iter__"):
            for o in other:
                self.add(o)
        else:
            self.add(other)

        return self

    def __iter__(self):
        return iter(self._contents)


class EpsilonBoxArchive(Archive):

    def __init__(self, epsilons):
        super(EpsilonBoxArchive, self).__init__(EpsilonDominance(epsilons))
        self.improvements = 0

    def add(self, solution):
        flags = [self._dominance.compare(solution, s) for s in self._contents]
        dominates = [x > 0 for x in flags]
        nondominated = [x == 0 for x in flags]
        dominated = [x < 0 for x in flags]
        not_same_box = [not self._dominance.same_box(solution, s) for s in self._contents]

        if any(dominates):
            return False
        else:
            self._contents = list(itertools.compress(self._contents, nondominated)) + [solution]

            if dominated and not_same_box:
                self.improvements += 1


class Crossover(Operation):

    def __init__(self, parameters, probability):
        super().__init__()
        self.parameters = parameters
        self.probability = probability

    @abstractmethod
    def cross(self, p1, p2):
        pass


class SimpleCrossover(Crossover):

    def __init__(self, parameters, probability):
        super().__init__(parameters, probability)

    def cross(self, p1, p2):
        parent_a = p1.vector.copy()
        parent_b = p2.vector.copy()

        if random.uniform(0.0, 1.0) <= self.probability:
            parameter1 = []
            parameter2 = []
            linear_range = 2

            alpha = random.uniform(0, linear_range)

            for i, param in enumerate(self.parameters):
                l_b = param['bounds'][0]
                u_b = param['bounds'][1]

                parameter1.append(self.clip(alpha * p1.vector[i] + (1 - alpha) * p2.vector[i], l_b, u_b))
                parameter2.append(self.clip((1 - alpha) * p1.vector[i] + alpha * p2.vector[i], l_b, u_b))

            parent_a = parameter1
            parent_b = parameter2

        offspring_a = p1.__class__(parent_a)
        offspring_b = p2.__class__(parent_b)

        return offspring_a, offspring_b


class SimulatedBinaryCrossover(Crossover):

    def __init__(self, parameters, probability, distribution_index=15):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index

    def sbx(self, x1, x2, lb, ub, p_type="real"):

        dx = x2 - x1

        if dx > EPSILON:
            if x2 > x1:
                y2 = x2
                y1 = x1
            else:
                y2 = x1
                y1 = x2

            beta = 1.0 / (1.0 + (2.0 * (y1 - lb) / (y2 - y1)))
            alpha = 2.0 - pow(beta, self.distribution_index + 1.0)
            rand = random.uniform(0.0, 1.0)

            if rand <= 1.0 / alpha:
                alpha = alpha * rand
                betaq = pow(alpha, 1.0 / (self.distribution_index + 1.0))
            else:
                alpha = alpha * rand
                alpha = 1.0 / (2.0 - alpha)
                betaq = pow(alpha, 1.0 / (self.distribution_index + 1.0))

            x1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
            beta = 1.0 / (1.0 + (2.0 * (ub - y2) / (y2 - y1)))
            alpha = 2.0 - pow(beta, self.distribution_index + 1.0)

            if rand <= 1.0 / alpha:
                alpha = alpha * rand
                betaq = pow(alpha, 1.0 / (self.distribution_index + 1.0))
            else:
                alpha = alpha * rand
                alpha = 1.0 / (2.0 - alpha)
                betaq = pow(alpha, 1.0 / (self.distribution_index + 1.0))

            x2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))

            # randomly swap the values
            if bool(random.getrandbits(1)):
                x1, x2 = x2, x1

            x1 = self.clip(x1, lb, ub)
            x2 = self.clip(x2, lb, ub)

            if p_type == "integer":
                x1 = int(x1)
                x2 = int(x2)

        return x1, x2

    def cross(self, p1, p2):
        """
        Create an offspring using simulated binary crossover.
        :return:  a list with 2 offsprings each with the genotype of an  offspring after recombination and mutation.
        """

        parent_a = p1.vector.copy()
        parent_b = p2.vector.copy()

        if random.uniform(0.0, 1.0) <= self.probability:
            for i, param in enumerate(self.parameters):
                if random.uniform(0.0, 1.0) <= 0.5:
                    x1 = parent_a[i]
                    x2 = parent_b[i]

                    lb = param['bounds'][0]
                    ub = param['bounds'][1]

                    if not 'parameter_type' in param:
                        continue
                    else:
                        p_type = param['parameter_type']

                    x1, x2 = self.sbx(x1, x2, lb, ub, p_type)

                    parent_a[i] = x1
                    parent_b[i] = x2

        offspring_a = p1.__class__(parent_a)
        offspring_b = p2.__class__(parent_b)

        return offspring_a, offspring_b
