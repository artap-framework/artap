from random import uniform
from abc import *
from .utils import VectorAndNumbers


class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """
    id = 0
    results = None
    gradients = None

    def __init__(self, vector, population_id=0):
        # self.vector = design_parameters.copy()
        self.vector = vector
        self.costs = []
        self.id = Individual.id
        self.gradient = []
        Individual.id += 1

        self.feasible = 0.0  # the distance from the feasibility region in min norm
        self.population_id = population_id
        self.is_evaluated = False
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = 0
        self.crowding_distance = 0

        # For particle swarm optimization
        self.velocity_i = []  # particle velocity
        self.best_parameters = []  # best position individual
        self.best_costs = []  # best error individual

        for i in range(0, len(self.vector)):
            self.velocity_i.append(uniform(-1, 1))

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """
        string = "vector: ["

        for i, number in enumerate(self.vector):
            string += str(number)
            if i < len(self.costs)-1:
                string += ", "

        string = string[:len(string) - 1]
        string += "]"
        string += "; costs:["
        for i, number in enumerate(self.costs):
            string += str(number)
            if i < len(self.costs)-1:
                string += ", "
        string += "]\n"
        return string

    def to_list(self):
        params = [[self.id], [self.population_id], self.vector, self.costs]
        # flatten list
        out = [val for sublist in params for val in sublist]
        out.append(self.front_number)
        if self.crowding_distance == float('inf'):
            out.append(0)
        else:
            out.append(self.crowding_distance)
        if self.feasible == float('inf'):
            out.append(0)
        else:
            out.append(self.feasible)
        dominates = []
        for individual in self.dominate:
            dominates.append(individual.number)
        out.append(dominates)
        out.append(self.gradient)
        return out

    def set_id(self):
        self.id = Individual.id
        Individual.id += 1

    @classmethod
    def gen_individuals(cls, number, population_id):
        individuals = []
        for i in range(number):
            individuals.append(cls.gen_individual(population_id))
        return individuals

    @classmethod
    def gen_individual(cls, parameters: dict, population_id=0):
        parameters_vector = VectorAndNumbers.gen_vector(cls, parameters)
        return cls(parameters_vector, population_id)
