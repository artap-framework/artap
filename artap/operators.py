from abc import abstractmethod, ABC
import sys
import random
import math
import itertools

from .individual import Individual
from .utils import VectorAndNumbers
from .doe import build_box_behnken, build_lhs, build_full_fact, build_plackett_burman

EPSILON = sys.float_info.epsilon


class Operation(ABC):

    def __init__(self):
        pass

    @staticmethod
    def clip(value, min_value, max_value):
        return max(min_value, min(value, max_value))


class Generation(Operation):

    def __init__(self, problem=None, individual_class=Individual, parameters=None):
        super().__init__()
        if problem is not None:
            self.parameters = problem.parameters
        else:
            self.parameters = parameters
        self.individual_class = individual_class

    def create_individual(self, vector: list=[]):
        return self.individual_class(vector)

    @abstractmethod
    def generate(self):
        pass


class CustomGeneration(Generation):

    def __init__(self, problem=None):
        super().__init__(problem)
        self.vectors = []

    def init(self, vectors):
        self.vectors = vectors

    def generate(self):
        individuals = []
        for vector in self.vectors:
            individuals.append(self.create_individual(vector))
        return individuals


class RandomGeneration(Generation):

    def __init__(self, problem=None, individual_class=Individual, parameters=None):
        super().__init__(problem, individual_class, parameters=parameters)
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

    def __init__(self, problem=None, parameters=None):
        super().__init__(problem, parameters=parameters)
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

    def __init__(self, problem=None, parameters=None):
        super().__init__(problem, parameters=parameters)

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

    def __init__(self, problem=None, parameters=None):
        super().__init__(problem, parameters=parameters)

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

    def __init__(self, problem=None, parameters=None):
        super().__init__(problem, parameters=parameters)
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

    def __init__(self, problem=None, parameters=None):
        super().__init__(parameters=parameters)
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

    def bitflip(self, x:list):

        for j in range(1,len(x)):
            if random.uniform(0.0, 1.0) <= self.probability:
                x[j] = not x[j]

        return x


class SwarmMutation(Mutation):

    def __init__(self, parameters, probability=1):
        super().__init__(parameters, probability)
        self.w = 0.1  # constant inertia weight (how much to weigh the previous velocity)
        self.c1 = 2  # cognitive constant
        self.c2 = 1  # social constant
        self.best_individual = None

    # evaluate current fitness
    def evaluate_pso(self, individual):

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


class Selection(Operation):

    def __init__(self, parameters, signs, part_num=2):
        super().__init__()
        self.parameters = parameters
        self.signs = signs
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
                if self.comparator.compare(p, q) == 1:          # TODO: simplify
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

    def __init__(self, epsilons, signs=None):
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

    def __init__(self, signs, epsilons=None):
        super(ParetoDominance, self).__init__()
        self.signs = signs

    def compare(self, p, q):
        if len(p.costs) != len(q.costs):
            print("Len {} - {}".format(len(p.costs), len(p.costs)))
        # first check constraint violation
        if p.feasible != q.feasible:
            if p.feasible == 0:
                return 1
            elif q.feasible == 0:
                return 2
            elif p.feasible < q.feasible:
                return 1
            elif q.feasible < p.feasible:
                return 2

        # The cost function can be a float or a list of floats
        # Check the pareto dominance on every value of the calculated vectors
        dominate_p = False
        dominate_q = False
        for i in range(0, len(p.costs)):
            sign = self.signs[i]
            if sign * p.costs[i] > sign * q.costs[i]:
                dominate_q = True

                if dominate_p:
                    return 0

            if sign * p.costs[i] < sign * q.costs[i]:
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

    def __init__(self, parameters, signs=None, part_num=2, dominance=ParetoDominance):
        super().__init__()
        self.parameters = parameters
        self.part_num = part_num
        self.comparator = dominance(signs=signs)  # ParetoDominance()
        self.signs = signs

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
                if self.comparator.compare(p, q) == 1:          # TODO: simplify
                    p.dominate.add(q)
                    p.dominate.add(q)
                elif self.comparator.compare(q, p) == 1:
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

    def __init__(self, parameters, signs, part_num=2):
        super().__init__(parameters, signs, part_num)

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

    def __init__(self, parameters, signs=None, dominance=ParetoDominance, epsilons=None):
        super().__init__(parameters, signs=signs)
        self.dominance = dominance(signs=signs, epsilons=epsilons)
        self.signs = signs
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
            flag = self.dominance.compare(winner, candidate)

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
