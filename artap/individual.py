from random import random
from numpy.random import normal
from abc import *
from multiprocessing import Queue
from numpy import NaN
from copy import copy

import itertools

class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """
    number = 0
    results = None

    def __init__(self, design_parameters, problem, population_id=0):
        self.parameters = design_parameters
        self.problem = problem
        self.length = len(self.parameters)
        self.costs = []
        self.number = Individual.number
        Individual.number += 1

        self.feasible = 0.0 # the distance from the feasibility region in min norm
        self.population_id = population_id
        self.is_evaluated = False

    def __repr__(self):
        """ :return: [parameters[p1, p2, ... pn]; costs[c1, c2, ... cn]] """
        string = "parameters: ["

        for i,number in enumerate(self.parameters):
            string += str(number)
            if i<len(self.costs)-1:
                string += ", "

        string = string[:len(string) - 1]
        string += "]"
        string += "; costs:["
        for i,number in enumerate(self.costs):
            string += str(number)
            if i<len(self.costs)-1:
                string += ", "
        string += "]\n"
        return string

    def to_list(self):
        params = [[self.number], [self.population_id], self.parameters, self.costs]
        # flatten list
        return [val for sublist in params for val in sublist]

    def evaluate(self):

        # check the constraints
        constraints = self.problem.eval_constraints(self.parameters)

        if constraints:
            self.feasible = sum(map(abs,constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints
        costs = self.problem.eval(self.parameters)

        if costs is not list:
            self.costs = [costs]
        # scipy uses the result number, the genetic algorithms using the property value
        self.is_evaluated = True
        self.problem.data_store.write_individual(self.to_list())

        #Individual.results.put([copy()])
        if self.problem.max_processes > 1:
            Individual.results.put([self.number, costs, self.feasible])

        return costs # for scipy

    def set_id(self):
        self.number = Individual.number
        Individual.number += 1

    @classmethod
    def gen_individuals(cls, number, problem, population_id):
        individuals = []
        for i in range(number):
            individuals.append(cls.gen_individual(problem, population_id))
        return individuals

    @classmethod
    def gen_individual(cls, problem, population_id=0):
        parameters_vector = cls.gen_vector(cls, problem.parameters)
        return cls(parameters_vector, problem, population_id)

    @staticmethod
    def gen_vector(cls, design_parameters: dict):

        parameters_vector = []
        for parameter in design_parameters.items():

            if not ('bounds' in parameter[1]):
                bounds = [parameter["initial_value"] * 0.5, parameter["initial_value"] * 1.5]
            else:
                bounds = parameter[1]['bounds']

            if not ('precision' in parameter[1]):
                precision = None
            else:
                precision = parameter[1]['precision']

            if (precision is None) and (bounds is None):
                parameters_vector.append(cls.gen_number())
                continue

            if precision is None:
                parameters_vector.append(cls.gen_number(bounds=bounds))
                continue

            if bounds is None:
                parameters_vector.append(cls.gen_number(precision=precision))
                continue

            parameters_vector.append(cls.gen_number(bounds, precision))

        return parameters_vector

    @classmethod
    def gen_number(cls, bounds=None, precision=0, distribution="uniform"):

        number = 0
        if bounds is None:
            bounds = [0, 1]

        if precision == 0:
            precision = 1e-12

        if distribution == "uniform":
            number = random() * (bounds[1] - bounds[0]) + bounds[0]
            number = round(number / precision) * precision

        if distribution == "normal":
            mean = (bounds[0] + bounds[1]) / 2
            std = (bounds[1] - bounds[0]) / 6
            number = normal(mean, std)

        return number


class Individual_NSGA_II(Individual):

    def __init__(self, x, problem, population_id=0):
        super().__init__(x, problem, population_id)
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = 0
        self.crowding_distance = 0
