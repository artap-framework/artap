from abc import *

from random import uniform

class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """

    def __init__(self, vector: list):
        self.vector = vector.copy()
        self.costs = []
        self.is_evaluated = False

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
        string += "]"

        return string

    def sync(self, individual):
        self.vector = individual.vector
        self.costs = individual.costs
        self.is_evaluated = individual.is_evaluated

    # deprecated
    # def to_list(self):
    #     params = [self.vector, self.costs]
    #     # flatten list
    #     out = [val for sublist in params for val in sublist]
    #     # front_number
    #     if self.front_number is None:
    #         out.append(0)
    #     else:
    #         out.append(self.front_number)
    #     # crowding_distance
    #     if self.crowding_distance is None:
    #         out.append(0)
    #     else:
    #         out.append(self.crowding_distance)
    #     # feasible
    #     if self.feasible is None:
    #         out.append(0)
    #     else:
    #         out.append(self.feasible)
    #     if self.depends_on is None:
    #         out.append(-1)
    #     else:
    #         out.append(self.depends_on)
    #     out.append(self.modified_param)
    #     # dominates
    #     dominates = []
    #     out.append(dominates)
    #     # gradient
    #     out.append(self.gradient)
    #     return out

class GeneticIndividual(Individual):
    def __init__(self, vector: list):
        super().__init__(vector)

        self.gradient = []
        self.feasible = 0.0  # the distance from the feasibility region in min norm
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

        for i in range(0, len(self.vector)):
            self.velocity_i.append(uniform(-1, 1))

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """

        string = "{}, ".format(super().__repr__())

        string += ", front number: {}".format(self.front_number)
        string += ", crowding distance: {}".format(self.crowding_distance)
        string += ", gradient: ["
        for i, number in enumerate(self.gradient):
            string += str(number)
            if i < len(self.vector)-1:
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
