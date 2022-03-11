import numpy as np
from tqdm import tqdm

from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .individual import Individual
from artap.operators import CustomGenerator, RandomGenerator, UniformGenerator
import time


class CEM(GeneralEvolutionaryAlgorithm):
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
        self.top_p = 20

        # Range of values
        self.min_val = 0
        self.max_val = 1
        self.theta_mean = np.random.uniform(self.min_val, self.max_val, (self.n_samples, self.dim_theta))
        self.theta_std = np.random.uniform(self.min_val, self.max_val, (self.n_samples, self.dim_theta))
        self.generator = UniformGenerator(self.problem.parameters, self.individual_features)

    def run(self):
        pass
