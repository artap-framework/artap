import numpy as np
from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from artap.operators import CustomGenerator, RandomGenerator, UniformGenerator
import time
from scipy.stats import norm
from .individual import Individual


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
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)

    def generate(self):
        # imsampling = ImportanceSampling()
        # samples = imsampling.generate()
        self.generator.init(self.options['max_population_size'])
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
        self.generator = UniformGenerator(self.problem.parameters, self.individual_features)

    def generate(self):
        sampling = ImportanceSampling(self.problem)
        samples = sampling.generate()
        individuals = samples
        # samples = weights
        # self.generator.init(samples)
        # individuals = self.generator.generate()
        # self.generator.init(self.options['max_population_size'])
        # individuals = self.generator.generate()

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
        # for it in range(self.options['max_population_number']):

        self.evaluate(individuals)

        for individual in individuals:
            # individual.costs[0] = individual.costs[0] / self.options['max_population_size']
            # add to population
            # individual.population_id = it + 1
            # append to problem
            self.problem.individuals.append(individual)
            # sync to datastore
            self.problem.data_store.sync_individual(individual)

        t = time.time() - start
        self.problem.logger.info("Monte_Carlo: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()


class ImportanceSampling(Monte_Carlo):
    """
    In statistics, importance sampling is a general technique for estimating properties of a particular distribution,
    while only having samples generated from a different distribution than the distribution of interest. The method was
    first introduced by Teun Kloek and Herman K. van Dijk in 1978,[1]

    p(x), given a distribution to be sampled, and a proposal distribution, q(x),
    now define weights w(x) = p(x) / q(x) , such that p(x) = (p(x)/q(x)) * q(x) = w(x)q(x).


    [1] Kloek, T.; van Dijk, H. K. (1978). "Bayesian Estimates of Equation System Parameters: An Application of
        Integration by Monte Carlo". Econometrica. 46 (1): 1–19.

    """

    def __init__(self, problem: Problem, name="Importance Sampling"):
        super().__init__(problem, name)
        self.name = 'Importance Sampling'
        self.min_val, self.max_val = 0, 1
        self.size = self.options['max_population_size']
        self.problem = problem
        self.mean = np.random.uniform(self.min_val, self.max_val, self.size)
        self.std = np.random.uniform(self.max_val - 1, self.max_val, self.size)
        self.cov = np.diag(self.std)

    def generate(self):
        individuals = []
        q = np.random.uniform(self.min_val, self.max_val, self.size)
        q_x = norm(self.mean, self.std).pdf(q)
        p_x = norm(self.min_val, self.max_val).pdf(q)

        weights = p_x / q_x
        samples = weights * q_x
        for i in range(len(samples)):
            individuals.append(Individual([samples[i]], self.individual_features))
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
        self.problem.logger.info("ImportanceSampling: {}/{}".format(self.options['max_population_number'],
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
        self.problem.logger.info("ImportanceSampling: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()


class Rejection_Sampling(Monte_Carlo):
    """
    Rejection sampling, or the acceptance-rejection method, is one of the basic techniques used to generate
    observations from a distribution. The rejection sampling method generates sampling values from a target
    distribution X with arbitrary probability density function f(x) by using a proposal distribution Y
    with probability density g(x). The idea is that one can generate a sample value from X by instead sampling
    from Y and accepting the sample from Y with probability f(x)/(Cg(x)), repeating the draws from
    Y until a value is accepted. C here is a constant, finite bound on the likelihood ratio f(x)/g(x),
    satisfying  1<=C<infty over the support of X; in other words, C must satisfy f(x)<=Mg(x) for all values of x [1].

    [1] Casella, George; Robert, Christian P.; Wells, Martin T. (2004). Generalized Accept-Reject sampling schemes.
        Institute of Mathematical Statistics. pp. 342–347. doi:10.1214/lnms/1196285403. ISBN 9780940600614.
    """

    def __init__(self, problem: Problem, name="Rejection Sampling"):
        super().__init__(problem, name)
        self.name = 'Rejection Sampling'
        self.min_val, self.max_val = 0, 1
        self.size = self.options['max_population_size']
        self.problem = problem
        self.dimension = 1
        self.mean = np.random.uniform(self.min_val, self.max_val, self.dimension)
        self.std = np.random.uniform(self.max_val - 1, self.max_val, self.dimension)
        self.C = 1.0

    def _p_x(self, x):
        output = norm.pdf(x, self.mean, self.std)
        return output

    def _q_x(self, x):
        output = norm.pdf(x, self.min_val, self.max_val)
        return output

    def generate(self):
        i, samples = 0, []
        individuals = []
        while i < self.size:
            x_i = np.random.normal(self.min_val, self.max_val)
            if self._p_x(x_i) <= self.C * self._q_x(x_i):
                u = np.random.uniform(self.min_val - 1, self.C * self._q_x(x_i))
                if u < self._p_x(x_i):
                    samples.append(x_i)
                    i = i + 1
                else:
                    i = i + 1
        for i in range(len(samples)):
            individuals.append(Individual([samples[i]], self.individual_features))
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
        self.problem.logger.info("Rejection_Sampling: {}/{}".format(self.options['max_population_number'],
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
        self.problem.logger.info("Rejection_Sampling: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()
