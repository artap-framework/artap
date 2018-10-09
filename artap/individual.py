from random import random
from numpy.random import normal
from abc import *
from multiprocessing import Queue

class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """
    number = 0
    results = Queue()

    def __init__(self, design_parameters, problem, population_id=0):
        self.parameters = design_parameters
        self.problem = problem
        self.length = len(self.parameters)
        self.costs = []
        self.is_saved = False
        self.number = Individual.number
        Individual.number += 1

        self.population_id = population_id
        self.is_evaluated = False

    def to_string(self):
        string = "["
        for number in self.parameters:
            string += str(number) + ", "
        string = string[:len(string) - 1]
        string += "]"
        string += "; costs:["
        for number in self.costs:
            string += str(number) + ", "
        string += "]\n"
        return string

    def to_list(self):
        params = [self.number, self.population_id, self.parameters, self.costs]
        return params

    def evaluate(self):
        # problem cost function evaluate     
        costs = self.problem.eval(self.parameters)

        if type(costs) != list:
            self.costs = [costs]
        else:
            self.costs = costs

        self.is_evaluated = True
        if not self.is_saved:
            self.problem.data_store.write_individual(self.to_list())
            self.is_saved = True
        Individual.results.put([self.number, costs])
        return costs

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
                bounds = None
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
