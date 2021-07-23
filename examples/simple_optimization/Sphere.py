import matplotlib.pyplot as plt
import numpy as np

from artap.problem import Problem
from artap.algorithm_PSO import PSOAlgorithm
from artap.algorithm_swarm import SMPSO, PSOGA
from artap.algorithm_genetic import NSGAII
from artap.results import Results


class Sphere(Problem):
    def set(self):
        self.name = 'Sphere'

        self.parameters = [{'name': 'x1', 'bounds': [0, 1.0]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector[0]
        f1 = np.sum(x**2)
        return [f1]


problem = Sphere()
algorithm = PSOGA(problem)
algorithm.options['max_population_number'] = 2
algorithm.options['max_population_size'] = 10
# algorithm.options['init_position'] = [1, 1]
algorithm.run()
results = Results(problem)

ss = results.find_optimum()
print(ss)
