import numpy as np
from .individual import Individual
from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from artap.operators import CustomGenerator, RandomGenerator, UniformGenerator
import time


class CEM(GeneticAlgorithm):
    """Cross-Entropy Method
    https://link.springer.com/content/pdf/10.1007/s10479-005-5724-z.pdf
    """

    def __init__(self, problem: Problem, name="Cross-Entropy Method"):
        super().__init__(problem, name)
        self.problem = problem
        # Initialize mean and standard deviation
        # self.theta_mean = np.zeros((dim_theta))
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

        self.dim_theta = len(self.problem.parameters)

        # Elite ratio percentage
        self.top_p = 30

        # Range of values
        self.min_val = 0
        self.max_val = 1
        self.theta_mean = np.random.uniform(self.min_val, self.max_val, (self.n_samples, self.dim_theta))
        self.theta_std = np.random.uniform(self.min_val, self.max_val, (self.n_samples, self.dim_theta))
        self.generator = CustomGenerator(self.problem.parameters)

    def fit_gaussian(self):
        generation = np.random.normal(self.theta_mean, self.theta_std)
        individuals = np.clip(generation, self.min_val, self.max_val)
        self.generator.init(individuals)
        vectors = self.generator.generate()
        individuals = []
        for vector in vectors:
            individuals.append(Individual(vector))
        return individuals

    def take_elite(self, candidates):
        n_top = int((self.n_samples * self.top_p) / 100)
        elite = candidates[:n_top]
        return elite

    def compute_new_mean(self, e_candidates):
        new_means = np.mean(e_candidates, axis=0)
        new_means = np.tile(new_means, (self.n_samples, 1))
        return new_means

    def compute_new_std(self, e_candidates):
        eps = 1e-3
        new_std = np.std(e_candidates, ddof=1, axis=0) + eps
        return new_std

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

        self.evaluate(individuals)

        start = time.time()
        self.problem.logger.info("CEM: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))
        for it in range(self.options['max_population_number']):

            lists = []
            for individual in individuals:
                lists.append(individual.costs)
            lists = np.array(lists)

            mean_fitness.append(np.mean(lists))
            best_fitness.append(np.min(lists))
            worst_fitness.append(np.max(lists))
            fitness.append(lists)

            elite = self.take_elite(individuals)

            e_candidates = [i.vector for i in elite]

            self.theta_mean = self.compute_new_mean(e_candidates)
            self.theta_std = self.compute_new_std(e_candidates)
            individuals = self.fit_gaussian()

            self.evaluate(individuals)
            for individual in individuals:
                # add to population
                individual.population_id = it + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        t = time.time() - start
        self.problem.logger.info("CEM: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()
