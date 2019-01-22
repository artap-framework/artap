# import os
# import unittest
#
# from artap.problem import Problem
# from artap.algorithm_bayesopt import BayesOptSerial, BayesOptParallel
#
# from artap.results import Results
# from artap.datastore import DummyDataStore
# from artap.benchmark_functions import Booth
#
#
# class MyProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#     def __init__(self, name):
#         parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-30, 30], 'precision': 1e-1},
#                       'x_2': {'initial_value': 1.5, 'bounds': [-30, 30], 'precision': 1e-1}}
#         costs = ['F']
#
#         super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
#         self.options['max_processes'] = 1
#
#     def evaluate(self, x):
#         return [Booth.eval(x)]
#
#
# class TestBayesOptOptimization(unittest.TestCase):
#     """ Tests simple one objective optimization problem."""
#
#     def xtest_local_problem_bayesopt_parallel(self):
#         problem = MyProblem("TestBayesOptParallel")
#         algorithm = BayesOptParallel(problem)
#         algorithm.options['verbose_level'] = 0
#         algorithm.options['n_iterations'] = 100
#         algorithm.run()
#         # TODO - multiprocess test
#
#         # results = Results(problem)
#         # optimum = results.find_minimum(name='F')
#         # self.assertAlmostEqual(optimum, 0, places=2)
#
#     def test_local_problem_bayesopt_serial(self):
#         problem = MyProblem("TestBayesOptSerial")
#         algorithm = BayesOptSerial(problem)
#         algorithm.options['verbose_level'] = 0
#         algorithm.options['n_iterations'] = 200
#         algorithm.run()
#
#         results = Results(problem)
#         optimum = results.find_minimum(name='F')
#         self.assertAlmostEqual(optimum, 0, places=2)
#
#
# if __name__ == '__main__':
#     unittest.main()
