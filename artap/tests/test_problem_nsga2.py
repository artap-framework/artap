import unittest

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.results import Results, GraphicalResults

import optproblems as optp
import optproblems.cec2005 as cec2005

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


class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_nsga2(self):

        problem = BinhAndKornProblem("TestNSGA2Optimization")

        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 50
        algorithm.options['max_population_size'] = 50
        algorithm.options['calculate_gradients'] = True
        algorithm.options['verbose_level'] = 1
        algorithm.run()

        b = Results(problem)
        solution = b.pareto_values()
        wrong = 0
        for sol in solution:
            if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
                    and 20 < sol[0] < 70:
                wrong += 1

        self.assertLessEqual(wrong, 5)


class AckleyN2Test(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-32, 32]},
                      'x_2': {'initial_value': 2.5, 'bounds': [-32, 32]}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        function = AckleyN2()
        return [function.eval(x)]


class TestAckleyN2(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = AckleyN2Test("TestAckleyN2")
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        #algorithm.options['max_population_number'] = 3
        #algorithm.options['max_population_size'] = 3
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function
        self.assertAlmostEqual(optimum.costs[0], -200, 0)
#####
#####
class CEC2005_TEST_Problems(Problem):

    def __init__(self, name, nr):

        ub = 100
        lb = -100

        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [ub, lb]},
                      'x_2': {'initial_value': 2.5, 'bounds': [ub, lb]},
                      'x_3': {'initial_value': 2.5, 'bounds': [ub, lb]},
                      'x_4': {'initial_value': 2.5, 'bounds': [ub, lb]},
                      'x_5': {'initial_value': 2.5, 'bounds': [ub, lb]}}

        costs = ['F_1']

        super().__init__(name, parameters, costs)


    def evaluate(self, x):

        function = optp.cec2005.F1(5)
        problem = optp.Problem(function, num_objectives = 1)
        solutions = [optp.Individual(x)]

        problem.batch_evaluate(solutions)

        return [solutions[0].objective_values]


class TestCEC2005(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = CEC2005_TEST_Problems("CEC2005", 1)
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        #algorithm.options['max_population_number'] = 3
        #algorithm.options['max_population_size'] = 3
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function


        self.assertAlmostEqual(optimum.costs[0], -450, 0)

#####
#####
class TestAckleyN2(unittest.TestCase):
    """ Tests that the eps-moea algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = AckleyN2Test("TestAckleyN2")
        algorithm = EpsMOEA(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        algorithm.options['epsilons'] = 0.01
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function
        self.assertAlmostEqual(optimum.costs[0], -200, 0)

if __name__ == '__main__':
    unittest.main()
