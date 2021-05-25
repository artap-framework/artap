import numpy as np

from artap.algorithm_swarm import SMPSO, OMOPSO
from artap.problem import Problem
from artap.results import Results
from pylab import cos, sin, exp, plot, show, xlabel, ylabel


class KursaweFunctionProblem(Problem):

    def set(self):
        self.name = 'Kursawe Function'

        self.parameters = [{'name': 'x', 'bounds': [-5, 5]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector[0]

        f_1 = np.sum(-10 * exp(-0.2 * np.sqrt(np.square(x))))
        f_2 = np.sum(np.abs(x) ** 0.8 + 5 * sin(x ** 3))

        return [f_1, f_2]


problem = KursaweFunctionProblem()
algorithm = SMPSO(problem)
# algorithm = OMOPSO(problem)

algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 100
algorithm.run()

results = Results(problem)
solution = results.find_optimum()
#print(solution)
pareto = results.pareto_values()

for f1, f2 in pareto:
    plot(f1, f2, marker="o", color="blue", markeredgecolor="black")
    xlabel('f1')
    ylabel('f2')
show()
