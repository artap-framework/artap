import numpy as np

from artap.algorithm_swarm import SMPSO, OMOPSO, PSOGA
from artap.problem import Problem
from artap.results import Results
from pylab import cos, sin, exp, plot, show, xlabel, ylabel, pi


class HolderTableProblem(Problem):

    def set(self):
        self.name = 'Holder Table Function'
        self.parameters = [{'name': 'x', 'bounds': [-10, 10]},
                           {'name': 'y', 'bounds': [-10, 10]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector[0]
        y = individual.vector[1]

        f_1 = -(np.abs(sin(x) * cos(y) * exp(np.abs(1 - (np.sqrt(x * x + y * y) / pi)))))

        return [f_1]


problem = HolderTableProblem()
algorithm = PSOGA(problem)
# algorithm = OMOPSO(problem)

algorithm.options['max_population_number'] = 5
algorithm.options['max_population_size'] = 5
algorithm.run()

results = Results(problem)
solution = results.find_optimum()
print(solution)
# pareto = results.pareto_values()
# print(pareto)
#
# print(f' f(x,y) : {pareto[0]}')
#
# plot(pareto, marker="o", color="blue", markeredgecolor="black")
# show()
