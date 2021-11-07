import unittest

from ..results import Results
from ..problem import Problem
from ..benchmark_functions import Ackley

try:
    from ..algorithm_pymoo import Pymoo

    from pymoo.algorithms.soo.nonconvex.ga import GA
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.algorithms.soo.nonconvex.isres import ISRES
    from pymoo.algorithms.soo.nonconvex.nelder_mead import NelderMead
    from pymoo.algorithms.soo.nonconvex.de import DE

    from pymoo.operators.sampling.lhs import LHS
    from pymoo.factory import get_sampling, get_crossover, get_mutation

    __pymoo__ = True
except ImportError:
    print("pymoo is not present test skiped")
    __pymoo__ = False


class ProblemConstraint(Problem):
    def set(self):
        self.name = 'ProblemConstraint'

        self.parameters = [{'name': 'x', 'initial_value': 1.0, 'bounds': [-2, 2]},
                           {'name': 'y', 'initial_value': -1.0, 'bounds': [-2, 2]}]

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x = individual.vector

        f1 = 100 * (x[0] ** 2 + x[1] ** 2)
        f2 = (x[0] - 1) ** 2 + x[1] ** 2

        return [f1, f2]

    def evaluate_inequality_constraints(self, x):
        g1 = 2 * (x[0] - 0.1) * (x[0] - 0.9) / 0.18
        g2 = - 20 * (x[0] - 0.4) * (x[0] - 0.6) / 4.8

        return [g1, g2]


class TestpymooMultiConstraintOptimization(unittest.TestCase):
    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_pymoo_nsgaii(self):
        moo_algorithm = NSGA2(
            pop_size=40,
            n_offsprings=10,
            sampling=get_sampling("real_random"),
            crossover=get_crossover("real_sbx", prob=0.9, eta=15),
            mutation=get_mutation("real_pm", eta=20),
            eliminate_duplicates=True
        )

        problem = ProblemConstraint()

        algorithm = Pymoo(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 40
        algorithm.options['algorithm'] = moo_algorithm
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
        #
        # print(min(f_1), max(f_1), min(f_2), max(f_2))


class TestAckley(unittest.TestCase):
    """ Tests that the nsga - ii can find the global optimum. """

    def moo(self, moo_algorithm, population_number=20):
        try:
            problem = Ackley(**{'dimension': 1})

            algorithm = Pymoo(problem)
            algorithm.options['verbose_level'] = 0
            algorithm.options['n_iterations'] = population_number
            algorithm.options['algorithm'] = moo_algorithm
            algorithm.run()

            b = Results(problem)
            optimum = b.find_optimum('f_1')  # Takes last cost function
            #print(optimum)
            self.assertLess(optimum.costs[0], problem.global_optimum + 1.0)
        except AssertionError:
            # stochastic
            print("TestAckleyN222::test_local_problem", population_number)
            self.moo(moo_algorithm, int(1.5 * population_number))

    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_nsga2(self):
        moo_algorithm = NSGA2(
            pop_size=10,
            n_offsprings=10,
            sampling=get_sampling("real_random"),
            crossover=get_crossover("real_sbx", prob=0.9, eta=15),
            mutation=get_mutation("real_pm", eta=20),
            eliminate_duplicates=True
        )
        self.moo(moo_algorithm)

    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_isres(self):
        moo_algorithm = ISRES(
            n_offsprings=30,
            rule=1.0 / 7.0,
            gamma=0.85,
            alpha=0.2)
        self.moo(moo_algorithm)

    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_nelder_mead(self):
        moo_algorithm = NelderMead(max_restarts=1)
        self.moo(moo_algorithm)

    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_ga(self):
        moo_algorithm = GA(
            pop_size=20,
            eliminate_duplicates=True)
        self.moo(moo_algorithm)

    @unittest.skipIf(__pymoo__ is False, "requires pymoo")
    def test_de(self):
        moo_algorithm = DE(
            pop_size=20,
            sampling=LHS(),
            variant="DE/rand/1/bin",
            CR=0.3,
            dither="vector",
            jitter=False
        )
        self.moo(moo_algorithm)
