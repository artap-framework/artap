import numpy as np
from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .individual import Individual
from artap.operators import CustomGenerator
import time


class CMA_ES(GeneralEvolutionaryAlgorithm):
    """
    Implementation of CMA_ES, Covariance Matrix Adaptation Evolutionary strategy (CMA_ES).
    The Covariance Matrix Adaptation Evolution Strategy (CMA-ES) [1] is one of the most effective approaches
    for black-box optimization, in which objective functions cannot be specified explicitly in general.
    CMA-ES outperformed over 100 black-box optimization approaches for a variety of benchmark problems [2].

    The CMA-ES algorithm selects solutions from a multivariate gaussian distribution. Following the evaluation of
    all solutions, the solutions are sorted by evaluation values, and the distribution parameters
    (i.e., the mean vector and the covariance matrix) are updated depending on the ranking of evaluation values.

    [1] Nikolaus Hansen and Andreas Ostermeier. Completely derandomized self-adaptation in evolution strategies.
        Evol. Comput., 9(2):159–195, June 2001.
        DOI: http://dx.doi.org/10.1162/106365601750190398.
    [2] Nikolaus Hansen. The CMA Evolution Strategy: A Comparing Review, pages 75–102. Springer Berlin Heidelberg,
        Berlin, Heidelberg, 2006.
        DOI: https://doi.org/10.1007/3-540-32494-1_4.

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

        self.dim_theta = 1

        # Elite ratio percentage
        self.top_p = 20
        # Range of values
        self.min_val = 0
        self.max_val = 1
        # Number of Runs
        self.runs = 1
        self.theta_mean = np.random.uniform(self.min_val, self.max_val, self.dim_theta)
        # self.individuals = []
        theta_std = np.random.uniform(self.max_val - 1, self.max_val, self.dim_theta)
        self.theta_cov = np.diag(theta_std)
        self.generator = CustomGenerator(self.problem.parameters, self.individual_features)
        # self.fit_gaussian()

    def fit_gaussian(self):
        """
        generates individuals from a multivariate gaussian distribution
        :param
        :return population: list of individuals
        """
        theta = np.random.multivariate_normal(self.theta_mean, self.theta_cov, self.options['max_population_size'])
        individuals = np.clip(theta, self.min_val, self.max_val)
        self.generator.init(individuals)
        individuals = self.generator.generate()

        return individuals

    def take_elite(self, candidates):
        """
        Based on the fitness, it will take top individuals
        :param candidates
        :return elite: list of top individuals
        """
        n_top = int((self.n_samples * self.top_p) / 100)
        elite = candidates[:n_top]
        return elite

    def compute_new_mean(self, e_candidates):
        """
        Update distribution parameters. Here, the mean vector will be updated depending on the ranking of
        evaluation values.
        :param e_candidates
        :return new_means vector
        """
        new_means = np.mean(e_candidates, axis=0)
        return new_means

    def compute_new_cov(self, e_candidates):
        """
        Update distribution parameters. Here, the covariance matrix will be updated depending on the ranking of
        evaluation values
        :param e_candidates
        :return new_covariance matrix
        """
        e_candidates = np.array(e_candidates)
        I = np.identity(self.dim_theta)
        cov = np.zeros((self.dim_theta, self.dim_theta))
        for i in range(self.dim_theta):
            for j in range(self.dim_theta):
                cov[i, j] = np.sum(
                    ((e_candidates[:, i] - self.theta_mean[i]) * (e_candidates[:, j] - self.theta_mean[j])), axis=0)

        return 1 / e_candidates.shape[0] * cov + I * 1e-3

    def run(self):
        mean_fitness = []
        best_fitness = []
        worst_fitness = []
        fitness = []
        individuals = self.fit_gaussian()
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

            self.problem.data_store.sync_individual(individual)

        start = time.time()
        self.problem.logger.info("CMA_ES: {}/{}".format(self.options['max_population_number'],
                                                        self.options['max_population_size']))
        for it in range(self.options['max_population_number']):
            self.evaluate(individuals)

            lists = []
            for individual in individuals:
                # fitness.append(individual.costs)
                lists.append(individual.costs)
            lists = np.array(lists)

            mean_fitness.append(np.mean(lists))
            best_fitness.append(np.min(lists))
            worst_fitness.append(np.max(lists))
            fitness.append(lists)

            elite = self.take_elite(individuals)

            e_candidates = [i.vector for i in elite]

            self.theta_cov = self.compute_new_cov(e_candidates)
            self.theta_mean = self.compute_new_mean(e_candidates)
            self.fit_gaussian()

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
