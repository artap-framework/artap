import unittest
import os

from artap.datastore import DummyDataStore
from artap.executor import ComsolExecutor
from artap.problem import Problem
from artap.job import Job


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'a': {'initial_value': 10},
                      'b': {'initial_value': 10}}
        costs = ['F1']
        working_dir = "." + os.sep + "workspace" + os.sep + "condor" + os.sep

        super().__init__(name, parameters, costs, working_dir=working_dir)

        curr_dir = os.path.abspath(os.curdir)
        output_file = curr_dir + os.sep + "workspace" + os.sep + "comsol" + os.sep + "max.txt"
        model_file = curr_dir + os.sep + "workspace" + os.sep + "comsol" + os.sep + "elstat.mph"

        self.executor = ComsolExecutor(parameters, model_file, output_file)

    def evaluate(self, x: list):
        result = self.executor.eval(x)
        return [result]


class TestSimpleComsolOptimization(unittest.TestCase):
    def cluster_disabled_test_upper(self):
        problem = TestProblem("LocalComsolProblem")
        job = Job(problem)
        result = job.evaluate([1, 1])
        self.assertAlmostEqual(result[0], 11.294090668382257)


if __name__ == '__main__':
    unittest.main()
