import matplotlib.pyplot as plt
import numpy as np

from artap.problem import Problem
from artap.algorithm_PSO import PSOAlgorithm
from artap.results import Results


class Sphere(Problem):
    def set(self):
        self.name = 'Sphere'

        self.parameters = [{'name': 'x1', 'bounds': [1, 1], 'parameter_type': 'integer'}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual
        f1 = np.sum(np.square(x))
        return [f1]


problem = Sphere()
algorithm = PSOAlgorithm(problem)
# algorithm.options['max_population_number'] = 100
# algorithm.options['max_population_size'] = 100
# algorithm.options['init_position'] = [1, 1]
s = algorithm.run()
results = Results(problem)
print("Sphere function")
print(f'x = {s[0]}')
print(f'f = {s[1]}')
