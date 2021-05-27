import numpy as np

from artap.algorithm_swarm import SMPSO, OMOPSO
from artap.problem import Problem
from artap.results import Results
from artap.benchmark_functions import BenchmarkFunction
from pylab import cos, sin, exp, plot, show, xlabel, ylabel


class KursaweFunctionProblem(Problem):

    def set(self, **kwargs):
        self.name = 'Kursawe Function'
        p = BenchmarkFunction()
        if 'dimension' in kwargs:
            self.dimension = kwargs['dimension']
        self.parameters = [{'name': 'x', 'bounds': [-5, 5]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector
        f1 = []
        f2 = []
        for i in range(0, self.dimension):
            f_1 = np.sum(-10 * exp(-0.2 * np.sqrt(np.square(x[i]))))
            f1 = f_1

        for i in range(0, self.dimension):
            f_2 = np.sum(np.abs(x[i]) ** 0.8 + 5 * sin(x[i] ** 3))
            f2 = f_2
        return [f1, f2]


problem = KursaweFunctionProblem(**{'dimension': 1})
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
