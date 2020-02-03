from abc import *
from random import uniform
from enum import Enum
# from numpy import  asarray, float64, append
from copy import deepcopy


class Individual(metaclass=ABCMeta):
    """ Collects information about one point in design space. """

    class State(Enum):
        EMPTY = 0
        EVALUATED = 1
        FAILED = 2

    def __init__(self, vector: list):
        self.vector = vector.copy()
        self.costs = []
        self.state = self.State.EMPTY

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """

        string = "vector: ["
        for i, number in enumerate(self.vector):
            string += str(number)
            if i < len(self.vector) - 1:
                string += ", "
        string = string[:len(string) - 1]
        string += "]"

        string += "; costs:["
        for i, number in enumerate(self.costs):
            string += str(number)
            if i < len(self.costs) - 1:
                string += ", "
        string += "]"

        return string

    def __eq__(self, other):
        return self.vector == other.vector and self.costs == self.costs

    def __hash__(self):
        return id(self)

    def sync(self, individual):
        self.vector = individual.vector
        self.costs = individual.costs
        self.state = individual.state


class GeneticIndividual(Individual):
    def __init__(self, vector: list):
        super().__init__(vector)

        self.gradient = []
        self.feasible = 0.0  # the distance from the feasibility region in min norm, its an index, not a
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = None  # TODO: make better
        self.crowding_distance = 0  # TODO: deprecated? --
        self.depends_on = None  # For calculating gradients
        self.modified_param = -1
        # For particle swarm optimization
        self.velocity_i = [0] * len(vector)  # particle velocity
        self.best_parameters = []  # best position individual
        self.best_costs = []  # best error individual

        # transformed data, like a cache for the signed values of the calculation results in ndarray
        self.signed_costs = []

        for i in range(0, len(self.vector)):
            self.velocity_i.append(uniform(-1, 1))

    def transform_data(self, signs):
        """
        Tha aim of this function is to transform the data into a numpy array, which can make a faster
        comparison during the sorting of the data.

        :param signs: this is the list of the signs of every value, which shows that the minimum or the maximum
        of the values are calculated. This list is stored in the Problem class

        :return: nothing but calculates np array from the data
        """

        # svec = asarray(signs,dtype=float64)
        # cvec = asarray(self.costs, dtype=float64)

        # self.signed_costs = svec*cvec
        # self.signed_costs = append(self.signed_costs, self.feasible)

        self.signed_costs = list(map(lambda x, y: x * y, signs, self.costs))
        self.signed_costs.append(self.feasible)
        return

    def weighted_cost(self, weights):
        """
        Calculates a single best solution

        :param weights:
        :return:
        """

        return

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """

        string = "{}, ".format(super().__repr__())

        string += ", front number: {}".format(self.front_number)
        string += ", crowding distance: {}".format(self.crowding_distance)
        string += ", gradient: ["
        for i, number in enumerate(self.gradient):
            string += str(number)
            if i < len(self.vector) - 1:
                string += ", "
        string = string[:len(string) - 1]
        string += "]"

        return string

    def sync(self, individual):
        super().sync(individual)

        self.gradient = individual.gradient
        self.feasible = individual.feasible
        self.dominate = individual.dominate
        self.domination_counter = individual.domination_counter
        self.front_number = individual.front_number
        self.crowding_distance = individual.crowding_distance
        self.depends_on = individual.depends_on
        self.modified_param = individual.modified_param
        # For particle swarm optimization
        self.velocity_i = individual.velocity_i
        self.best_parameters = individual.best_parameters
        self.best_costs = individual.best_costs
