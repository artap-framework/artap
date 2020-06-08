import unittest
from builtins import int

from artap.benchmark_robust import Synthetic1D, Synthetic2D, Synthetic5D, Synthetic10D
from artap.operators import EpsilonDominance
from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.algorithm import EvaluatorType
from artap.results import Results
from artap.archive import Archive
import numpy as np
import pylab as plt


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_worst_case(self):
        problem = Synthetic1D()
        algorithm = NSGAII(problem, evaluator_type=EvaluatorType.WORST_CASE)
        algorithm.options['max_population_size'] = 200
        algorithm.options['max_population_number'] = 25
        algorithm.run()
        results = Results(problem)
        # an archive to collect the eps-dominated solutions
        # archive = Archive(dominance=EpsilonDominance(epsilons=[0.0001, 0.00001]))
        archive = Archive()
        # archive.extend(problem.populations[-1].individuals)
        # archive += problem.populations[-1].individuals
        problem.plot_1d()
        for individual in problem.populations[-1].individuals:
            archive += individual
            if individual.features['front_number'] == 1:
                print(individual)
                x = individual.vector[0]
                y = individual.costs[0]
                plt.plot(x, y, 'rx')

                for child in individual.children:
                    print('  ', child)
                    x = child.vector[0]
                    y = child.costs[0]
                    plt.plot(x, y, 'bx')

        plt.show()
        for individual in archive:
            print(individual)



if __name__ == '__main__':
    unittest.main()
