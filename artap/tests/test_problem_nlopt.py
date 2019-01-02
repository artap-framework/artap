import unittest

from artap.problem import Problem
from artap.algorithm_nlopt import NLopt
from artap.algorithm_nlopt import GN_DIRECT_L
from artap.algorithm_nlopt import GN_DIRECT_L_RAND
from artap.algorithm_nlopt import GN_MLSL
from artap.algorithm_nlopt import GN_CRS2_LM
from artap.algorithm_nlopt import GN_ISRES
from artap.algorithm_nlopt import GN_ESCH
from artap.algorithm_nlopt import LN_BOBYQA
from artap.algorithm_nlopt import LN_COBYLA
from artap.algorithm_nlopt import LN_NELDERMEAD
from artap.algorithm_nlopt import LN_SBPLX
from artap.algorithm_nlopt import LN_PRAXIS
from artap.algorithm_nlopt import LN_AUGLAG_EQ

from artap.results import Results

from artap.benchmark_functions import Booth


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-10, 10], 'precision': 1e-1}}

        # costs = {'F': {'type': Problem.MINIMIZE, 'value': 0.0}}
        costs = ['F']
        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def eval(self, x):
        return Booth.eval(x)


class TestNLoptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def run_test(self, method, n_iterations=100):
        problem = MyProblem("LocalPythonProblemNLopt")
        algorithm = NLopt(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['algorithm'] = method
        algorithm.options['xtol_abs'] = 1e-6
        algorithm.options['xtol_rel'] = 1e-3
        algorithm.options['ftol_rel'] = 1e-3
        algorithm.options['ftol_abs'] = 1e-6
        algorithm.options['n_iterations'] = n_iterations
        algorithm.run()

        # optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum, 0, places=1)

    def test_local_problem_nlopt_GN_DIRECT_L(self):
        self.run_test(GN_DIRECT_L, 400)

    # def test_local_problem_nlopt_GN_DIRECT_L_RAND(self):
    #    self.run_test(GN_DIRECT_L_RAND, 100)

    def test_local_problem_nlopt_GN_MLSL(self):
        self.run_test(GN_MLSL, 500)

    def test_local_problem_nlopt_GN_CRS2_LM(self):
        self.run_test(GN_CRS2_LM, 1000)

    def test_local_problem_nlopt_GN_ISRES(self):
        self.run_test(GN_ISRES, 3000)

    def test_local_problem_nlopt_GN_ESCH(self):
        self.run_test(GN_ESCH, 30000)

    def test_local_problem_nlopt_LN_BOBYQA(self):
        self.run_test(LN_BOBYQA)

    def test_local_problem_nlopt_LN_COBYLA(self):
        self.run_test(LN_COBYLA)

    def test_local_problem_nlopt_LN_NELDERMEAD(self):
        self.run_test(LN_NELDERMEAD)

    def test_local_problem_nlopt_LN_SBPLX(self):
        self.run_test(LN_SBPLX, 200)

    def test_local_problem_nlopt_LN_AUGLAG_EQ(self):
        self.run_test(LN_AUGLAG_EQ)

    def test_local_problem_nlopt_LN_PRAXIS(self):
        self.run_test(LN_PRAXIS)

if __name__ == '__main__':
    unittest.main()
