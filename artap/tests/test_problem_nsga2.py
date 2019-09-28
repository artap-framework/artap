import unittest

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AckleyN2
from artap.algorithm_genetic import NSGAII
from artap.results import Results

# import optproblems as optp
# import optproblems.cec2005 as cec2005
# import optproblems.dtlz as dtlz

# from math import pi


class BinhAndKornProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "TestNSGA2Optimization"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}, {'name': 'F_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        function = BinhAndKorn()
        return function.eval(individual.vector)

    def evaluate_constraints(self, individual):
        return BinhAndKorn.constraints(individual.vector)


class TestNSGA2Optimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

   def test_local_problem_nsga2(self):

        problem = BinhAndKornProblem()

        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 50
        algorithm.options['max_population_size'] = 200
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
=======
    def test_local_problem_nsga2(self, population_number=5):
        try:
            problem = BinhAndKornProblem()
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 50
            algorithm.options['calculate_gradients'] = True
            algorithm.options['verbose_level'] = 1

            algorithm.run()
            b = Results(problem)
            solution = b.pareto_values()
            wrong = 0

            #c = GraphicalResults(problem)
            #c.plot_populations()

            for sol in solution:
                if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
                        and 20 < sol[0] < 70:
                    wrong += 1
            print(wrong)
            self.assertLessEqual(wrong, 5)
        except AssertionError:
            # stochastic
            print("TestNSGA2Optimization::test_local_problem_nsga2", population_number)
            self.test_local_problem_nsga2(int(1.5 * population_number))
>>>>>>> 67d613f4a3d65887d47051fb5e17913667e32fa5


class AckleyN2Test(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def set(self):
        self.name = "TestAckleyN2"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-32, 32]},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [-32, 32]}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        function = AckleyN2()
        return [function.eval(individual.vector)]


class TestAckleyN2(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self, population_number=20):
        try:
            problem = AckleyN2Test()
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], -200, 0)
        except AssertionError:
            # stochastic
            self.test_local_problem(int(1.5 * population_number))

#####
#####
# class CEC2005_TEST_Problems(Problem):
#
#     # these problems working for 2, 10, 30 variables in every case
#
#     def __init__(self, name, test_function, ub, lb):
#
#         #ub = 100
#         #lb = -100
#
#         parameters = {'x_1', 'initial_value': 2.5, 'bounds': [lb, ub]},
#                       'x_2', 'initial_value': 2.5, 'bounds': [lb, ub]}}
#
#         costs = ['F_1']
#         self.function = test_function(2)
#
#         super().__init__(name, parameters, costs)
#
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
#     """ Tests that the NSGA II algorithm can find the global optimum of a function."""
#
#     def run_test_problem(self, method, ub, lb, gen_nr):
#         problem = CEC2005_TEST_Problems("CEC2005",method, ub, lb)
#         algorithm = NSGAII(problem)
#         algorithm.options['max_population_number'] = gen_nr
#         algorithm.options['max_population_size'] = 100
#         algorithm.run()
#
#         b = Results(problem)
#         optimum = b.find_minimum('F_1')  # Takes last cost function
#         self.assertAlmostEqual(optimum.costs[0], method.bias, 0)
#
#     # unimodal problems
#
#     def test_shifted_sphere(self):
#         self.run_test_problem(optp.cec2005.F1, 100, -100, 100)
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
#
#     # def test_rot_hybrid_function(self):
#     #     self.run_test_problem(optp.cec2005.F18, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_2(self):
#     #     self.run_test_problem(optp.cec2005.F19, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_3(self):
#     #     self.run_test_problem(optp.cec2005.F20, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_4(self):
#     #     self.run_test_problem(optp.cec2005.F21, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_5(self):
#     #     self.run_test_problem(optp.cec2005.F22, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_6(self):
#     #     self.run_test_problem(optp.cec2005.F23, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_7(self):
#     #     self.run_test_problem(optp.cec2005.F24, 5, -5, 1000)
#     #
#     # def test_rot_hybrid_function_wo_bounds(self):
#     #     self.run_test_problem(optp.cec2005.F25, 100, -100, 100)
#

#####

if __name__ == '__main__':
    unittest.main()
