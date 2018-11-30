from .problem import Problem
from .population import Population
from .individual import Individual
from .utils import ConfigDictionary

from abc import ABCMeta, abstractmethod


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.options = ConfigDictionary()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')


    @abstractmethod
    def run(self):
        pass


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

    def run(self):
        parameters = []
        for parameter in self.problem.parameters.items():
            parameters.append(float(parameter[1]['initial_value']))

        for parameter_name in self.parameters:
            parameter_values = []
            population = Population(self.problem)

            index = 0
            selected_parameter = None
            for parameter in self.problem.parameters.items():
                if parameter[0] == parameter_name:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.problem.max_population_size):
                value = Individual.gen_number(selected_parameter[1]['bounds'], selected_parameter[1]['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy(), self.problem)
                individuals.append(individual)

            population.individuals = individuals
            population.evaluate()
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

            self.problem.populations.append(population)
