import unittest

from artap.problem import Problem
from artap.algorithm_nlopt import NLopt
from artap.algorithm_nlopt import LN_BOBYQA
from artap.algorithm_nlopt import LN_NELDERMEAD

from artap.benchmark_functions import Rosenbrock

class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-30, 30], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-30, 30], 'precision': 1e-1}}
        costs = ['F']

        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        return Rosenbrock.eval(x)


class TestBayesOptOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem_nlopt_bobyqa(self):
        problem = MyProblem("LocalPythonProblemNLopt_LN_BOBYQA")
        algorithm = NLopt(problem)
        algorithm.options['verbose_level'] = 1
        algorithm.options['algorithm'] = LN_BOBYQA
        algorithm.options['n_iterations'] = 200
        algorithm.run()
        # TODO: population.find_min

    def test_local_problem_nlopt_ln_neldermead(self):
        problem = MyProblem("LocalPythonProblemNLopt_LN_NELDERMEAD")
        algorithm = NLopt(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['algorithm'] = LN_NELDERMEAD
        algorithm.options['n_iterations'] = 150
        algorithm.run()
        # TODO: population.find_min

if __name__ == '__main__':
    unittest.main()
