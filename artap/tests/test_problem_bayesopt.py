import unittest

try:
    from artap.algorithm_bayesopt import BayesOptSerial, BayesOptParallel

    __bayes_opt__ = True
except ImportError:
    __bayes_opt__ = False

from artap.results import Results
from artap.benchmark_functions import Booth


class TestBayesOptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    # def test_local_problem_bayesopt_parallel(self):
    #     problem = Booth()
    #     algorithm = BayesOptParallel(problem)
    #     algorithm.options['verbose_level'] = 0
    #     algorithm.options['n_iterations'] = 50
    #     algorithm.run()
    #     # TODO - multiprocess test
    #
    #     results = Results(problem)
    #     optimum = results.find_minimum(name='F')
    #     self.assertAlmostEqual(optimum.costs[0], 0, places=2)

    @unittest.skipIf(__bayes_opt__ is False, "requires module BayesOpt")
    def test_local_problem_bayesopt_serial(self):
        problem = Booth()
        algorithm = BayesOptSerial(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 200
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum(name='F')
        self.assertAlmostEqual(optimum.costs[0], 0, places=2)


if __name__ == '__main__':
    unittest.main()
