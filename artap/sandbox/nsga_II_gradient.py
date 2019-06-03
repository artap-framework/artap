from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn
from artap.algorithm_genetic import NSGAII
from artap.results import Results


class BinhAndKornProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5]},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3]}}
        costs = ['F_1', 'F_2']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        function = BinhAndKorn()
        return function.eval(x)

    def evaluate_constraints(self, x):
        return BinhAndKorn.constraints(x)


problem = BinhAndKornProblem("TestNSGA2Optimization")
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 20
algorithm.options['calculate_gradients'] = True
algorithm.options['verbose_level'] = 1
algorithm.run()

b = Results(problem)

for population in problem.data_store.populations[0:1]:
    print(len(population.individuals))
    for individual in population.individuals:
        print(individual.gradient)

