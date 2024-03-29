import unittest
import os

from ..executor import LocalFEMMExecutor
from ..problem import Problem
from ..results import Results
from ..algorithm_sweep import SweepAlgorithm
from ..operators import CustomGenerator

from distutils.spawn import find_executable
path = find_executable('femm')
__femm__ = path is not None


class FEMMProblem(Problem):
    def set(self):
        self.name = "FEMMProblem"
        # Parameters must be defined in the FEMM model
        # pp = 0.8 -- relative pole pitch: 0.4 - 0.99
        # p_offset = 0.8 -- relative offset: 0 - 0.99
        self.parameters = [{'name': 'pp', 'initial_value': 0.8, 'bounds': [0.5, 0.9]},
                           {'name': 'p_offset', 'initial_value': 0.8, 'bounds': [0.5, 0.9]}]

        self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
        self.output_files = ["output.txt"]

        # Executor serves for calling the FEMM
        self.executor = LocalFEMMExecutor(self,
                                          script_file="artap/tests/data/femm/femm_test.lua",
                                          output_files=["output.txt"])

    # Calculate the value of the objective function
    def evaluate(self, individual):
        cog = self.executor.eval(individual)[0]  # method evaluate must return list
        if cog < 1.:
            cog = 1e10
        return [cog]

    # This method processes files generated by 3rd party software, depends on files format
    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
            content = content[0]
            content = content.split(',')
            content = [float(i) for i in content[:-1]]
            cogging_torque = max(content) - min(content)

        return [cogging_torque]


class TestLocalFEMM(unittest.TestCase):
    @unittest.skipIf(__femm__ is False, "require FEMM")
    def test_femm_exec(self):
        """ Tests one calculation of goal function."""
        problem = FEMMProblem()

        # DoE - Latin - Hypercube
        gen = CustomGenerator(problem.parameters)
        gen.init([[0.8, 0.7]])

        algorithm_sweep = SweepAlgorithm(problem, generator=gen)
        algorithm_sweep.run()

        # Post - processing the results
        results = Results(problem)

        individual = results.find_optimum()
        print(individual.vector)
        self.assertAlmostEqual(457.88, individual.costs[0], places=1)

