import unittest
from artap.problem import Problem
from artap.algorithm_swarm import PSO
from artap.benchmark_functions import BinhAndKorn


class PSORosenbrock(Problem):
    """ Search the optimal value of the Rosenbrock function in 2d"""

    def set(self):
        self.name = "PSORosenbrock"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
                      {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]
        self.costs = [{'name': 'F_1'},
                      {'name': 'F_2'}]

    def evaluate(self, individual):
        function = BinhAndKorn()
        return function.eval(individual.vector)


class TestPSOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_pso(self):
        problem = PSORosenbrock()
        algorithm = PSO(problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        # b = Results(problem)
        # solution = b.pareto_values()
        # wrong = 0
        # for sol in solution:
        #     if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
        #             and 20 < sol[0] < 70:
        #         wrong += 1
        #
        # self.assertLessEqual(wrong, 5)

        # results = GraphicalResults(problem)
        # results.plot_scatter_vectors('x_1', 'x_2', filename="/tmp/scatter_vec.pdf", population_number=10)
        # results.plot_scatter('F_1', 'F_2', filename="/tmp/scatter.pdf", population_number=None)


if __name__ == '__main__':
    unittest.main()
