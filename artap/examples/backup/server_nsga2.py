from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import NSGAII
# from artap.results import Results
from artap.results import GraphicalResults


class MyProblem(Problem):
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


problem = MyProblem("NSGA2Optimization")
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 30
algorithm.options['max_population_size'] = 100
# algorithm.options['calculate_gradients'] = True
algorithm.run()

# results = GraphicalResults(problem)
# results.plot_scatter('F_1', 'F_2', filename="/tmp/scatter.pdf")
# results.plot_scatter('x_1', 'x_2')
# results.plot_individuals('F_1')
