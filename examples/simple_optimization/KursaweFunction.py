import numpy as np

from artap.algorithm_swarm import SMPSO, OMOPSO, PSOGA
from artap.algorithm_genetic import NSGAII
from artap.problem import Problem
from artap.results import Results
from pylab import cos, sin, exp, plot, show, xlabel, ylabel


class KursaweFunctionProblem(Problem):

    def set(self, **kwargs):
        self.name = 'Kursawe Function'
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
            f_1 = np.sum(-10 * exp(-0.2 * np.sqrt(np.square(x[i]) + np.square(x[i - 1]))))
            f1 = f_1

        for i in range(0, self.dimension):
            f_2 = np.sum(np.abs(x[i]) ** 0.8 + 5 * sin(x[i] ** 3))
            f2 = f_2
        return [f1, f2]


problem = KursaweFunctionProblem(**{'dimension': 1})
# algorithm = SMPSO(problem)
# algorithm = OMOPSO(problem)
algorithm = PSOGA(problem)

algorithm.options['max_population_number'] = 5
algorithm.options['max_population_size'] = 5
algorithm.run()

results = Results(problem)
solution = results.find_optimum()
print(solution.vector)
print(solution.costs)
# s = results.population(10)
# print(s)
# ponindex = results.parameter_on_index(name='x', population_id=7)
# print(ponindex)
#
# csv = results.export_to_csv(filename='kursawe.csv')
#
# preto = results.pareto_front(population_id=10)  # It will get an error because the swarm algorithm does not have
# # 'front_number' feature
# print(preto)
# pareto = results.pareto_values()
# print(pareto)
#
# # Next lines without show() command, does not plot the objectives and goals 0n indexes
# results.objectives_plot()
# results.goal_on_index_plot(name='f_1', population_id=7)
# show()


# for f1, f2 in pareto:
#     plot(f1, f2, marker="o", color="blue", markeredgecolor="black")
#     xlabel('f1')
#     ylabel('f2')
# show()
