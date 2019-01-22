# import os
# from unittest import TestCase, main
# import getpass
#
# from artap.executor import CondorComsolJobExecutor
# from artap.problem import Problem
# from artap.datastore import DummyDataStore
# from artap.enviroment import Enviroment
# from artap.population import Population
#
#
# class TestProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#
#     def __init__(self, name):
#
#         parameters = {'a': {'initial_value': 10, 'bounds': [1, 5], 'precision': 1e-1},
#                       'b': {'initial_value': 10, 'bounds': [10, 15], 'precision': 1e-1}}
#         costs = ['F1']
#         working_dir = "." + os.sep + "workspace" + os.sep + "condor_comsol" + os.sep
#
#         super().__init__(name, parameters, costs, working_dir=working_dir, data_store=DummyDataStore(self))
#         self.options['max_processes'] = 10
#
#         output_files = ["out.txt"]
#         model_file = "elstat.mph"
#
#         # current username
#         if Enviroment.condor_host_login == "":
#             user = getpass.getuser()
#         else:
#             user = Enviroment.condor_host_login
#         # host
#
#         host = Enviroment.condor_host_ip
#
#         self.executor = CondorComsolJobExecutor(parameters, model_file, output_files,
#                                                 username=user, hostname=host, working_dir=working_dir)
#
#         self.executor.parse_results = self.parse_results
#
#     def evaluate(self, x):
#         result = self.executor.eval(x)
#         return [result]
#
#     def parse_results(self, content, x):
#         lines = content.split("\n")
#         line_with_results = lines[5]  # 5th line contains results
#         result = float(line_with_results)
#         return [result]
#
#
# class TestCondor(TestCase):
#     """ Tests simple optimization problem where calculation of
#         goal function is submitted as a job on HtCondor.
#     """
#
#     def test_condor_run(self):
#         """ Tests one calculation of goal function."""
#         problem = TestProblem("Condor Comsol Problem")
#         population = Population(problem)
#         # population.gen_random_population(15, len(problem.vector),
#         #                                  problem.vector)
#
#         table = [[10, 10], [11, 11]]
#         population.gen_population_from_table(table)
#         population.evaluate()
#         # population.evaluate_gradients()
#         population.save()
#
#
# if __name__ == '__main__':
#     main()
