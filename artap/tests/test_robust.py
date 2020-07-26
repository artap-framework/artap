import unittest

from ..benchmark_robust import Synthetic1D
from ..algorithm_genetic import EpsMOEA
from ..algorithm import EvaluatorType
from ..results import Results
from ..archive import Archive


# Make test to test something
class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_worst_case(self):
        # problem = Synthetic1D()
        problem = Synthetic1D()
        algorithm = EpsMOEA(problem, evaluator_type=EvaluatorType.WORST_CASE)
        algorithm.options['max_population_size'] = 50
        algorithm.options['max_population_number'] = 10
        algorithm.run()
        # an archive to collect the eps-dominated solutions
        # archive = Archive(dominance=EpsilonDominance(epsilons=[0.0001, 0.00001]))
        archive = Archive()
        # archive.extend(problem.populations[-1].individuals)
        # archive += problem.populations[-1].individuals

        for individual in problem.last_population():
            archive += individual

            for child in individual.children:
                x_1 = child.vector[0]
                y = child.costs[0]


if __name__ == '__main__':
    unittest.main()

