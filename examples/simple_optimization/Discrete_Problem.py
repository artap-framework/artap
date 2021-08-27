import numpy as np

from artap.algorithm_swarm import SMPSO, OMOPSO, PSOGA
from artap.problem import Problem
from artap.results import Results


class DiscreteProblem(Problem):

    def set(self):
        self.name = 'Discrete Problem which deal with integer values'
        self.parameters = [{'name': 'x', 'bounds': [1, 10]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector[0]

        f_1 = -np.min(x * [3, 1])
        f_2 = x + x - 10

        return [f_1, f_2]


problem = DiscreteProblem()
algorithm = PSOGA(problem)

algorithm.options['max_population_number'] = 5
algorithm.options['max_population_size'] = 5
algorithm.run()

results = Results(problem)
solution = results.find_optimum()
print(solution)
print(solution.vector)
print(solution.costs)
