import matplotlib.pyplot as plt

from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.results import Results


class RosenbrockFunctionProblem(Problem):
    def set(self):
        self.name = 'Rosenbrock Function Optimization'

        self.parameters = [{'name': 'x1', 'bounds': [-1.5, 1.5], 'parameter_type': 'integer'},
                           {'name': 'x2', 'bounds': [-0.5, 2.5], 'parameter_type': 'integer'}, ]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'},
                      {'name': 'f_3', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector
        F1 = (1 - x[0])
        F2 = (x[1] - (x[0] ** 2))
        F3 = F1 ** 2 + 100 * (F2 ** 2)
        return [F3]


problem = RosenbrockFunctionProblem()
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 10
algorithm.options['max_population_size'] = 10
algorithm.run()

results = Results(problem)

optimum = results.find_optimum()
print(optimum)

solution = results.pareto_values()

print(solution)
plt.plot(solution)
plt.show()

results.objectives_plot()
