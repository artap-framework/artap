import os
import unittest

from artap.problem import Problem
from artap.benchmark_functions import Binh_and_Korn, AckleyN2
from artap.algorithm_genetic import NSGA_II
from artap.results import GraphicalResults, Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        costs = ['F_1', 'F_2']

        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep

        super().__init__(name, parameters, costs, working_dir=working_dir)
        self.options['save_data'] = False
        self.options['max_processes'] = 10

    def eval(self, x):
        return Binh_and_Korn.eval(x)

    def eval_constraints(self, x):
        return Binh_and_Korn.constraints(x)


class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_nsga2(self):

        problem = MyProblem("LocalPythonProblemNSGA_II")
        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 40
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        b = Results(problem)
        solution = b.pareto_values()
        # print(*solution[0], sep="\n")

        x, y = zip(*solution)

        wrong = 0
        for sol in solution:
            if abs(Binh_and_Korn.approx(sol[0])-sol[1]) > 0.1 * Binh_and_Korn.approx(sol[0]) and sol[0] > 20 and sol[0]< 70:
                wrong += 1

        self.assertAlmostEqual(wrong, 0)


class AckleyN2Test(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1},
                      'x_2': {'initial_value': 2.5, 'bounds': [-32, 32], 'precision': 1e-1}}
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir)
        self.options['save_data'] = False
        self.options['max_processes'] = 10

    def eval(self, x):
        return AckleyN2.eval(x)


class TestAckleyN2(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = AckleyN2Test("LocalPythonProblem")
        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 15
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function
        self.assertAlmostEqual(optimum, -200, 0)


if __name__ == '__main__':
    unittest.main()
