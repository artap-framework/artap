import unittest

# from pygments.lexer import words

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import NSGA_II
from artap.results import Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        costs = ['F_1', 'F_2']
        working_dir = "./"
        super().__init__(name, parameters, costs, save_data=True, working_dir=working_dir)
        self.options['save_level'] = "population"
        self.options['max_processes'] = 10
        self.options['save_data'] = True

    def eval(self, x):
        function = BinhAndKorn()
        return function.eval(x)

    def eval_constraints(self, x):
        return BinhAndKorn.constraints(x)


class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_nsga2(self):

        problem = MyProblem("TestNSGA2Optimization")
        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 10
        algorithm.options['calculate_gradients'] = True
        algorithm.run()

        b = Results(problem)
        solution = b.pareto_values()
        wrong = 0
        for sol in solution:
            if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
                    and 20 < sol[0] < 70:
                wrong += 1

        self.assertLessEqual(wrong, 3)


class AckleyN2Test(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1},
                      'x_2': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)
        self.options['save_level'] = "population"
        self.options['max_processes'] = 1

    def eval(self, x):
        function = AckleyN2()
        return function.eval(x)


class TestAckleyN2(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = AckleyN2Test("TestAckleyN2")
        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 15
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function
        self.assertAlmostEqual(optimum, -200, 0)


if __name__ == '__main__':
    unittest.main()
