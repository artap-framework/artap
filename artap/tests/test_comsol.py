import unittest
import os

from artap.executor import LocalExecutor
from artap.problem import Problem, ProblemType
from artap.algorithm import DummyAlgorithm
from artap.population import Population


class ComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'a': {'initial_value': 10},
                      'b': {'initial_value': 10}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "data" + os.sep)
        self.type = ProblemType.comsol
        self.output_files = ["out.txt"]
        self.executor = LocalExecutor(self,
                                      problem_file="elstat.mph",
                                      output_files=self.output_files)

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self):
        output_file = self.output_files[0]
        path = self.working_dir + output_file
        content = ""
        if os.path.exists(path):
            with open(path) as file:
                content = file.read()
        else:
            self.logger.error(
                "Output file '{}' doesn't exists.".format(path))

        lines = content.split("\n")
        line_with_results = lines[5]  # 5th line contains results
        result = float(line_with_results)
        return [result]


class TestSimpleComsolOptimization(unittest.TestCase):
    def test_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = ComsolProblem("ComsolProblem")

        table = [[10, 10]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])


if __name__ == '__main__':
    unittest.main()
