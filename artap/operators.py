from _ast import Dict
from abc import abstractmethod, ABC
from copy import deepcopy
import sys
import random

from .individual import Individual
from .utils import VectorAndNumbers

EPSILON = sys.float_info.epsilon


class Operator(ABC):

    def __init__(self):
        pass

    @staticmethod
    def clip(value, min_value, max_value):
        return max(min_value, min(value, max_value))


class Generation(Operator):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def generate(self, number, parameters):
        pass


class RandomGeneration(Generation):

    def __init__(self):
        super().__init__()

    def generate(self, number, parameters):
        individuals = []
        for i in range(number):
            vector = VectorAndNumbers.gen_vector(parameters)
            individuals.append(Individual(vector))
        return individuals


class Mutation(Operator):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def mutate(self, parameters, p):
        pass


class SimpleMutation(Mutation):
    def __init__(self, prob_mutation):
        super().__init__()
        self.prob_mutation = prob_mutation

    def mutate(self, parameters, p):
        """ uniform random mutation """
        mutation_space = 0.1
        vector = []

        for i, parameter in enumerate(parameters.items()):
            if random.uniform(0, 1) < self.prob_mutation:

                l_b = parameter[1]['bounds'][0]
                u_b = parameter[1]['bounds'][1]

                para_range = mutation_space * (u_b - l_b)
                mutation = random.uniform(-para_range, para_range)
                vector.append(self.clip(p.vector[i] + mutation, l_b, u_b))
            else:
                vector.append(p.vector[i])

        p_new = Individual(vector)
        return p_new


class PmMutation(Mutation):

    def __init__(self, mutation_index=5):
        super().__init__()
        self.mutation_index = mutation_index

    def run(self, x, lb, ub):
        u = random.uniform(0, 1)
        dx = ub - lb

        if u < 0.5:
            bl = (x - lb) / dx
            b = 2.0 * u + (1.0 - 2.0 * u) * pow(1.0 - bl,  self.mutation_index + 1.0)
            delta = pow(b, 1.0 / (self.mutation_index + 1.0)) - 1.0
        else:
            bu = (ub - x) / dx
            b = 2.0 * (1.0 - u) + 2.0 * (u - 0.5) * pow(1.0 - bu, self.mutation_index + 1.0)
            delta = 1.0 - pow(b, 1.0 / (self.mutation_index + 1.0))

        x = x + delta * dx
        x = PmMutation.clip(x, lb, ub)

        return x


class Selection(Operator):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def select(self, parents, part_num=2):
        pass


class TournamentSelection(Selection):

    def __init__(self):
        super().__init__()

    def select(self, parents, part_num=2):
        """
        Binary tournament selection:
        An individual is selected in the rank is lesser than the other or if crowding distance is greater than the other
        """

        participants = random.sample(parents, part_num)
        return min(participants, key=lambda x: (x.front_number, -x.crowding_distance))


class Crossover(Operator):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def cross(self, parameters, p1, p2):
        pass


class SimpleCrossover(Crossover):

    def __init__(self, prob_cross):
        super().__init__()
        self.prob_cross = prob_cross

    def cross(self, parameters, p1, p2):
        """ the random linear operator """
        if random.uniform(0, 1) >= self.prob_cross:
            return p1, p2

        parameter1, parameter2 = [], []
        linear_range = 2

        alpha = random.uniform(0, linear_range)

        for i, param in enumerate(parameters.items()):
            l_b = param[1]['bounds'][0]
            u_b = param[1]['bounds'][1]

            parameter1.append(self.clip(alpha * p1.vector[i] + (1 - alpha) * p2.vector[i], l_b, u_b))
            parameter2.append(self.clip((1 - alpha) * p1.vector[i] + alpha * p2.vector[i], l_b, u_b))

        c1 = Individual(parameter1)
        c2 = Individual(parameter2)
        return c1, c2


class SimulatedBinaryCrossover(Crossover):

    def __init__(self, parameters: Dict,  distribution_index=5):
        super().__init__()
        self.distribution_index = distribution_index
        self.parameters = parameters

    def sbx(self, x1, x2, lb, ub):
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

        return x1, x2

    def cross(self, p1, p2):
        pass

    def run(self, individuals):
        """Create an offspring using simulated binary crossover.

        :parameter individuals: - list of individuals from the population, each a vector of genes.
        :return:  a list with 2 offsprings each with the genotype of an  offspring after recombination and mutation.
        """

        parent_a = deepcopy(individuals[0].vector)
        parent_b = deepcopy(individuals[1].vector)

        if random.uniform(0.0, 1.0) <= self.distribution_index:
            for i, param in enumerate(self.parameters.items()):
                x1 = parent_a[i]
                x2 = parent_b[i]

                lb = param[1]['bounds'][0]
                ub = param[1]['bounds'][1]

                x1, x2 = self.sbx(x1, x2, lb, ub)

                parent_a[i] = x1
                parent_b[i] = x2

        offspring_a = Individual(parent_a)
        offspring_b = Individual(parent_b)

        return [offspring_a, offspring_b]
