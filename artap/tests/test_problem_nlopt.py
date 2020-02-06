import unittest
import sys

from artap.problem import Problem
try:
    from artap.algorithm_nlopt import NLopt
    from artap.algorithm_nlopt import GN_DIRECT_L
    from artap.algorithm_nlopt import GN_MLSL
    from artap.algorithm_nlopt import GN_CRS2_LM
    from artap.algorithm_nlopt import GN_ISRES
    from artap.algorithm_nlopt import LN_BOBYQA
    from artap.algorithm_nlopt import LN_COBYLA
    from artap.algorithm_nlopt import LN_NELDERMEAD
    from artap.algorithm_nlopt import LN_SBPLX
    from artap.algorithm_nlopt import LN_PRAXIS
    from artap.algorithm_nlopt import LN_AUGLAG_EQ

    __nlopt__ = True
except ImportError:
    __nlopt__ = False

from artap.results import Results
from artap.benchmark_functions import Booth


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "Booth Problem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-10, 10]},
                      {'name': 'x_2', 'initial_value': 1.5, 'bounds': [-10, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        return [Booth.eval(individual.vector)]


class TestNLoptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def run_test(self, method, n_iterations=100):
        try:
            problem = MyProblem()
            algorithm = NLopt(problem)
            algorithm.options['verbose_level'] = 0
            algorithm.options['algorithm'] = method
            algorithm.options['xtol_abs'] = 1e-6
            algorithm.options['xtol_rel'] = 1e-3
            algorithm.options['ftol_rel'] = 1e-3
            algorithm.options['ftol_abs'] = 1e-6
            algorithm.options['n_iterations'] = n_iterations
            algorithm.run()

            results = Results(problem)
            optimum = results.find_minimum('F')
            self.assertAlmostEqual(optimum.costs[0], 0, places=1)
        except AssertionError:
            # try again with more iterations - NLopt - 3rd party library
            self.run_test(method, int(1.5 * n_iterations))

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_GN_DIRECT_L(self):
        self.run_test(GN_DIRECT_L, 400)

    # @unittest.skipUnless(sys.platform.startswith("linux"), "requires linux")
    # def test_local_problem_nlopt_GN_DIRECT_L_RAND(self):
    #    self.run_test(GN_DIRECT_L_RAND, 100)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_GN_MLSL(self):
        self.run_test(GN_MLSL, 500)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_GN_CRS2_LM(self):
        self.run_test(GN_CRS2_LM, 1000)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_GN_ISRES(self):
        self.run_test(GN_ISRES, 1000)

    # @unittest.skipUnless(sys.platform.startswith("linux"), "requires linux")
    # def test_local_problem_nlopt_GN_ESCH(self):
    #     self.run_test(GN_ESCH, 5000)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_BOBYQA(self):
        self.run_test(LN_BOBYQA)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_COBYLA(self):
        self.run_test(LN_COBYLA)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_NELDERMEAD(self):
        self.run_test(LN_NELDERMEAD)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_SBPLX(self):
        self.run_test(LN_SBPLX, 200)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_AUGLAG_EQ(self):
        self.run_test(LN_AUGLAG_EQ)

    @unittest.skipIf(__nlopt__ is False, "requires NLopt")
    def test_local_problem_nlopt_LN_PRAXIS(self):
        self.run_test(LN_PRAXIS)


if __name__ == '__main__':
    unittest.main()
