from random import uniform
from abc import *


class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """

    def __init__(self, vector: list):
        self.vector = vector.copy()
        self.costs = []
        self.gradient = []

        self.feasible = 0.0  # the distance from the feasibility region in min norm
        self.is_evaluated = False
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = None  # TODO: make better
        self.crowding_distance = 0  # TODO: deprecated? --

        # For particle swarm optimization
        self.velocity_i = [0]*len(vector)  # particle velocity
        self.best_parameters = []  # best position individual
        self.best_costs = []  # best error individual

        for i in range(0, len(self.vector)):
            self.velocity_i.append(uniform(-1, 1))

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """
        string = "vector: ["

        for i, number in enumerate(self.vector):
            string += str(number)
            if i < len(self.vector)-1:
                string += ", "

        string = string[:len(string) - 1]
        string += "]"
        string += "; costs:["

        for i, number in enumerate(self.costs):
            string += str(number)
            if i < len(self.costs)-1:
                string += ", "
        string += "],"
        string += " front number: {}".format(self.front_number)
        string += " crowding distance: {}".format(self.crowding_distance)
        return string

    def to_list(self):
        params = [self.vector, self.costs]
        # flatten list
        out = [val for sublist in params for val in sublist]
        # front_number
        if self.front_number is None:
            out.append(0)
        else:
            out.append(self.front_number)
        # crowding_distance
        if self.crowding_distance is None:
            out.append(0)
        else:
            out.append(self.crowding_distance)
        # feasible
        if self.feasible is None:
            out.append(0)
        else:
            out.append(self.feasible)
        # dominates
        dominates = []
        out.append(dominates)
        # gradient
        out.append(self.gradient)

        return out
