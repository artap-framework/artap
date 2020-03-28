import unittest

from artap.problem import Problem
from artap.benchmark_functions import BinhAndKorn, AlpineFunction, Ackley
from artap.algorithm_genetic import NSGAII
from artap.results import Results


class BinhAndKornProblem(Problem):
    """
    Describe simple one objective optimization problem.
    Note: This test is not removed, because its not part of the cec2005 library.
    """

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

            # c = GraphicalResults(problem)
            # c.plot_populations()

            for sol in solution:
                if abs(BinhAndKorn.approx(sol[0]) - sol[1]) > 0.1 * BinhAndKorn.approx(sol[0]) \
                        and 20 < sol[0] < 70:
                    wrong += 1

            self.assertLessEqual(wrong, 5)
        except AssertionError:
            # stochastic
            print("TestNSGA2Optimization::test_local_problem_nsga2", population_number)
            self.test_local_problem_nsga2(int(1.5 * population_number))


class TestAckley(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=15):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 50
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


class TestAlpine(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=15):
        try:
            problem = AlpineFunction(**{'dimension': 3})
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 10
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAlpine::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
