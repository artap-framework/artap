from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.results import Results
import numpy as np


class SingleObjectiveProblem_NSGAII(Problem):

    def set(self):
        self.name = 'SingleObjective Test Problem'
        self.working_dir = '.'
        self.parameters = [{'name': 'x_1', 'bounds': [0, 1.0]}]
        self.costs = [{'name': 'f_1'}]

    def evaluate(self, individual):
        x = individual.vector[0]
        f1 = np.sum(x ** 2)
        return [f1]


problem = SingleObjectiveProblem_NSGAII()
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 10
algorithm.options['max_population_size'] = 10

algorithm.run()

results = Results(problem)


opt = results.find_optimum()

print(opt)

