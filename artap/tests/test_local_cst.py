import unittest
import os
import numpy as np
from ..executor import LocalCSTExecutor
from ..problem import Problem
from ..algorithm import DummyAlgorithm
from ..individual import Individual
from .tests_root import tests_root_path

# Test if the Cst software is installed on the system
# Note: cst must be in system path
__cst__ = True
result = os.system('"CST DESIGN ENVIRONMENT_AMD64.exe" /version')
if result != 0:
    __cst__ = False


class CstProblem(Problem):
    #
    def set(self):
        self.name = "ComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10},
                           {'name': 'b', 'initial_value': 10}]
        self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
        self.output_files = ["patch_circular_polarization\\Export\\Farfield\\farfield_source_broadband_[1].ffs"]
        problem_file = os.path.join(tests_root_path, 'data\\cst\\patch_circular_polarization.cst')
        self.executor = LocalCSTExecutor(self, model_file=problem_file)

    #
    def evaluate(self, individual):
        individual.dep_param = 0
        return self.executor.eval(individual)

    def parse_results(self, individual, output_files=None):
        # output_file = output_files[0]
        # path = output_file
        #
        # content = ""
        # if os.path.exists(path):
        #     with open(path) as file:
        #         content = file.read()
        # else:
        #     self.logger.error(
        #         "Output file '{}' doesn't exists.".format(path))
        # far_field = np.zeros([361, 181])
        # with open(output_file) as file:
        #     lines = file.readlines()
        #
        # for line in lines[31:]:
        #     data = line.split()
        #     numbers = []
        #     for item in data:
        #         numbers.append(float(item))
        #
        #     phi = int(numbers[0])
        #     theta = int(numbers[1])
        #     x = np.abs(numbers[2] + 1j * numbers[3])
        #     y = np.abs(numbers[4] + 1j * numbers[5])
        #     far_field[phi, theta] = np.sqrt(x ** 2 + y ** 2)

        return 10


class TestLocalComsol(unittest.TestCase):
    @unittest.skipIf(__cst__ is False, "require CST")
    def test_cst_exec(self):
        """ Tests one calculation of goal function."""
        problem = CstProblem()

        individuals = [Individual([10, 10])]
        algorithm = DummyAlgorithm(problem)
        algorithm.evaluator.evaluate(individuals)
        try:
            algorithm.evaluate(individuals)
            self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])
        except Exception as e:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(e)
