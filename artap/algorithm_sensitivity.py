from .utils import VectorAndNumbers
from .algorithm import Algorithm
from .population import Population
from .individual import Individual
from .job import Job
from .problem import Problem
from .operators import CustomGeneration

from SALib.sample.saltelli import sample as sobol_sample
from SALib.sample.morris import sample as morris_sample
from SALib.sample.fast_sampler import sample as fast_sample
from SALib.sample.latin import sample as latin_sample
from SALib.sample.ff import sample as ff_sample

from SALib.analyze import sobol
from SALib.analyze import ff
from SALib.analyze import morris
from SALib.analyze import fast
from SALib.analyze import rbd_fast
from SALib.analyze import delta

import time
import numpy as np

_method = ['rbd_fast', 'fast', 'morris', 'sobol', 'delta', 'ff']


class SALibAlgorithm(Algorithm):
    """
    SALib Analysis
    """

    def __init__(self, problem: Problem, name='SALibAlgorithm'):
        super().__init__(problem, name)

        self.sa_problem = {}
        self.samples_x = []
        self.samples_y = []

        self.job = Job(self.problem)

        self.options.declare(name='method', default='sobol', values=_method,
                             desc='Method')
        self.options.declare(name='print_to_console', default=False,
                             desc='Print to console')
        self.options.declare(name='samples', default=10, lower=1,
                             desc='Samples')

    def run(self):
        t_s = time.time()

        # set SALib problem
        names = []
        bounds = []
        for parameter in self.problem.parameters:
            names.append(parameter['name'])
            bounds.append(parameter['bounds'])

        self.sa_problem = {'num_vars': len(self.problem.parameters),
                           'names': names,
                           'bounds': bounds}

        # generate samples
        if self.options["method"] == "rbd_fast":
            self.samples_x = latin_sample(self.sa_problem, self.options["samples"])
        elif self.options["method"] == "fast":
            self.samples_x = fast_sample(self.sa_problem, self.options["samples"])
        elif self.options["method"] == "morris":
            self.samples_x = morris_sample(self.sa_problem, self.options["samples"], num_levels=4)
        elif self.options["method"] == "sobol":
            self.samples_x = sobol_sample(self.sa_problem, self.options["samples"])
        elif self.options["method"] == "delta":
            self.samples_x = latin_sample(self.sa_problem, self.options["samples"])
        elif self.options["method"] == "ff":
            self.samples_x = ff_sample(self.sa_problem, self.options["samples"])

        individuals = []
        for vector in self.samples_x:
            individuals.append(Individual(vector))

        # set current size
        self.population_size = len(individuals)
        # evaluate individuals
        self.evaluate(individuals)

        for individual in individuals:
            self.samples_y.append(individual.costs[0]) # TODO: fix index [0]
        self.samples_y = np.array(self.samples_y)

        population = Population(individuals)
        self.problem.populations.append(population)

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))

    def analyze(self):
        if self.options["method"] == "rbd_fast":
            return self.analyze_rbd_fast()
        elif self.options["method"] == "fast":
            return self.analyze_sobol()
        elif self.options["method"] == "morris":
            return self.analyze_morris()
        elif self.options["method"] == "sobol":
            return self.analyze_sobol()
        elif self.options["method"] == "delta":
            return self.analyze_delta()
        elif self.options["method"] == "ff":
            return self.analyze_ff()

    def analyze_rbd_fast(self):
        #  RBD-FAST - Random Balance Designs Fourier Amplitude Sensitivity Test
        return rbd_fast.analyze(self.sa_problem, self.samples_x, self.samples_y, print_to_console=self.options["print_to_console"])

    def analyze_fast(self):
        # FAST - Fourier Amplitude Sensitivity Test
        return fast.analyze(self.sa_problem, self.samples_y, print_to_console=self.options["print_to_console"])

    def analyze_morris(self):
        # Method of Morris
        return morris.analyze(self.sa_problem, self.samples_x, self.samples_y, conf_level=0.95, num_levels=4, print_to_console=self.options["print_to_console"])

    def analyze_sobol(self):
        # Sobol Sensitivity Analysis
        return sobol.analyze(self.sa_problem, self.samples_y, print_to_console=self.options["print_to_console"])

    def analyze_delta(self):
        # Delta Moment-Independent Measure
        return delta.analyze(self.sa_problem, self.samples_x, self.samples_y, print_to_console=self.options["print_to_console"])

    def analyze_ff(self):
        # Fractional Factorial
        return ff.analyze(self.sa_problem, self.samples_x, self.samples_y, second_order=True, print_to_console=self.options["print_to_console"])


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')

    def run(self):
        self.population_size = self.options['max_population_size']

        parameters = []
        for parameter in self.problem.parameters:
            parameters.append(float(parameter['initial_value']))

        population = Population()

        for parameter_name in self.parameters:
            parameter_values = []

            index = 0
            selected_parameter = None
            for parameter in self.parameters:
                if parameter['name'] == parameter_name['name']:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.options['max_population_size']):
                value = VectorAndNumbers.gen_number(selected_parameter['bounds'], selected_parameter['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy())
                individuals.append(individual)

            self.evaluate(population.individuals)
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

        # append population
        self.problem.populations.append(population)
