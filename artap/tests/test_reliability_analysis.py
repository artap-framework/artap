import unittest
from ..algorithm_NSGAII import NSGAII
from ..benchmark_functions import Sphere
from ..results import Results

# ToDo: Ask for another goal function
# class Limit_State(Problem):
#
#     def set(self, **kwargs):
#         """Time-dependent 1D QM wave function of a single particle - squared."""
#         self.parameters = [{'name': 'x_1', 'bounds': [0, 100], 'parameter_type': 'float'},
#                            {'name': 'x_2', 'bounds': [0, 100], 'parameter_type': 'float'}]
#         self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]
#
#     def evaluate(self, individual):
#         X = individual.vector
#         x1 = X[0]
#         x2 = X[1]
#         res = x1 ** 3 + x2 ** 3 - 18
#         return [res]


class Test_FORM(unittest.TestCase):
    def test_local_problem(self):
        problem = Sphere(**{'dimension': 1})
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 10
        algorithm.run()

        result = Results(problem)
        optimal = result.find_optimum('f_1')
        x, reliability_index = result.form_reliability(problem, optimal)
        print(reliability_index)
        self.assertAlmostEqual(x[0], 0.0, places=1)
