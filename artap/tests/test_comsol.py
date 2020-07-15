# import unittest
# import os
#
# from ..executor import LocalComsolExecutor
# from ..problem import Problem
# from ..algorithm import DummyAlgorithm
# from ..individual import Individual
# from .tests_root import tests_root_path
# __comsol__ = True
# result = os.system('comsol --version')
# if result != 0:
#     __comsol__ = False
#
#
# class ComsolProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#
#     def set(self):
#         self.name = "ComsolProblem"
#         self.parameters = [{'name': 'a', 'initial_value': 10},
#                            {'name': 'b', 'initial_value': 10}]
#         self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
#         self.output_files = ["out.txt"]
#         problem_file = os.path.join(tests_root_path, './data/elstat.mph')
#         self.executor = LocalComsolExecutor(self,
#                                             problem_file=problem_file,
#                                             output_files=self.output_files)
#
#     def evaluate(self, individual):
#         individual.dep_param = 0
#         return self.executor.eval(individual)
#
#     def parse_results(self, output_files, individual):
#         output_file = output_files[0]
#         path = output_file
#         content = ""
#         if os.path.exists(path):
#             with open(path) as file:
#                 content = file.read()
#         else:
#             self.logger.error(
#                 "Output file '{}' doesn't exists.".format(path))
#
#         lines = content.split("\n")
#         line_with_results = lines[5]  # 5th line contains results
#         result = float(line_with_results)
#         return [result]
#
#
# class TestLocalComsol(unittest.TestCase):
#     @unittest.skipIf(__comsol__ is False, "require Comsol Multiphysics")
#     def test_comsol_exec(self):
#         """ Tests one calculation of goal function."""
#         problem = ComsolProblem()
#
#         individuals = [Individual([10, 10])]
#         algorithm = DummyAlgorithm(problem)
#         algorithm.evaluator.evaluate(individuals)
#         try:
#             algorithm.evaluate(individuals)
#             self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])
#         except Exception as e:
#             print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#             print(e)
