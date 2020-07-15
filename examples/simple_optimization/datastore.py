# import tempfile
#
# from artap.problem import Problem
# from artap.datastore import JsonDataStore
# from artap.algorithm_genetic import NSGAII
#
#
# class MyProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#     def set(self):
#         self.name = "NLopt_BOBYQA"
#         self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-10, 10]},
#                            {'name': 'x_2', 'initial_value': 1.5, 'bounds': [-10, 10]}]
#         self.costs = [{'name': 'F1', 'criteria': 'minimize'},
#                       {'name': 'F2', 'criteria': 'minimize'}]
#
#     def evaluate(self, individual):
#         x_1 = individual.vector[0]
#         x_2 = individual.vector[1]
#
#         # set custom properties
#         individual.custom["functions"] = [x_1**2, x_2**2]
#
#         return [x_1**2, x_2**2]
#
#
# problem = MyProblem()
#
# # set data store
# database_name = 'pokus'
# problem.data_store = JsonDataStore(problem, database_name=database_name)
#
# algorithm = NSGAII(problem)
# algorithm.options['max_population_number'] = 1
# algorithm.options['max_population_size'] = 1  # according to the literature
# algorithm.options['max_processes'] = 20
# algorithm.options['verbose_level'] = 0
# algorithm.run()
#
# problem.data_store = JsonDataStore(problem, database_name=database_name, mode='read')
