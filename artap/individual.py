from abc import *
from collections.abc import Iterable
from enum import Enum


class Individual(metaclass=ABCMeta):
    """ Collects information about one point in design space. """

    class State(Enum):
        EMPTY = 0
        IN_PROGRESS = 1
        EVALUATED = 2
        FAILED = 3

    @classmethod
    def to_string(cls, state):
        if state == cls.State.EMPTY:
            return 'empty'
        if state == cls.State.IN_PROGRESS:
            return 'in_progress'
        if state == cls.State.EVALUATED:
            return 'evaluated'
        if state == cls.State.FAILED:
            return 'failed'

    counter: int = 0

    def __init__(self, vector: list = [], features=dict()):
        self.id = Individual.counter
        Individual.counter += 1

        self.vector = vector.copy()
        self.costs = []
        self.costs_signed = []
        self.state = self.State.EMPTY
        self.population_id = -1
        self.algorithm_id = 0

        self.parents = []
        self.children = []

        self.features = dict()
        self.features["start_time"] = 0.0
        self.features["finish_time"] = 0.0
        self.features["feasible"] = 0.0   # the distance from the feasibility region in min norm, its an index, not a
        self.features["precision"] = 7   # the default value of the considered decimals
        for key, value in features.items():
            if not key in self.features:
                self.features[key] = value

        self.custom = {}

    def calc_signed_costs(self, p_signs):
        """
        This function calculates the signed costs for every vector and insert the feasibility after
        :return:
        """
        self.costs_signed = list(map(lambda x, y: x * round(y, ndigits=self.features["precision"]), p_signs, self.costs))
        self.costs_signed.append(self.features["feasible"])

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
            for key, value in self.custom.items():
                string += "'{}': {}".format(key, value)
                if i < len(self.custom) - 1:
                    string += ", "
            string += "]"

        if len(self.features) > 0:
            string += "; features:["
            for key, value in self.features.items():
                string += "'{}': {}".format(key, value)
                if i < len(self.features) - 1:
                    string += ", "
            string += "]"

        # string += "; state: '{}', ".format(Individual.State.to_string(self.state))
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
        self.state = individual.state
        self.population_id = individual.population_id
        self.algorithm_id = individual.algorithm_id

        self.parents = individual.parents
        self.children = individual.children

        self.features = individual.features

        self.custom = individual.custom

    def to_dict(self):
        output = {'id': self.id,
                  'vector': list(self.vector),
                  'costs': list(self.costs),
                  'costs_signed': self.costs_signed,
                  'state': self.to_string(self.state),
                  'population_id': self.population_id,
                  'algorithm_id': self.algorithm_id,
                  'custom': self.custom,
                  'features': self.features}

        parents = []
        for parent in self.parents:
            parents.append(self._replace_individual_id(parent))
        output['parents'] = parents

        children = []
        for child in self.children:
            children.append(self._replace_individual_id(child))
        output['children'] = children

        features = dict()
        for key, value in self.features.items():
            features[key] = self._replace_individual_id(value)
        output['features'] = features

        return output

    def _replace_individual_id(self, value):
        if isinstance(value, Iterable):
            val = []
            for item in value:
                val.append(self._replace_individual_id(item))
            return val
        elif isinstance(value, Individual):
            return value.id
        else:
            return value

    @staticmethod
    def from_dict(dictionary):
        individual = Individual()
        individual.id = dictionary['id']

        individual.vector = dictionary['vector']
        individual.costs = dictionary['costs']
        individual.state = dictionary['state']
        individual.costs_signed = dictionary['costs_signed']
        individual.population_id = dictionary['population_id']
        individual.algorithm_id = dictionary['algorithm_id']

        individual.custom = dictionary['custom']
        individual.features = dictionary['features']

        # for feature in individual.features.items():
        #     key = 'feature_' + feature[0]
        #     if isinstance(feature[1], Iterable):
        #         value = []
        #         for item in feature[1]:
        #             if isinstance(item, Individual):
        #                 value.append(item.id)
        #             else:
        #                 value.append(item)
        #     else:
        #         value = feature[1]

        return individual

