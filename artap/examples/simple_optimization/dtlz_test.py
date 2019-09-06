from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.results import Results

import optproblems as optp
import optproblems.dtlz as dtlz

import matplotlib.pyplot as plt
#
# TODO::: No module named : diversipy
#

class DTLZ2_TEST_Problems(Problem):
    """
    This example shows the solution of a DTLZ test example. This name is an abbreviation of the
    authors Deb -- Thiele -- Laumanns -- Zitzler (I -- VII). The definition and the solution of
    these multiobjective optimization test problems defined in [Deb2002] and in the optproblems
    library.

    Here, the DTLZ -- 2 problem was solved for 10 independent parameters. The solution, the Pareto-front
    of this example is placed on a 3 dimensional sphere.
    NSGA - II algorithm is used to solve this example.

    References
    ----------

    .. [Deb2002] Deb, K.; Thiele, L.; Laumanns, M.; Zitzler, E. (2002).
        Scalable multi-objective optimization test problems, Proceedings of
        the IEEE Congress on Evolutionary Computation, pp. 825-830

    """


    def set(self):

        self.name = "DTLZ -- 2 test problem"

        self.parameters = [{'name':'x_1', 'bounds': [0, 1]},
                           {'name':'x_2', 'bounds': [0, 1]},
                           {'name':'x_3', 'bounds': [0, 1]},
                           {'name':'x_4', 'bounds': [0, 1]},
                           {'name': 'x_5', 'bounds': [0, 1]},
                           {'name': 'x_6', 'bounds': [0, 1]},
                           {'name': 'x_7', 'bounds': [0, 1]},
                           {'name': 'x_8', 'bounds': [0, 1]},
                           {'name': 'x_9', 'bounds': [0, 1]},
                           {'name': 'x_10', 'bounds': [0, 1]}]

        self.costs = [{'name': 'F_1'},{'name': 'F_2'}]

    def evaluate(self, x):
        # objective values were stored together with decision variables
        problem = optp.Problem(dtlz.DTLZ2(3, 10), num_objectives=3)
        solutions = [optp.Individual(x)]

        problem.batch_evaluate(solutions)
        return solutions[0].objective_values.copy()


def test_problem_2():

    problem = DTLZ2_TEST_Problems()
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 1000
    algorithm.options['max_population_size'] = 100
    algorithm.run()

    b = Results(problem)
    solution = b.pareto_values()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.scatter([s[0] for s in solution],
                [s[1] for s in solution],
                [s[2] for s in solution])
    ax.set_xlim([0, 1.1])
    ax.set_ylim([0, 1.1])
    ax.set_zlim([0, 1.1])

    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")

    ax.view_init(elev=30.0, azim=15.0)
    plt.show()

def test_problem_1():

    problem = DTLZ2_TEST_Problems("DTLZ2")
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

    b = Results(problem)

    solution = b.pareto_values()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.scatter([s[0] for s in solution],
                [s[1] for s in solution],
                [s[2] for s in solution])
    ax.set_xlim([0, 1.1])
    ax.set_ylim([0, 1.1])
    ax.set_zlim([0, 1.1])

    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")

    ax.view_init(elev=30.0, azim=15.0)
    plt.show()


test_problem_2()