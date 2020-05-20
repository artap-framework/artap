import platform
from abc import *
from enum import Enum
from random import uniform


class Individual(metaclass=ABCMeta):
    """ Collects information about one point in design space. """

    class State(Enum):
        EMPTY = 0
        IN_PROGRESS = 1
        EVALUATED = 2
        FAILED = 3

        @staticmethod
        def to_string(state):
            if state == Individual.State.EMPTY:
                return "Individual is empty."
            elif state == Individual.State.IN_PROGRESS:
                return "Individual is in progress."
            elif state == Individual.State.EVALUATED:
                return "Individual is evaluated."
            elif state == Individual.State.FAILED:
                return "Individual evaluation failed."

    def __init__(self, vector: list):
        self.vector = vector.copy()
        self.costs = []
        self.costs_signed = []
        self.state = self.State.EMPTY
        self.parents = []
        self.children = []
        self.features = {}
        self.custom = {}
        self.feasible = 0.0  # the distance from the feasibility region in min norm, its an index, not a
        self.precision = 7   # the default value of the considered decimals

        self.info = {"start_time": 0.0,
                     "finish_time": 0.0,
                     "population": -1,
                     "processor": platform.processor(),
                     "system": platform.system(),
                     "python": platform.python_version(),
                     "hostname": platform.node()}

    def calc_signed_costs(self, p_signs):
        """
        This function calculates the signed costs for every vector and insert the feasibility after
        :return:
        """
        self.costs_signed = list(map(lambda x, y: x * round(y, ndigits=self.precision), p_signs, self.costs))
        self.costs_signed.append(self.feasible)

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

        if len(self.custom) > 0:
            string += "; custom:["
            for i, number in enumerate(self.custom):
                string += str(number)
                if i < len(self.custom) - 1:
                    string += ", "
            string += "]"

        string += "; state: '{}', ".format(Individual.State.to_string(self.state))
        # string += "; info: {}, ".format(self.info)

        return string

    def __eq__(self, other):

        if self.costs_signed == []:
            diff = set(self.vector) - set(other.vector)
            return diff == set()
        else:
            diff = set(self.costs_signed) - set(other.costs_signed)
            return  diff == set()

    def __hash__(self):
        #return id(self)
        return hash(tuple(self.vector))

    def sync(self, individual):
        self.vector = individual.vector
        self.costs = individual.costs
        self.costs_signed = individual.costs_signed
        self.custom = individual.custom
        self.state = individual.state
        self.info = individual.info
