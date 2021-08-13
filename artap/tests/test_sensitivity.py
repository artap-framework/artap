import unittest

from ..problem import Problem
from ..algorithm_sensitivity import SALibAlgorithm

import math


class SensitivitySALibProblem(Problem):
    def set(self):
        self.name = "SensitivityTestProblem"
        self.parameters = [{'name': 'A', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]},
                           {'name': 'B', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]},
                           {'name': 'C', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]}]

        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        return [math.sin(individual.vector[0]) + 7.0 * math.sin(individual.vector[1])**2 + \
                0.1 * individual.vector[2]**4 * math.sin(individual.vector[0])]


class TestSALibSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_sobol_problem(self):
        problem = SensitivitySALibProblem()
        problem.options['save_data_files'] = True

        algorithm = SALibAlgorithm(problem)
        algorithm.options["samples"] = 1024
        algorithm.options["method"] = "sobol"
        algorithm.options["print_to_console"] = True
        algorithm.run()

        res = algorithm.analyze()

        self.assertAlmostEqual(res["S1"][0], 0.30797525, 2)
        self.assertAlmostEqual(res["S1"][1], 0.44776754, 2)
        self.assertAlmostEqual(res["S1"][2], -0.00425456, 2)


if __name__ == '__main__':
    unittest.main()
