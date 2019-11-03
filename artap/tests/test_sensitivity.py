import unittest

from artap.problem import Problem
from artap.algorithm_sensitivity import Sensitivity, SALibAlgorithm

import math


class SensitivitySALibProblem(Problem):
    def set(self):
        self.name = "SensitivityTestProblem"
        self.parameters = [{'name': 'A', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]},
                           {'name': 'B', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]},
                           {'name': 'C', 'initial_value': 0.0, 'bounds': [-3.14159, 3.14159]}]

        self.costs = [{'name': 'F_1'}]
        # self.executor = CondorComsolJobExecutor(self, model_file="./data/coil_linear_current.mph",
        #                                        files_from_condor=["temp.txt"])

    def evaluate(self, individual):
        return [math.sin(individual.vector[0]) + 7.0 * math.pow(math.sin(individual.vector[1]), 2) + \
                0.1 * math.pow(individual.vector[2], 4) * math.sin(individual.vector[0])]


class TestSALibSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_sobol_problem(self):
        problem = SensitivitySALibProblem()
        problem.options['save_data_files'] = True

        algorithm = SALibAlgorithm(problem)
        algorithm.options["samples"] = 1000
        algorithm.options["method"] = "sobol"
        algorithm.options["print_to_console"] = False
        algorithm.run()

        res = algorithm.analyze()
        self.assertAlmostEqual(res["S1"][0], 0.30797525)
        self.assertAlmostEqual(res["S1"][1], 0.44776754)
        self.assertAlmostEqual(res["S1"][2], -0.00425456)


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "LocalPythonProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                           {'name': 'x_2', 'initial_value': 2.5, 'bounds': [2.2, 2.4], 'precision': 1e-1},
                           {'name': 'x_3', 'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        result = x[0] * x[0] + 0.1 * x[1] * x[1] + x[2] * x[2]
        return [result]


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem()
        algorithm = Sensitivity(problem, ['x_2', 'x_3'])
        algorithm.options['max_population_size'] = 10
        algorithm.run()


if __name__ == '__main__':
    unittest.main()
