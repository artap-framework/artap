from .problem import Problem
from .utils import ConfigDictionary
from .job import JobSimple
from .population import Population
from .individual import Individual,GeneticIndividual
from .operators import RandomGeneration

from abc import ABCMeta, abstractmethod
import numpy as np

from joblib import Parallel, delayed


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.parameters = problem.parameters
        self.options = ConfigDictionary()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')
        self.options.declare(name='calculate_gradients', default=False,
                             desc='Enable calculating of gradients')
        # max(int(2 / 3 * cpu_count(), 1)
        self.options.declare(name='max_processes', default=1,
                             desc='Max running processes')

        self.options.declare(name='n_iterations', default=10,
                             desc='Max number of iterations')

        # initial population size
        self.population_size = 0

        # set random generator
        self.generator = RandomGeneration(self.problem.parameters)
        self.generator.init(10)

    @abstractmethod
    def run(self):
        pass

    def gen_initial_population(self, is_archive=False):
        individuals = self.generator.generate()
        # set current size
        self.population_size = len(individuals)
        # evaluate individuals
        self.evaluate(individuals)

        if is_archive:
            population = Population(individuals, individuals)
        else:
            population = Population(individuals)
        return population

    def evaluate(self, individuals: list):
        if self.options["max_processes"] > 1:
            self.evaluate_parallel(individuals)
        else:
            self.evaluate_serial(individuals)

        n_failed = 0
        for individual in individuals:
            if individual.state == Individual.State.FAILED:
                n_failed += 1
                individuals.remove(individual)   # TODO: is can be not feasible?
            if isinstance(individual, GeneticIndividual):
                individual.transform_data(self.problem.signs)


    def evaluate_serial(self, individuals: list):
        job = JobSimple(self.problem)
        for individual in individuals:
            if individual.state == Individual.State.EMPTY:
                job.evaluate(individual)

    def evaluate_parallel(self, individuals: list):
        # simple parallel loop
        job = JobSimple(self.problem)
        Parallel(n_jobs=self.options["max_processes"], verbose=1, require='sharedmem')(delayed(job.evaluate)(individual)
                                                                                       for individual in individuals)

    def evaluate_gradient(self, individuals: list, gradient_individuals: list):
        # Todo: Make operator Gradient consisting of current gradient generator and evaluate_gradient
        # individuals.sort(key=lambda x: abs(x.depends_on))
        n_params = len(individuals[0].vector)
        for j in range(len(individuals)):
            table = []
            for i in range(len(gradient_individuals)):
                individual = gradient_individuals[i]
                if individual.depends_on == j:
                    table.append(individual)

            gradient = np.zeros(n_params)
            for k in range(len(table)):
                index = table[k].modified_param
                gradient[index] = ((individuals[j].costs[0] - table[k].costs[0]) / 1e-6)

            individuals[j].gradient = gradient


class DummyAlgorithm(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, name='DummyAlgorithm'):
        super().__init__(problem, name)

    def run(self):
        pass
