from abc import abstractmethod, ABC
import sys
import random
import math
from math import exp
import numpy as np
import functools
import itertools

from .individual import Individual
from .utils import VectorAndNumbers
from .doe import build_box_behnken, build_lhs, build_full_fact, build_plackett_burman, build_gsd, build_halton
from .job import Job
from joblib import Parallel, delayed
from copy import deepcopy

EPSILON = sys.float_info.epsilon

# global constants to p and q dominates
QDOM = 1
PDOM = 2


class Operator(ABC):

    def __init__(self):
        pass

    @staticmethod
    def clip(value, min_value, max_value):
        return max(min_value, min(value, max_value))


# TODO: Change name of classes to Evaluator?
class Evaluator(Operator):

    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.individuals = []
        self.job = Job(self.algorithm.problem)

    def add(self, individual):
        self.individuals.append(individual)

    def run(self):
        self.evaluate(self.individuals)

    def evaluate(self, individuals):
        if self.algorithm.options["max_processes"] > 1:
            self.evaluate_parallel(individuals)
        else:
            self.evaluate_serial(individuals)

    def evaluate_serial(self, individuals: list):
        for individual in individuals:
            if individual.state == individual.State.EMPTY:
                individual.costs.append(self.job.evaluate(individual))

    def evaluate_parallel(self, individuals: list):
        # simple parallel loop
        Parallel(n_jobs=self.algorithm.options["max_processes"], verbose=1, require='sharedmem')(
            delayed(self.job.evaluate)(individual)
            for individual in individuals)

    def evaluate_scalar(self, vector):
        individual = Individual(list(vector))

        # add to problem
        self.algorithm.problem.individuals.append(individual)

        self.job.evaluate(individual)
        return individual.costs[0]


class GradientEvaluator(Evaluator):

    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.delta = 1e-4
        self.to_evaluate = []
        self.algorithm.problem.costs.append({'name': 'sensitivity', 'criteria': 'minimize'})
        self.n = len(algorithm.problem.costs)

    def add(self, individual):
        self.individuals.append(individual)
        individual.children = []

        for i in range(len(individual.vector)):
            vector = individual.vector.copy()
            vector[i] += self.delta
            individual.children.append(Individual(vector))
            individual.children[-1].parents.append(individual)

        self.to_evaluate.append(individual)
        self.to_evaluate.extend(individual.children)

    def evaluate(self, individuals):
        for individual in individuals:
            self.add(individual)
        self.run()

    def evaluate_scalar(self, x):
        individual = Individual(x)

        self.add(individual)
        self.run()
        self.algorithm.problem.individuals.append(individual)
        self.to_evaluate = []

        return individual.costs[0]

    def run(self):
        n_params = len(self.individuals[0].vector)
        super().evaluate(self.to_evaluate)
        for individual in self.individuals:
            gradient = np.zeros(n_params)
            i = 0
            for child in individual.children:
                gradient[i] = ((child.costs[0] - individual.costs[0]) / self.delta)
                i += 1
            individual.features['gradient'] = gradient
            if any(gradient < 0):
                sensitivity = 1000
            else:
                sensitivity = sum(abs(gradient))
            if len(individual.costs) > self.n:
                individual.costs[-1] = sensitivity
                individual.costs_signed[-2] = sensitivity
            else:
                individual.costs.append(sensitivity)
                individual.costs_signed.insert(-1, sensitivity)

        self.individuals = []
        self.to_evaluate = []


class WorstCaseEvaluator(Evaluator):

    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.algorithm.problem.costs.append({'name': 'sensitivity', 'criteria': 'minimize'})
        self.n = len(algorithm.problem.costs)
        self.to_evaluate = []

    def add(self, individual):
        parameters = self.algorithm.problem.parameters
        individual.children = []
        self.individuals.append(individual)
        for i in range(len(individual.vector)):
            parameter = parameters[i]
            for sign in [-1, 1]:
                vector = individual.vector.copy()
                vector[i] += sign * parameter['tol']
                individual.children.append(Individual(vector))
                individual.children[-1].parents.append(individual)

        self.to_evaluate.append(individual)
        self.to_evaluate.extend(individual.children)

    def evaluate(self, individuals):
        super().evaluate(individuals)
        for individual in individuals:
            self.add(individual)
        self.run()

    def evaluate_scalar(self, x):
        parent_individual = Individual(x)
        parent_individual.costs.append(self.job.evaluate(parent_individual))
        self.add(parent_individual)
        for individual in self.to_evaluate:
            individual.costs.append(self.job.evaluate(individual))
        self.algorithm.problem.individuals.append(parent_individual)
        self.to_evaluate = []
        return parent_individual.costs[0]

    def run(self):
        super().evaluate(self.to_evaluate)
        for individual in self.individuals:
            sensitivity = []
            for child in individual.children:
                sensitivity.append(abs(individual.costs[0] - child.costs[0]))
            individual.features['sensitivity'] = sum(sensitivity)

            if len(individual.costs) > self.n:
                individual.costs[-1] = sum(sensitivity)
                individual.costs_signed[-2] = sum(sensitivity)
            else:
                individual.costs.append(sum(sensitivity))
                individual.costs_signed.insert(-1, sum(sensitivity))


class Generator(Operator):
    def __init__(self, parameters=None, features=dict()):
        super().__init__()
        self.parameters = parameters
        self.features = features

    @abstractmethod
    def generate(self):
        pass


class CustomGenerator(Generator):
    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
        self.vectors = []

    def init(self, vectors):
        self.vectors = vectors

    def generate(self):
        individuals = []
        for vector in self.vectors:
            individuals.append(Individual(vector, self.features))
        return individuals


class UniformGenerator(Generator):
    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
        self.number = 0

    def init(self, number):
        self.number = number

    def generate(self):
        individuals = []
        vectors = []
        for parameter in self.parameters:
            vectors.append([])
            delta = (parameter['bounds'][1] - parameter['bounds'][0]) / (self.number - 1)
            for i in range(self.number):
                vectors[-1].append(parameter['bounds'][0] + i*delta)

        for combination in itertools.product(*vectors):
            individuals.append(Individual(list(combination), self.features))

        return individuals


class RandomGenerator(Generator):
    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
        self.number = 0

    def init(self, number):
        self.number = number

    def generate(self):
        individuals = []
        for i in range(self.number):
            vector = VectorAndNumbers.gen_vector(self.parameters)
            individuals.append(Individual(vector, self.features))
        return individuals


class FullFactorGenerator(Generator):
    """
    Create a general full-factorial design
    Number of experiments (2 ** len(parameters) - without center, 3 ** len(parameters - with center)
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
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
            individuals.append(Individual(vector, self.features))
        return individuals


class FullFactorLevelsGenerator(Generator):
    """
    Create a general full-factorial design
    Number of experiments (2 ** len(parameters) - without center, 3 ** len(parameters - with center)
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
        self.values = []

    def init(self, values):
        self.values = values

    def generate(self):
        dict_vars = {}
        for value, parameter in zip(self.values, self.parameters):
            dict_vars[parameter['name']] = value

        df = build_full_fact(dict_vars)

        individuals = []
        for vector in df:
            individuals.append(Individual(vector, self.features))
        return individuals


class PlackettBurmanGenerator(Generator):
    """
    Create a general full-factorial design
    Number of experiments (2 ** len(parameters) - without center, 3 ** len(parameters - with center)
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)

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
            individuals.append(Individual(vector, self.features))
        return individuals


class BoxBehnkenGenerator(Generator):
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

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)

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
            individuals.append(Individual(vector, self.features))
        return individuals


class LHSGenerator(Generator):
    """
    Builds a Latin Hypercube design dataframe from a dictionary of factor/level ranges.
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
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
            individuals.append(Individual(vector, self.features))
        return individuals


class HaltonGenerator(Generator):
    """
    Builds a Halton sequence.
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
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

        df = build_halton(dict_vars, num_samples=self.number)
        print(df)

        individuals = []
        for vector in df:
            individuals.append(Individual(vector, self.features))
        return individuals


class GSDGenerator(Generator):
    """
    Builds a Latin Hypercube design dataframe from a dictionary of factor/level ranges.
    """

    def __init__(self, parameters=None, features=dict()):
        super().__init__(parameters, features)
        self.values = []
        self.reduction = 1
        self.n = 1

    def init(self, values, reduction, n=1):
        self.values = values
        self.reduction = reduction
        self.n = n

    def generate(self):
        levels = []
        for value in self.values:
            levels.append(len(value))

        df = build_gsd(levels, self.reduction, self.n)
        # print(df)

        individuals = []
        for vector in df:
            vals = []
            for i in range(len(vector)):
                vals.append(self.values[i][vector[i]])
            individuals.append(Individual(vals, self.features))
        return individuals


class Mutator(Operator):
    def __init__(self, parameters, probability):
        super().__init__()
        self.parameters = parameters
        self.probability = probability

    @abstractmethod
    def mutate(self, p, current_iteration=0):
        pass


class SimpleMutator(Mutator):
    def __init__(self, parameters, probability):
        super().__init__(parameters, probability)

    def mutate(self, p, current_iteration=0):
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

        p_new = Individual(vector, p.features)
        return p_new


class PmMutator(Mutator):
    """
    PmMutation -- for nsga2 and epsMoEA

    This operator can handle real, integer and boolean optimization parameters.
    The class contains two-kind of operators as the original Deb's implementation .
    """

    def __init__(self, parameters, probability, distribution_index=20):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index

    def mutate(self, parent, current_iteration=0):
        vector = []

        for i, parameter in enumerate(self.parameters):
            if random.uniform(0, 1) < self.probability:
                l_b = parameter['bounds'][0]
                u_b = parameter['bounds'][1]
                vector.append(self.pm_mutation(parent.vector[i], l_b, u_b))
            else:
                vector.append(parent.vector[i])

        return Individual(vector, parent.features)

    def pm_mutation(self, x, lb, ub):
        """
        Polynomial mutation for float and integer parameters.

        :param x: represents one parameter of the problem
        :param lb: lower bound
        :param ub: upper bound
        :return:
        """
        rnd = random.uniform(0, 1)
        dx = ub - lb
        delta1 = (x - lb) / dx
        delta2 = (ub - x) / dx
        mut_pow = 1.0 / (self.distribution_index + 1.0)
        if rnd < 0.5:
            xy = 1.0 - delta1
            val = 2.0 * rnd + (1.0 - 2.0 * rnd) * (pow(xy, self.distribution_index + 1.0))
            deltaq = pow(val, mut_pow) - 1.0
        else:
            xy = 1.0 - delta2
            val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * (pow(xy, self.distribution_index + 1.0))
            deltaq = 1.0 - pow(val, mut_pow)

        x = x + deltaq * dx
        x = self.clip(x, lb, ub)

        return x

    def bitflip(self, x: list):

        for j in range(1, len(x)):
            if random.uniform(0.0, 1.0) <= self.probability:
                x[j] = not x[j]

        return x


class UniformMutator(Mutator):
    """
    Uniform mutator -- for omopso .
    """

    def __init__(self, parameters, probability, perturbation=0.5):
        super().__init__(parameters, probability)
        self.perturbation = perturbation

    def mutate(self, parent, current_iteration=0):
        vector = []

        for i, parameter in enumerate(self.parameters):
            if random.uniform(0, 1) < self.probability:
                l_b = parameter['bounds'][0]
                u_b = parameter['bounds'][1]
                vector.append(self.uniform_mutation(parent.vector[i], l_b, u_b))
            else:
                vector.append(parent.vector[i])

        return Individual(vector, parent.features)

    def uniform_mutation(self, x, lb, ub):

        x = x + (random.random() - 0.5) * self.perturbation
        x = self.clip(x, lb, ub)

        return x


class NonUniformMutation(Mutator):

    def __init__(self, parameters, probability, max_iterations, perturbation=0.5, ):
        super().__init__(parameters, probability)
        self.perturbation = perturbation
        self.max_iterations = max_iterations

    def __delta(self, y: float, b_mutation_parameter: float, current_iteration):
        return (y * (1.0 - pow(random.random(),
                               pow((1.0 - 1.0 * current_iteration / self.max_iterations), b_mutation_parameter))))

    def mutate(self, parent, current_iteration=0):
        vector = []

        for i, parameter in enumerate(self.parameters):
            if random.uniform(0, 1) < self.probability:
                l_b = parameter['bounds'][0]
                u_b = parameter['bounds'][1]
                vector.append(self.non_uniform_mutation(parent.vector[i], l_b, u_b, current_iteration))
            else:
                vector.append(parent.vector[i])

        return Individual(vector, parent.features)

    def non_uniform_mutation(self, x, lb, ub, current_iteration):

        rand = random.random()

        if rand <= 0.5:
            x = self.__delta(ub - x, self.perturbation, current_iteration)
        else:
            x = self.__delta(lb - x, self.perturbation, current_iteration)

        if isinstance(x, complex):
            print(x)
        x = self.clip(x, lb, ub)

        return x


# class SwarmStep(Mutator):
#     """
#     This swarm mutator operator is made for the original PSO algorithm, which defined by Kennedy and Eberhart in 1995
#
#     PSO shares many similarities with evolutionary computation. Both algorithms start with a group of a randomly
#     generated population. Both update the population iteratively and search for the optimum with stochastic techniques.
#     The main difference between them is in the information sharing mechanism. In EA, only the individuals of current
#     generation share information with each other, and any individual has a chance to give out information to others.
#     In PSO, actually not the current individuals share information with each other, but the individuals of previous
#     generation (the optimal particles) give out information to the current ones. In other words, the information sharing
#     is one-way in PSO.
#     """
#
#     def __init__(self, parameters, probability=1):
#         super().__init__(parameters, probability)
#         self.w = 0.1  # constant inertia weight (how much to weigh the previous velocity)
#         self.c1 = 2.  # cognitive constant
#         self.c2 = 1.  # social constant
#         self.best_individual = None
#
#     def evaluate_best_individual(self, individual):
#         """ Determines the best individual in the swarm """
#         dominates = True
#         individual.features['best_costs'] = [0] * len(individual.costs)
#         for i in range(len(individual.features['best_costs'])):
#             if individual.costs[i] > individual.features['best_costs'][i]:
#                 dominates = False
#
#         # check to see if the current position is an individual best
#         if dominates:
#             individual.features['best_vector'] = individual.vector
#             individual.features['best_costs'] = individual.costs
#
#     # update new particle velocity
#     def update_velocity(self, individual):
#         individual.features['velocity'] = [0] * len(individual.vector)
#         individual.features['best_vector'] = [0] * len(individual.vector)
#         for i in range(0, len(individual.vector)):
#             r1 = 0.1 * random.random()
#             r2 = 0.1 * random.random()
#
#             vel_cognitive = self.c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
#             vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
#             individual.features['velocity'][i] = self.w * individual.features['velocity'][
#                 i] + vel_cognitive + vel_social
#
#     # update the particle position based off new velocity updates
#     def update_position(self, individual):
#
#         for parameter, i in zip(self.parameters, range(len(individual.vector))):
#             individual.vector[i] = individual.vector[i] + individual.features['velocity'][i]
#
#             # adjust maximum position if necessary
#             if individual.vector[i] > parameter['bounds'][1]:
#                 individual.vector[i] = parameter['bounds'][1]
#
#             # adjust minimum position if necessary
#             if individual.vector[i] < parameter['bounds'][0]:
#                 individual.vector[i] = parameter['bounds'][0]
#
#     def update(self, best_individual):
#         self.best_individual = best_individual
#
#     def mutate(self, p):
#         self.update_velocity(p)
#         self.update_position(p)
#         return p
#

# class SwarmStepTVIW(SwarmStep):
#     """
#     This is an improvement of the original PSO algorithm with Time Varying Inertia Weight operators.
#
#     Empirical study of particle swarm optimization,” in Proc. IEEE Int. Congr. Evolutionary Computation, vol. 3,
#     1999, pp. 101–106.
#
#     Shi and Eberhart have observed that the optimal solution can be improved by varying the inertia weight value from
#     0.9 (at the beginning of the search) to 0.4 (at the end of the search) for most problems. This modification to the
#     original PSO concept has been considered as the basis for two novel strategies introduced in this paper. Hereafter,
#     in this paper, this version of PSO is referred to as time-varying inertia weight factor method
#
#     Contras:
#     -------
#     - PSO-TVIW concept is not very effective for tracking dynamic systems
#
#     - its ability to fine tune the optimum solution is comparatively weak, mainly due
#       to the lack of diversity at the end of the search
#
#     R. C. Eberhart and Y. Shi, “Tracking and optimizing dynamic systems with particle swarms,” in Proc. IEEE Congr.
#     Evolutionary Computation 2001, Seoul, Korea, 2001, pp. 94–97
#     """
#
#     def __init__(self, parameters, probability=1, nr_maxgen=100):
#         super().__init__(parameters, probability)
#         self.w1 = 0.9  # inertia weight is calculated from w1 and w2
#         self.w2 = 0.4
#         self.c1 = 2.  # cognitive constant
#         self.c2 = 1.  # social constant
#         self.best_individual = None
#
#         # new parameters
#         self.max_nr_generations = nr_maxgen
#         self.current_iter = 0.
#
#     # update new particle velocity
#     def update_velocity(self, individual):
#         """
#         :param nr_generations: total number of generations, during the calculation, MAXITER
#         :param iteration_nr: actual generation
#         """
#
#         individual.features['velocity'] = [0] * len(individual.vector)
#         individual.features['best_vector'] = [0] * len(individual.vector)
#         for i in range(0, len(individual.vector)):
#             r1 = 0.1 * random.random()
#             r2 = 0.1 * random.random()
#
#             # (w1-w2)*(MAX_ITER-iter)/MAX_ITER
#             w = (self.w1 - self.w2) * (self.max_nr_generations - self.current_iter) / self.max_nr_generations + self.w2
#
#             vel_cognitive = self.c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
#             vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
#             individual.features['velocity'][i] = w * individual.features['velocity'][i] + vel_cognitive + vel_social
#
#             self.current_iter += 1.
#

# class SwarmStepRandIW(SwarmStep):
#     """
#     In this variation, the inertia weght is changing randomly,the mean value of the inertia weight is 0.75.
#     This modification was inspired by Clerc’s constriction factor concept,  in which the inertia weight is
#     kept constant at 0.729 and both acceleration coefficients are kept constant at 1.494.
#     Therefore, when random inertia weight factor method is used the acceleration coefficients are kept constant at 1.494.
#
#     Contras:
#     -------
#     """
#
#     def __init__(self, parameters, probability=1):
#         super().__init__(parameters, probability)
#         self.w = 0.5  # inertia weight -> changed randomly
#         self.c1 = 2.  # cognitive constant
#         self.c2 = 1.  # social constant
#         self.best_individual = None
#
#     # update new particle velocity
#     def update_velocity(self, individual):
#         """
#         :param nr_generations: total number of generations, during the calculation, MAXITER
#         :param iteration_nr: actual generation
#         """
#         for i in range(0, len(individual.vector)):
#             r1 = 0.1 * random.random()
#             r2 = 0.1 * random.random()
#
#             # (w1-w2)*(MAX_ITER-iter)/MAX_ITER
#             w = self.w * random.random() / 2.
#
#             vel_cognitive = self.c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
#             vel_social = self.c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
#             individual.velocity_i[i] = w * individual.velocity_i[i] + vel_cognitive + vel_social
#

# class FireflyStep(SwarmStep):
#     """
#     Firefly algorithm is a modification of the original pso algorithms. The idea is that it mimics the behaviour of
#     the fireflies, which uses specfic light combinations for hunting and dating. This algorithm mimics the dating
#     behaviour of these bugs. The algorithm is originally published by [1]
#
#     The brightest individual attracts the darkest ones, this starts to go to that direction, if there is not an
#     existing brighter solutions, the algorithm randomly steps one into another direction.
#
#     This operator makes the following
#     ---------------------------------
#
#     - calculates the distance between two points, because its correlates with that value.
#     - the brightness of the other point
#     - the mutator constant, which contains a damping factor [2]?
#
#     The k+1 th position of the j(th) individual is calculated by the following formula
#     ---------------------------------------------------------------------------
#
#         b0=2;               # Attraction Coefficient Base Value
#         a=0.2;              # Mutation Coefficient
#         ad=0.98;            # Mutation Coefficient Damping Ratio -- decreases the initial value of a after each
#                               iteration step
#         gamma = 1.          # light absorbtion coefficient
#
#         x(j,k+1) = x(j,k) + b0*exp(-gamma*r^2) + sum_{i<j}[x(j,k) - x(i,k)] + a*(rand[0,1] - 0.5)
#
#     [1] Yang, Xin-She. "Firefly algorithms for multimodal optimization." International symposium on stochastic algorithms.
#         Springer, Berlin, Heidelberg, 2009.
#     [2] firefly algorithm implementation from www.Yarpiz.com
#
#     [3] https://nl.mathworks.com/matlabcentral/fileexchange/29693-firefly-algorithm
#
#      Similarly, alpha should also be linked with scales, the steps should not too large or too small, often steps
#      are about 1/10 to 1/100 of the domain size. In addition, alpha should be reduced gradually using
#      alpha=alpha_0 delta^t during eteration t.  Typically, delta=0.9 to 0.99 will be a good choice.
#     """
#
#     def __init__(self, parameters, probability=0.05):
#         super().__init__(parameters, probability)
#
#         self.beta = 2.0
#         self.alpha = 0.2
#         self.ad = 0.98
#         self.gamma = 1.
#
#         self.best_individual = None
#
#     def dominate(self, current, other):
#         """True if other dominates over current """
#         dominates = True
#
#         for i in range(len(current.costs)):
#             if other.costs_signed[i] > current.costs_signed[i]:
#                 dominates = False
#
#         return dominates
#
#     def update_coefficient_a(self):
#         """ Updates the mutation coefficient with the damping factor, after each iteration step """
#         self.alpha *= self.ad
#         return
#
#     # update new particle velocity
#     def update_velocity_ij(self, current, other):
#         """
#         This algorithm has a two-layered hierarchy, because every individual calculates an approximative next position
#         from the light intensity between two selected points.
#         """
#         r2 = 0.  # euclidean distance
#
#         for i, param in enumerate(self.parameters):
#             lb = param['bounds'][0]
#             ub = param['bounds'][1]
#
#             # elementary distance of the particle
#             e = self.probability * (ub - lb)
#             # distance between the two individuals
#             r2 += current.vector[i] ** 2. + other.vector[i] ** 2.
#             vel_attraction = self.beta * exp(-self.gamma * r2 ** 2.)
#
#             v_rd = self.alpha * (random.random() - 0.5) * e
#             current.velocity_i[i] = vel_attraction + v_rd
#
#             return
#
#     def mutate_ij(self, p, q):
#         """
#         For firefly algorithm, because of the two-layered hierarchy.
#
#         :param p:
#         :param q:
#         :return:
#         """
#         self.update_velocity_ij(p, q)
#         self.update_position(p)
#         return
#
#
# class SwarmStepTVAC(SwarmStep):
#     """
#     Time-varying acceleration coefficients as a new parameter automation strategy for the PSO concept.
#
#     An improved optimum solution for most of the benchmarks was observed when changing c1 from 2.5 to 0.5
#     and changing c2 from 0.5 to 2.5, over the full range of the search.
#     Therefore, these values are used for the rest of the work. With this modification, a significant improvement of
#     the optimum value and the rate of convergence were observed, particularly for unimodal functions, compared with
#     the PSO-TVIW. However, it has been observed that the performance of the PSO-TVAC method is similar or poor
#     for multimodal functions. In contrast, compared with the PSO-RANDIW method an improved performance has been
#     observed with the PSO-TVAC for multimodal functions.
#     However, for unimodal functions, the PSO-RANDIW method showed significantly quick convergence to a good solution
#     compared with the PSO-TVAC method. The results are presented and discussed in Section V.
#
#     Pros: improved convergence rate in case of multi-modal functions
#
#     Cons: significantly slower convergence rate than PSO-RandIW for unimodal functions
#     """
#
#     def __init__(self, parameters, probability=1):
#         super().__init__(parameters, probability)
#         self.w = 0.9  # inertia weight
#         self.c1i = 0.5  # cognitive constant initial value
#         self.c1f = 2.5  # cognitive constant final value
#         self.c2i = 2.5  # social constant initial value
#         self.c2f = 0.5  # social constant final value
#         self.best_individual = None
#
#     # update new particle velocity
#     def update_velocity(self, individual, nr_generations, iteration_nr):
#         """
#         :param nr_generations: total number of generations, during the calculation, MAXITER
#         :param iteration_nr: actual generation
#         """
#         for i in range(0, len(individual.vector)):
#             r1 = 0.1 * random.random()
#             r2 = 0.1 * random.random()
#
#             # (c1f-c1i)*(MAX_ITER-iter)/MAX_ITER +
#             c1 = (self.c1f - self.c1i) * (nr_generations - iteration_nr) / nr_generations + self.c1i
#             c2 = (self.c2f - self.c2i) * (nr_generations - iteration_nr) / nr_generations + self.c2i
#
#             vel_cognitive = c1 * r1 * (individual.features['best_vector'][i] - individual.vector[i])
#             vel_social = c2 * r2 * (self.best_individual.vector[i] - individual.vector[i])
#             individual.velocity_i[i] = self.w * individual.velocity_i[i] + vel_cognitive + vel_social
#

class Dominance(ABC):
    def __init__(self):
        pass

    def compare(self, p, q):
        raise NotImplementedError("method not implemented")


class EpsilonDominance(Dominance):
    """
    Epsilon dominance comparator divides the number
    """

    def __init__(self, epsilons):
        super(EpsilonDominance, self).__init__()

        if hasattr(epsilons, "__getitem__"):
            self.epsilons = epsilons
        else:
            self.epsilons = [epsilons]

    def compare(self, p: list, q: list):
        """
        Eps Dominance comparator, the implementation based on Platypus.
        This operator works similarly like the normal, Dominance operator. However, it divides the current value with
        the epsilons and selects which dominates the other. If they are equal it selects those one, which is closer to
        the boundary.

        :param p: solution p
        :param q: solution q
        :return:
        """

        # first check constraint violation, the last item is the feasibility, which is a real number if its zero,
        # it means that the solution is feasible
        if p[-1] != q[-1]:
            if p[-1] == 0:
                return 1  # p dominates
            elif q[-1] == 0:
                return 2  # q is dominates, because it has smaller degree in constraint violation
            elif abs(p[-1]) < abs(q[-1]):
                return 1  # p is dominates
            elif abs(q[-1]) < abs(p[-1]):
                return 2  # q is dominates

        # then use epsilon dominance on the objectives
        dominate_p = False
        dominate_q = False

        for i, (p_costs, q_costs) in enumerate(zip(p[:-1], q[:-1])):

            epsilon = float(self.epsilons[i % len(self.epsilons)])

            p_eps = math.floor(p_costs / epsilon)
            q_eps = math.floor(q_costs / epsilon)

            if p_eps > q_eps:
                dominate_q = True
                if dominate_p:
                    return 0
            elif q_eps > p_eps:
                dominate_p = True
                if dominate_q:
                    return 0

        if not dominate_p and not dominate_q:
            dist1 = 0.0
            dist2 = 0.0

            for i, (p_costs, q_costs) in enumerate(zip(p[:-1], q[:-1])):
                epsilon = float(self.epsilons[i % len(self.epsilons)])

                i1 = math.floor(p_costs / epsilon)
                i2 = math.floor(q_costs / epsilon)

                dist1 += math.pow(p_costs - i1 * epsilon, 2.0)
                dist2 += math.pow(q_costs - i2 * epsilon, 2.0)

            if dist1 < dist2:
                return 1
            else:
                return 2
        elif dominate_p:
            return 1
        else:
            return 2

    def same_box(self, p, q):
        # if not dominate1 and not dominate2:
        if self.compare(p, q) == 0:
            return True
        else:
            return False


class ParetoDominance(Dominance):
    """Pareto dominance with constraints.

    If either solution violates constraints, then the solution with a smaller
    constraint violation is preferred. If both solutions are feasible, then
    Pareto dominance is used to select the preferred solution.
    """

    def __init__(self, epsilons=None):
        super(ParetoDominance, self).__init__()
        # self.signs = signs deprecated

    def compare(self, p: list, q: list):
        """
        Here, p and q are tuples, which contains the (feasibility index, cost vector)
        """
        # assert len(p) == len(q)

        # first check constraint violation, the last item is the feasibility, which is a real number if its zero,
        # it means that the solution is feasible
        if p[-1] != q[-1]:
            if p[-1] == 0:
                return 1  # p dominates
            elif q[-1] == 0:
                return 2  # q is dominates, because it has smaller degree in constraint violation
            elif abs(p[-1]) < abs(q[-1]):
                return 1  # p is dominates
            elif abs(q[-1]) < abs(p[-1]):
                return 2  # q is dominates

        dominate_p = False
        dominate_q = False

        for (p_costs, q_costs) in zip(p[:-1], q[:-1]):
            if p_costs > q_costs:
                dominate_q = True
                if dominate_p:
                    return 0
            elif q_costs > p_costs:
                dominate_p = True
                if dominate_q:
                    return 0

        if dominate_q == dominate_p:
            return 0
        elif dominate_p:
            return 1
        else:
            return 2


class Selector(Operator):

    def __init__(self, parameters, sign=None, part_num=2, dominance=ParetoDominance):
        """

        :param parameters:
        :param sign: one value from now, because its goal is to tell the direction of the optimum min or max
        :param part_num:
        :param dominance:
        """
        super().__init__()
        self.parameters = parameters
        self.comparator = dominance()  # ParetoDominance()
        self.signs = sign

    @abstractmethod
    def select(self, population):
        pass

    def pop_acceptance(self, individuals, individual):
        """
        This function differs from add() function that it preserves the length of the _content in the archive class.
        :return:
        """

        dominates = []
        dominated = False

        for i in range(len(individuals)):
            flag = self.dominance.compare(individual.costs_signed, individuals[i].costs_signed)

            if flag == 1:
                dominates.append(i)
            elif flag == 2:
                dominated = True

        if len(dominates) > 0:
            del individuals[random.choice(dominates)]
            individuals.append(individual)

        elif not dominated:
            individuals.remove(random.choice(individuals))
            individuals.append(individual)

        return

    def individual(self, polulation, id):
        for individual in polulation:
            if individual.id == id:
                return individual

        return None

    def fast_nondominated_sorting(self, population):
        pareto_front = [[]]
        front_number = 1

        # reset elements
        for p in population:
            p.features['domination_counter'] = 0
            p.features['front_number'] = None
            p.features['dominate'] = []

        for i, p in enumerate(population):
            for j in range(i + 1, len(population)):
                q = population[j]
                dom = self.comparator.compare(p.costs_signed, q.costs_signed)
                if dom == 1:
                    p.features['dominate'].append(q.id)
                    q.features['domination_counter'] += 1
                elif dom == 2:
                    p.features['domination_counter'] += 1
                    q.features['dominate'].append(p.id)

            # selects the pareto values
            if p.features['domination_counter'] == 0:
                p.features['front_number'] = front_number
                pareto_front[front_number - 1].append(p)

        while len(pareto_front[front_number - 1]) > 0:
            front_number += 1
            pareto_front.append([])
            for p in pareto_front[front_number - 2]:
                for individual_id in p.features['dominate']:
                    q = self.individual(population, individual_id)
                    q.features['domination_counter'] -= 1
                    if q.features['domination_counter'] == 0 and q.features['front_number'] is None:
                        q.features['front_number'] = front_number
                        pareto_front[front_number - 1].append(q)

        if len(pareto_front[front_number - 1]) == 0:
            pareto_front.pop()
        for sub_front in pareto_front:
            crowding_distance(sub_front)

        return


def crowding_distance(front):
    """
    Crowding distance calculates the solution density on a front, a subset of the population.
    :param front: list of individuals
                  which is a subset of the total population
    :return:
    """
    n = len(front)

    if n == 0:
        return
    elif n == 1:
        front[0].features['crowding_distance'] = math.inf
        return
    elif n == 2:
        front[0].features['crowding_distance'] = math.inf
        front[1].features['crowding_distance'] = math.inf
        return

    for i in range(len(front)):
        front[i].features['crowding_distance'] = 0.0

    for dim in range(len(front[0].costs_signed[:-1])):

        front.sort(key=lambda x: x.costs_signed[dim])
        # self.sort_by_coordinate(population, dim)

        front[0].features['crowding_distance'] = math.inf
        front[-1].features['crowding_distance'] = math.inf
        max_distance = front[-1].costs_signed[dim] - front[0].costs_signed[dim]
        for i in range(1, n - 1):
            distance = front[i + 1].costs_signed[dim] - front[i - 1].costs_signed[dim]
            if max_distance > 0.0:
                front[i].features['crowding_distance'] += distance / max_distance
    return


def nondominated_truncate(population, size):
    """Truncates a population to the given size, using non-dominated sorting.
    The resulting population is filled with the first N-1 fronts.
    The Nth front is too large and must be split using crowding distance.

    Parameters
    ----------
    :population : iterable
        The collection of solutions that have been non-domination sorted
    :size:
        The size of the truncated result
    """

    # calculating the crowding distance on the different fronts
    population = list(set(population))
    result = sorted(population, key=functools.cmp_to_key(nondominated_cmp))
    return result[:size]


def nondominated_cmp(p, q):
    """
    From the 'front_number' the smaller value is favourized.
    From the 'crowding_distance' the higher values are favoured.
    :param p: Individual
    :param q: Individual
    :return: -1 if x dominates
              0 if they are equals
              1 if y dominates
    """
    if p.features['front_number'] == q.features['front_number']:
        if -p.features['crowding_distance'] < -q.features['crowding_distance']:
            return -1
        elif -p.features['crowding_distance'] > -q.features['crowding_distance']:
            return 1
        else:
            return 0
    else:
        if p.features['front_number'] < q.features['front_number']:
            return -1
        elif p.features['front_number'] > q.features['front_number']:
            return 1
        else:
            return 0


class DummySelector(Selector):
    def __init__(self, parameters):
        super().__init__(parameters)

    def select(self, individuals):
        return individuals


class CopySelector(Selector):
    def __init__(self, parameters):
        super().__init__(parameters)

    def select(self, individuals):
        selection = []
        for individual in individuals:
            candidate = Individual(individual.vector)
            candidate.costs = deepcopy(individual.costs)
            candidate.features = deepcopy(individual.features)
            candidate.population_id = -1
            selection.append(candidate)
        return selection


class TournamentSelector(Selector):
    def __init__(self, parameters, dominance=ParetoDominance, epsilons=None):
        super().__init__(parameters)
        self.dominance = dominance(epsilons=epsilons)

    def select(self, individuals):
        """
        Binary tournament selection:

        2 individuals are selected from the given population (randomly), then the function gaves
        back the dominant (or random).
        """

        if len(individuals) == 1:
            selected = individuals[0]
        else:
            # Sampling two individuals without a replacement
            candidates = random.sample(individuals, 2)

            # they should have this at this stage
            if candidates[0].features['front_number'] < candidates[1].features['front_number']:
                return candidates[0]
            elif candidates[1].features['front_number'] < candidates[0].features['front_number']:
                return candidates[1]

            flag = self.dominance.compare(candidates[0].costs_signed, candidates[1].costs_signed)

            if flag == 1:
                selected = candidates[0]
            elif flag == 2:
                selected = candidates[1]
            else:
                selected = random.choice(candidates)

        return selected


class FireflyStep(Operator):
    """
      This operator makes the following
      ---------------------------------

      - calculates the distance between two points, because its correlates with that value.
      - the brightness of the other point
      - the mutator constant, which contains a damping factor [2]?

      The k+1 th position of the j(th) individual is calculated by the following formula
      ---------------------------------------------------------------------------

          L = ub-lb
          b=1;               # Attraction Coefficient Base Value, if beta = 0, it becamos a random walk
          a=0.01*L;              # Mutation Coefficient
          ad=0.9;            # Mutation Coefficient Damping Ratio -- decreases the initial value of a after each, as same as in simulated annealing
                                iteration step
          gamma = 0.5/L^2          # light absorbtion coefficient


          x(j,k+1) = x(j,k) + b0*exp(-gamma*r^2) + sum_{i<j}[x(j,k) - x(i,k)] + a*(rand[0,1] - 0.5)

      [1] Yang, Xin-She. "Firefly algorithms for multimodal optimization." International symposium on stochastic algorithms.
          Springer, Berlin, Heidelberg, 2009.

      [2]: Yang, X. S. (2013). Multiobjective firefly algorithm for continuous optimization.
              Engineering with computers, 29(2), 175-184.
    """

    def __init__(self, parameters, alpha = 0.01, beta = 1.0, gamma = 0.5, damping = 0.9, dominance=ParetoDominance()):
        super().__init__()
        self.parameters = parameters
        self.dominance = dominance
        self.b = beta
        self.a = alpha
        self.gamma = gamma
        self.damping_factor = damping

    def attraction_step(self, current, other, iteration_nr):
        # refresh the position of the offspring if its more attractive
        # if it's dominant returns without changing its position
        if self.dominance.compare(current.costs_signed, other.costs_signed) == 1:
            return
        else:
            for i, param in enumerate(self.parameters):
                lb = param['bounds'][0]
                ub = param['bounds'][1]

                L = (ub-lb)
                Gamma = L*self.gamma
                alpha = self.a*L*0.9**iteration_nr

                # elementary distance of the particle, random walk
                e = random.random() * (ub - lb)
                # distance between the two individuals
                r2 = current.vector[i] ** 2. + other.vector[i] ** 2.
                vel_attraction = self.b * exp(-Gamma * r2 ** 2.) * (other.vector[i] - current.vector[i])

                v_rd = alpha * (random.random() - 0.5) * e
                # position i+1
                current.vector[i] += vel_attraction + v_rd
                current.vector[i] = self.clip(current.vector[i], lb, ub)
        return


class Crossover(Operator):

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

        offspring_a = Individual(parent_a, p1.features)
        offspring_b = Individual(parent_b, p2.features)

        return offspring_a, offspring_b


class SimulatedBinaryCrossover(Crossover):

    def __init__(self, parameters, probability, distribution_index=15):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index
        if distribution_index < 0:
            raise Exception('The distribution index have to be positive.')
        if probability > 1.:
            raise Exception('The probability should be selected from [0,1].')
        elif probability < 0.:
            raise Exception('The probability should be selected from [0,1].')

    def cross(self, p1, p2):
        """
        Create an offspring using simulated binary crossover.
        :return:  Individual, Individual

        a list with 2 offsprings each with the genotype of an  offspring after recombination and mutation.
        """

        x1 = deepcopy(p1.vector)
        x2 = deepcopy(p2.vector)

        if random.random() <= self.probability:
            for i, param in enumerate(self.parameters):

                if random.random() <= 0.5:

                    if abs(x2[i] - x1[i]) > EPSILON:
                        if x2[i] > x1[i]:
                            y1, y2 = x1[i], x2[i]
                        else:
                            y1, y2 = x2[i], x1[i]

                        lb, ub = param['bounds'][0], param['bounds'][1]

                        # calculates c1
                        beta = 1.0 + (2.0 * (y1 - lb) / (y2 - y1))
                        alpha = 2.0 - pow(beta, -(self.distribution_index + 1.0))

                        rand = random.random()
                        if rand <= (1.0 / alpha):
                            betaq = pow(rand * alpha, (1.0 / (self.distribution_index + 1.0)))
                        else:
                            betaq = pow(1.0 / (2.0 - rand * alpha), 1.0 / (self.distribution_index + 1.0))

                        c1 = 0.5 * (y1 + y2 - betaq * (y2 - y1))

                        # calculates c2
                        beta = 1.0 + (2.0 * (ub - y2) / (y2 - y1))
                        alpha = 2.0 - pow(beta, -(self.distribution_index + 1.0))

                        if rand <= (1.0 / alpha):
                            betaq = pow((rand * alpha), (1.0 / (self.distribution_index + 1.0)))
                        else:
                            betaq = pow(1.0 / (2.0 - rand * alpha), 1.0 / (self.distribution_index + 1.0))

                        c2 = 0.5 * (y1 + y2 + betaq * (y2 - y1))

                        # check the boundaries
                        c1 = self.clip(c1, lb, ub)
                        c2 = self.clip(c2, lb, ub)

                        if random.random() <= 0.5:
                            x1[i], x2[i] = c2, c1
                        else:
                            x1[i], x2[i] = c1, c2

        return Individual(x1, p1.features), Individual(x2, p2.features)
