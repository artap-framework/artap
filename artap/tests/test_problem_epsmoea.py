import unittest

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, Ackley
from artap.algorithm_genetic import EpsMOEA
from artap.results import Results, GraphicalResults

# import optproblems as optp
# import optproblems.cec2005 as cec2005

# class BinhAndKornProblem(Problem):
#
#     """ Describe simple one objective optimization problem. """
#     def set(self):
#         self.name = "EPSMOEA"
#         self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
#                            {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]
#         self.costs = [{'name': 'F_1'}, {'name': 'F_2'}]
#
#     def evaluate(self, x):
#         function = BinhAndKorn()
#         return function.eval(x)
#
#     def evaluate_constraints(self, x):
#         return BinhAndKorn.constraints(x)
#
#
# class TestEPSMOEAOptimization(unittest.TestCase):
#     """ Tests simple one objective optimization problem."""
#
#     def test_local_problem_epsmoea(self):
#         problem = BinhAndKornProblem()
#         algorithm = EpsMOEA(problem)
#         algorithm.options['max_population_number'] = 100
#         algorithm.options['max_population_size'] = 100
#         algorithm.options['calculate_gradients'] = True
#         algorithm.options['verbose_level'] = 1
#         algorithm.options['epsilons'] = 0.05
#
#         algorithm.run()
#
#         b = Results(problem)
#         solution = b.pareto_values()
#         wrong = 0
#         for sol in solution:
#             if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
#                     and 20 < sol[0] < 70:
#                 wrong += 1
#
#         self.assertLessEqual(wrong, 10)
#
#
# class AckleyN2Test(Problem):
#     """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""
#
#     def set(self):
#         self.name = "TestAckleyN2"
#         self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-32, 32]},
#                       {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-32, 32]}]
#         self.costs = [{'name': 'F_1'}]
#
#     def evaluate(self, individual):
#         function = AckleyN2()
#         return [function.eval(individual.vector)]


class TestAckleyN222(unittest.TestCase):
    """ Tests that the eps-moea algorithm can find the global optimum of a function."""

    def test_local_problem(self, population_number=10):
        try:
            problem = Ackley(**{'dimension':1})
            algorithm = EpsMOEA(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['epsilons'] = 0.01
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 0)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
