import numpy as np
from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from artap.operators import Generator, CustomGenerator
import time
from scipy.stats import norm


class ImportanceSampling(Generator):
    """
    In statistics, importance sampling is a general technique for estimating properties of a particular distribution,
    while only having samples generated from a different distribution than the distribution of interest. The method was
    first introduced by Teun Kloek and Herman K. van Dijk in 1978,[1]

    p(x), given a distribution to be sampled, and a proposal distribution, q(x),
    now define weights w(x) = p(x) / q(x) , such that p(x) = (p(x)/q(x)) * q(x) = w(x)q(x).


    [1] Kloek, T.; van Dijk, H. K. (1978). "Bayesian Estimates of Equation System Parameters: An Application of
        Integration by Monte Carlo". Econometrica. 46 (1): 1–19.

    """

    def __init__(self):
        super().__init__()
        self.min_val, self.max_val = 0, 1
        self.size = 10
        self.mean = np.random.uniform(self.min_val, self.max_val, self.size)
        self.std = np.random.uniform(self.max_val - 1, self.max_val, self.size)
        self.cov = np.diag(self.std)

    def generate(self):
        q = np.random.multivariate_normal(self.mean, self.cov, self.size)
        q_x = norm(self.min_val, self.max_val).pdf(q)
        p_x = norm(self.min_val, self.max_val).pdf(q)

        weights = p_x / q_x
        return weights * q_x


class Monte_Carlo(GeneralEvolutionaryAlgorithm):
    """
    Monte Carlo simulation
        1) make a list of random values of x
        2) pick a small number of random value of x
        3) evaluate the objective function
        4) pick the lowest
    """

    def __init__(self, problem: Problem, name="Monte Carlo"):
        super().__init__(problem, name)
        self.evaluation = 0
        self.z_min, self.z_max = 0, 1
        self.sampling_size = self.options['max_population_size']
        self.problem = problem
        # self.problem.parameters = bm.generate_paramlist(self, dimension=self.dimension, lb=0.0, ub=1.0)
        self.intervals = np.linspace(self.z_min, self.z_max, self.sampling_size)
        self.generator = CustomGenerator(self.problem.parameters, self.individual_features)

    def generate(self):
        imsampling = ImportanceSampling()
        samples = imsampling.generate()
        self.generator.init(samples)
        individuals = self.generator.generate()

        return individuals

    def run(self):

        individuals = self.generate()
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

            self.problem.data_store.sync_individual(individual)

        start = time.time()
        self.problem.logger.info("Monte_Carlo: {}/{}".format(self.options['max_population_number'],
                                                             self.options['max_population_size']))
        for it in range(self.options['max_population_number']):

            self.evaluate(individuals)

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        t = time.time() - start
        self.problem.logger.info("Monte_Carlo: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()


class Numerical_Integrator(GeneralEvolutionaryAlgorithm):
    """
    Adaptive Monte Carlo Integral Approximation.
    Summation is used to estimate the expected value of a function under a distribution, instead of integration.
    """

    def __init__(self, problem: Problem, name="Numerical Integrator using Monte Carlo"):
        super().__init__(problem, name)
        self.evaluation = 0
        self.z_min, self.z_max = 0, 1
        self.sampling_size = self.options['max_population_size']
        self.problem = problem
        # self.problem.parameters = bm.generate_paramlist(self, dimension=self.dimension, lb=0.0, ub=1.0)
        self.intervals = np.linspace(self.z_min, self.z_max, self.sampling_size)
        self.generator = CustomGenerator(self.problem.parameters, self.individual_features)

    def generate(self):
        imsampling = ImportanceSampling()
        samples = imsampling.generate()
        self.generator.init(samples)
        individuals = self.generator.generate()

        return individuals

    def run(self):

        individuals = self.generate()
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

            self.problem.data_store.sync_individual(individual)

        start = time.time()
        self.problem.logger.info("Monte_Carlo: {}/{}".format(self.options['max_population_number'],
                                                             self.options['max_population_size']))
        for it in range(self.options['max_population_number']):

            self.evaluate(individuals)

            for individual in individuals:
                individual.costs[0] = individual.costs[0] / self.options['max_population_size']
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        t = time.time() - start
        self.problem.logger.info("Monte_Carlo: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()
