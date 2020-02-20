import unittest

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import EpsMOEA
from artap.results import Results, GraphicalResults

import optproblems as optp
import optproblems.cec2005 as cec2005

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

class AckleyN2Test(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def set(self):
        self.name = "TestAckleyN2"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-32, 32]},
                      {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-32, 32]}]
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        function = AckleyN2()
        return [function.eval(individual.vector)]


class TestAckleyN222(unittest.TestCase):
    """ Tests that the eps-moea algorithm can find the global optimum of a function."""

    def test_local_problem(self, population_number=10):
        try:
            problem = AckleyN2Test()
            algorithm = EpsMOEA(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['epsilons'] = 0.01
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], -200, 0)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))
#####
#####
# class CEC2005_TEST_Problems(Problem):
#
#     # these problems working for 2, 10, 30 variables in every case
#
#
#
#     def set(self):
#         # two variables
#         self.parameters = [{'name': 'x_1', 'bounds': [func.min_bounds[0], func.max_bounds[0]]},
#                            {'name': 'x_2', 'bounds': [func.min_bounds[1], func.max_bounds[1]]}]
#
#         self.costs = [{'name': 'F_1'}]
#
#     def evaluate(self, x):
#
#         #function = optp.cec2005.F1(2)
#         problem = optp.Problem(self.function, num_objectives = 1)
#         solutions = [optp.Individual(x)]
#
#         problem.batch_evaluate(solutions)
#
#         return [solutions[0].objective_values]

# class TestCEC2005(unittest.TestCase):
#     """Tests from CEC2005 library"""
#
#     def run_test_problem(self, nr_gen, function):
#         try:
#             global func
#             func = function
#             problem = CEC2005_TEST_Problems()
#             algorithm = EpsMOEA(problem)
#             algorithm.options['max_population_number'] = nr_gen
#             algorithm.options['max_population_size'] = 100
#             algorithm.options['max_processes'] = 10
#             algorithm.run()
#
#             b = Results(problem)
#             optimum = b.find_minimum('F_1')  # Takes last cost function
#             self.assertAlmostEqual(optimum.costs[0], func.bias, 0)
#             del func
#         except AssertionError:
#             # try again with more populations
#             max_pop = int(1.5 * nr_gen)
#             # print("Try again with more populations: {}".format(max_pop))
#             self.run_test_problem(max_pop, function)
#
#     def test_shifted_sphere(self):
#         self.run_test_problem(50, optp.cec2005.F1(2))
#
#
#     def test_shifted_double_sum(self):
#         self.run_test_problem(optp.cec2005.F2, 100, -100, 100)
#
#     # def test_shifted_rotated_elliptic(self): # wrong with platypus also
#     #     self.run_test_problem(optp.cec2005.F3, 100, -100, 10000)
#     #
#     #def test_shifted_schwefel(self): # wrong with platypus also
#     #    self.run_test_problem(optp.cec2005.F4, 100, -100, 10000)
#
#     def test_schwefel(self): # !
#         self.run_test_problem(optp.cec2005.F5, 100, -100, 100)
#
#     def test_shifted_rosenbrock(self):
#         self.run_test_problem(optp.cec2005.F6, 100, -100, 1000)
#
#     # multimodal problems
#     #def test_shifted_rot_griewank(self):
#     #    self.run_test_problem(optp.cec2005.F7, 100, -100, 10000)
#
#     #def test_shifted_rot_ackley(self):
#     #    self.run_test_problem(optp.cec2005.F8, 32, -32, 100)
#
#     def test_shifted_rastrigin(self):
#         self.run_test_problem(optp.cec2005.F9, 5, -5, 100)
#
#     def test_shifted_rot_rastrigin(self):
#         self.run_test_problem(optp.cec2005.F10, 5, -5, 1000)
#
#     def test_shifted_rot_weierstrass(self):
#         self.run_test_problem(optp.cec2005.F11, 0.5, -0.5, 100)
#
#     def test_fletcherpowell(self): #schwefel
#         self.run_test_problem(optp.cec2005.F12, pi, -pi, 100)
#
#     def test_f8f2(self):
#         self.run_test_problem(optp.cec2005.F13, 1, -3, 100)
#
#     def test_expanded_f6(self):
#         self.run_test_problem(optp.cec2005.F14, 100, -100, 100)
#
#     #####
#     def test_hybrid_composition(self):
#         self.run_test_problem(optp.cec2005.F15, 5, -5, 100)
#
#     def test_rotated_f15(self):
#         self.run_test_problem(optp.cec2005.F16, 5, -5, 100)
#
#     def test_f16_with_noise(self):
#         self.run_test_problem(optp.cec2005.F17, 5, -5, 250)

if __name__ == '__main__':
    unittest.main()
