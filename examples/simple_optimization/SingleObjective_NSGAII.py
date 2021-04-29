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
        x = individual.vector
        f1 = np.sum(k ** 2 for k in x)
        return [f1]


problem = SingleObjectiveProblem_NSGAII()
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 100
algorithm.options['max_population_size'] = 100

algorithm.run()

results = Results(problem)


opt = results.find_optimum('f_1')

print('Optimal solution (NSGAII):', opt)

