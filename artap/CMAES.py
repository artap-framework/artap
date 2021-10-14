
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .individual import Individual
from artap.operators import UniformGenerator, IntegerGenerator
import time


class Termination:

    def __init__(self) -> None:
        """
        Base class for the implementation of a termination criterion for an algorithm.
        """
        super().__init__()

        # the algorithm can be forced to terminate by setting this attribute to true
        self.force_termination = False

    def do_continue(self, algorithm):
        """
        Whenever the algorithm objects wants to know whether it should continue or not it simply
        asks the termination criterion for it.
        Parameters
        ----------
        algorithm : class
            The algorithm object that is asking if it has terminated or not.
        Returns
        -------
        do_continue : bool
            Whether the algorithm has terminated or not.
        """

        if self.force_termination:
            return False
        else:
            return self._do_continue(algorithm)

    # the concrete implementation of the algorithm
    def _do_continue(self, algorithm, **kwargs):
        pass

    def has_terminated(self, algorithm):
        """
        Instead of asking if the algorithm should continue it can also ask if it has terminated.
        (just negates the continue method.)
        """
        return not self.do_continue(algorithm)


class NoTermination(Termination):
    def _do_continue(self, algorithm, **kwargs):
        return True


class MaximumGenerationTermination(Termination):

    def __init__(self, n_max_gen) -> None:
        super().__init__()
        self.n_max_gen = n_max_gen

        if self.n_max_gen is None:
            self.n_max_gen = float("inf")

    def _do_continue(self, algorithm, **kwargs):
        return algorithm.n_gen < self.n_max_gen


class MaximumFunctionCallTermination(Termination):

    def __init__(self, n_max_evals) -> None:
        super().__init__()
        self.n_max_evals = n_max_evals

        if self.n_max_evals is None:
            self.n_max_evals = float("inf")

    def _do_continue(self, algorithm, **kwargs):
        return algorithm.evaluator.n_eval < self.n_max_evals


class CMA_ES(GeneralEvolutionaryAlgorithm):
    """
    Implementation a hybrid of CMAES
    """

    def __init__(self, problem: Problem, name="Covariance Matrix Adaptation Evolutionary Strategy"):

        super().__init__(problem, name)
        # Population Size
        self.n_samples = self.options['max_population_size']
        # Number of generation
        self.t = self.options['max_population_number']
        self.individual_features['velocity'] = dict()
        self.individual_features['best_cost'] = dict()
        self.individual_features['best_vector'] = dict()

        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        # Add front_number feature
        self.individual_features['front_number'] = 0

        # self.selector = CopySelector(self.problem.parameters)
        # self.dominance = ParetoDominance()
        # # set random generator
        # self.generator = IntegerGenerator(self.problem.parameters, self.individual_features)
        # self.leaders = Archive()
        # self.mutator = PmMutator(self.problem.parameters, self.options['prob_mutation'])
        # # constants for the speed and the position calculation

        self.dim_theta = 10

        # Elite ratio percentage
        self.top_p = 20
        # Range of values
        self.min_val = 0
        self.max_val = 1
        # Plot or not (0 = False, 1 = True)
        self.plot = 1
        # Number of Runs
        self.runs = 1
        # Plot output frequency
        self.pause = 0.01
        self.theta_mean = np.random.uniform(self.min_val, self.max_val, (self.dim_theta))

        theta_std = np.random.uniform(self.max_val - 1, self.max_val, (self.dim_theta))
        self.theta_cov = np.diag(theta_std)
        self.generator = UniformGenerator(self.problem.parameters, self.individual_features)
        self.fit_gaussian()

    def fit_gaussian(self):
        self.theta = []
        # theta is actually the population sampled from the distribution
        theta = np.random.multivariate_normal(self.theta_mean, self.theta_cov, (self.n_samples))
        individuals = np.clip(theta, self.min_val, self.max_val)
        for individual in individuals:
            self.theta.append(Individual(individual, self.individual_features))
        # self.generator.init(self.options['max_population_size'])
        # individual = self.generator.generate()
        # self.theta = individual

    def generation(self, problem):
        # Sample n_sample candidates from N(theta)
        mean_fitness = []
        best_fitness = []
        worst_fitness = []

        for i in tqdm(range(0, self.t)):

            self.evaluate(self.theta)
            fitness = self.problem.costs
            mean_fitness.append(np.mean(fitness))
            best_fitness.append(np.min(fitness))
            worst_fitness.append(np.max(fitness))

            couple = list(zip(self.theta, np.transpose(fitness)))
            sorted_fitness = sorted(couple, key=lambda tup: tup[1])
            elite = self.take_elite(sorted_fitness)

            e_candidates = [i[0] for i in elite]

            self.theta_cov = self.compute_new_cov(e_candidates)
            self.theta_mean = self.compute_new_mean(e_candidates)
            self.fit_gaussian()

        # mean_fitness.append(np.mean(self.evaluate(self.theta)))
        # best_fitness.append(np.min(fitness))
        # worst_fitness.append(np.max(fitness))

        # couple = list(zip(self.theta, np.transpose(fitness)))
        # sorted_fitness = sorted(couple, key=lambda tup: tup[1])
        # elite = self.take_elite(sorted_fitness)

        # return mean_fitness, best_fitness, worst_fitness

    def take_elite(self, candidates):
        n_top = int((self.n_samples * self.top_p) / 100)
        elite = candidates[:n_top]
        return elite

    def compute_new_mean(self, e_candidates):

        new_means = np.mean(e_candidates, axis=0)
        return new_means

    def compute_new_cov(self, e_candidates):
        e_candidates = np.array(e_candidates)
        I = np.identity(self.dim_theta)
        cov = np.zeros((self.dim_theta, self.dim_theta))
        for i in range(self.dim_theta):
            for j in range(self.dim_theta):
                cov[i, j] = np.sum(
                    ((e_candidates[:, i] - self.theta_mean[i]) * (e_candidates[:, j] - self.theta_mean[j])), axis=0)

        return 1 / e_candidates.shape[0] * cov + I * 1e-3

    def run(self):
        # mean = []
        # best = []
        # worst = []
        start = time.time()
        self.problem.logger.info("CMA_ES: {}/{}".format(self.options['max_population_number'],
                                                       self.options['max_population_size']))
        for individual in self.theta:
            self.problem.data_store.sync_individual(individual)

        for it in range(self.options['max_population_number']):
            self.generation(self.problem)

            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        t = time.time() - start
        self.problem.logger.info("CMA_ES: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()