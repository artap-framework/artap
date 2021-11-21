import unittest

from ..benchmark_functions import AlpineFunction, Ackley
from ..benchmark_pareto import ZDT1
from ..algorithm_genetic import NSGAII
from ..results import Results
from ..problem import Problem
from ..quality_indicator import epsilon_add


class TestNSGA2(unittest.TestCase):
    def test_local_problem(self):
        problem = ZDT1()
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 5
        algorithm.options['max_population_size'] = 3
        algorithm.options['max_processes'] = 1
        algorithm.run()

        populations = problem.populations()

        self.assertEqual(len(populations), algorithm.options['max_population_number'] + 1)
        for individuals in populations.values():
            self.assertEqual(len(individuals), algorithm.options['max_population_size'])


class TestZDT1(unittest.TestCase):
    # integration test -- tests the total functionality of nsga2
    # around 11secs according to literature DOI: 10.1007/978-3-642-01020-0_39
    def test_local_problem(self):
        problem = ZDT1()
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 250
        algorithm.options['max_population_size'] = 100    # according to the literature
        algorithm.options['max_processes'] = 1
        algorithm.run()

        results = Results(problem)
        vals = results.pareto_values()
        exact = problem.pareto_front(vals[0])
        self.assertLessEqual(epsilon_add(exact, vals), 0.2)


class TestAckley(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=50):
        try:
            problem = Ackley(**{'dimension': 1})
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


class TestAlpine(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def test_local_problem(self, population_number=50):
        try:
            problem = AlpineFunction(**{'dimension': 3})
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
        except AssertionError:
            # stochastic
            print("TestAlpine::test_local_problem", population_number)
            self.test_local_problem(int(1.5 * population_number))


class ProblemConstraint(Problem):
    def set(self):
        self.name = 'ProblemConstraint'

        self.parameters = [{'name': 'x', 'initial_value': 1.0, 'bounds': [-2, 2]},
                           {'name': 'y', 'initial_value': -1.0, 'bounds': [-2, 2]}]

        # multi objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

        # constraints
        self.constraints = [{'name': 'c_1'},
                            {'name': 'c_2'}]

    def evaluate(self, individual):
        x = individual.vector

        f1 = 100 * (x[0] ** 2 + x[1] ** 2)
        f2 = (x[0] - 1) ** 2 + x[1] ** 2

        return [f1, f2]

    def evaluate_inequality_constraints(self, x):
        g1 = 2 * (x[0] - 0.1) * (x[0] - 0.9) / 0.18
        g2 = - 20 * (x[0] - 0.4) * (x[0] - 0.6) / 4.8

        return [g1, g2]


class MultiConstraintOptimization(unittest.TestCase):
    def test_constraint_nsgaii(self, population_number=10):
        try:
            problem = ProblemConstraint()
            algorithm = NSGAII(problem)
            algorithm.options['max_population_number'] = population_number
            algorithm.options['max_population_size'] = 100
            algorithm.options['max_processes'] = 1
            algorithm.run()

            f_1 = []
            f_2 = []
            for individual in problem.last_population():
                f_1.append(individual.costs[0])
                f_2.append(individual.costs[1])

            # print(len(problem.individuals))
            # for individual in problem.individuals:
            #    print(individual)

            self.assertLess(min(f_1), 1.5)
            self.assertGreater(max(f_1), 74)
            self.assertLess(max(f_2), 1.5)
            self.assertGreater(max(f_2), 0.75)

            # import matplotlib.pyplot as plt
            #
            # plt.figure(figsize=(7, 5))
            # # plt.scatter(res.F[:, 0], res.F[:, 1], s=30, facecolors='none', edgecolors='blue')
            # plt.scatter(f_1, f_2, s=30, facecolors='none', edgecolors='blue')
            # plt.title("Objective Space")
            # plt.show()

            # print(min(f_1), max(f_1), min(f_2), max(f_2))
        except AssertionError:
            # stochastic
            print("MultiConstraintOptimization::test_local_problem", population_number)
            self.test_constraint_nsgaii(int(1.5 * population_number))


if __name__ == '__main__':
    unittest.main()
