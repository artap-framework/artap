from _ast import Dict
from abc import abstractmethod, ABC
from copy import deepcopy
import sys
import random
import math

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

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters

    @abstractmethod
    def generate(self, number):
        pass


class RandomGeneration(Generation):

    def __init__(self, parameters):
        super().__init__(parameters)

    def generate(self, number):
        individuals = []
        for i in range(number):
            vector = VectorAndNumbers.gen_vector(self.parameters)
            individuals.append(Individual(vector))
        return individuals


class Mutation(Operator):

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

        for i, parameter in enumerate(self.parameters.items()):
            if random.uniform(0, 1) < self.probability:
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

    def __init__(self, parameters, probability, distribution_index=20):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index

    def mutate(self, p):
        vector = []

        for i, parameter in enumerate(self.parameters.items()):
            if random.uniform(0, 1) < self.probability:
                l_b = parameter[1]['bounds'][0]
                u_b = parameter[1]['bounds'][1]

                vector.append(self.pm_mutation(p.vector[i], l_b, u_b))
            else:
                vector.append(p.vector[i])

        p_new = Individual(vector)
        return p_new

    def pm_mutation(self, x, lb, ub):
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


class Selection(Operator):

    def __init__(self, parameters, part_num=2):
        super().__init__()
        self.parameters = parameters
        self.part_num = part_num

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
            if p.costs[i] < q.costs[i]:
                dominate = True
        return dominate

    def non_dominated_sort(self, population):
        pareto_front = []
        front_number = 1

        for p in population:
            for q in population:
                if p is q:
                    continue
                if self.is_dominate(p, q):
                    p.dominate.add(q)
                elif self.is_dominate(q, p):
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
                    if q.domination_counter == 0 and q.front_number == 0:
                        q.front_number = front_number
                        temp_set.append(q)
            pareto_front = temp_set

    def sort_by_coordinate(self, population, dim):
        population.sort(key=lambda x: x.vector[dim])
        return population

    def crowding_distance(self, population):
        infinite = float("inf")
        n = len(population[0].vector)
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


class Dominance(ABC):
    def __init__(self):
        pass

    def compare(self, p, q):
        raise NotImplementedError("method not implemented")


class EpsilonDominance(Dominance):

    def __init__(self, epsilons):
        super().__init__()
        self.epsilons = epsilons

    def same_box(self, ind1, ind2):

        # first check constraint violation
        if ind1.feasible != ind2.feasible:
            if ind1.feasible == 0:
                return False
            elif ind2.feasible == 0:
                return False
            elif ind1.feasible < ind2.feasible:
                return False
            elif ind2.feasible < ind1.feasible:
                return False

        # then use epsilon dominance on the objectives
        dominate1 = False
        dominate2 = False

        for i in range(len(ind1.costs)):
            o1 = ind1.costs[i]
            o2 = ind2.costs[i]

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

    def compare(self, ind1, ind2):

        # first check constraint violation
        if ind1.feasible != ind2.feasible:
            if ind1.feasible == 0:
                return 2
            elif ind2.feasible == 0:
                return 1
            elif ind1.feasible < ind2.feasible:
                return 2
            elif ind2.feasible < ind1.feasible:
                return 1

        # then use epsilon dominance on the objectives
        dominate1 = False
        dominate2 = False

        for i in range(len(ind1.costs)):
            o1 = ind1.costs[i]
            o2 = ind2.costs[i]

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

            for i in range(len(ind1.costs)):
                o1 = ind1.costs[i]
                o2 = ind2.costs[i]

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

    def __init__(self):
        super(ParetoDominance, self).__init__()

    def compare(self, p, q):
        # First check the constraint violations
        if p.feasible != 0.0:
            if q.feasible != 0.0:
                if abs(p.feasible) < abs(q.feasible):
                    return 1
                else:
                    return 2
            else:
                return 2
        else:
            if q.feasible != 0.0:
                return 1

        # Then the pareto dominance

        dominate_p = False
        dominate_q = False

        # The cost function can be a float or a list of floats
        for i in range(0, len(p.costs)):
            if p.costs[i] > q.costs[i]:
                dominate_q = True

                if dominate_p:
                    return 0
            if p.costs[i] < q.costs[i]:
                dominate_p = True

                if dominate_q:
                    return 0

        if dominate_q == dominate_p:
            return 0
        elif dominate_p:
            return 1
        else:
            return 2


class TournamentSelection(Selection):

    def __init__(self, parameters, dominance=ParetoDominance()):
        super().__init__(parameters)
        self.dominance = dominance
        # self.dominance = EpsilonDominance([0.01])

    def select(self, population):
        """
        Binary tournament selection:
        An individual is selected in the rank is lesser than the other or if crowding distance is greater than the other
        """

        winner = random.choice(population)

        for _ in range(self.part_num - 1):
            candidate = random.choice(population)
            flag = self.dominance.compare(winner, candidate)

            if flag > 0:
                winner = candidate

        return winner

        # participants = random.sample(parents, part_num)
        # return min(participants, key=lambda x: (x.front_number, -x.crowding_distance))


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
        parent_a = deepcopy(p1.vector)
        parent_b = deepcopy(p2.vector)

        if random.uniform(0.0, 1.0) <= self.probability:
            parameter1 = []
            parameter2 = []
            linear_range = 2

            alpha = random.uniform(0, linear_range)

            for i, param in enumerate(self.parameters.items()):
                l_b = param[1]['bounds'][0]
                u_b = param[1]['bounds'][1]

                parameter1.append(self.clip(alpha * p1.vector[i] + (1 - alpha) * p2.vector[i], l_b, u_b))
                parameter2.append(self.clip((1 - alpha) * p1.vector[i] + alpha * p2.vector[i], l_b, u_b))

            parent_a = parameter1
            parent_b = parameter2

        offspring_a = Individual(parent_a)
        offspring_b = Individual(parent_b)

        return offspring_a, offspring_b


class SimulatedBinaryCrossover(Crossover):

    def __init__(self, parameters, probability, distribution_index=5):
        super().__init__(parameters, probability)
        self.distribution_index = distribution_index

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
        """Create an offspring using simulated binary crossover.

        :return:  a list with 2 offsprings each with the genotype of an  offspring after recombination and mutation.
        """

        parent_a = deepcopy(p1.vector)
        parent_b = deepcopy(p2.vector)

        if random.uniform(0.0, 1.0) <= self.probability:
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

        return offspring_a, offspring_b
