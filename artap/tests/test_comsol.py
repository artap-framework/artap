import unittest
import os

from artap.executor import ComsolExecutor
from artap.problem import Problem
from artap.algorithm import DummyAlgorithm
from artap.population import Population

class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'a': {'initial_value': 10},
                      'b': {'initial_value': 10}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "workspace" + os.sep + "comsol" + os.sep)

        self.executor = ComsolExecutor(self,
                                       model_file="elstat.mph",
                                       output_file="out.txt")

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        lines = content.split("\n")
        line_with_results = lines[5]  # 5th line contains results
        result = float(line_with_results)
        return [result]


class TestSimpleComsolOptimization(unittest.TestCase):
    def test_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = TestProblem("CondorComsolProblem")

        table = [[10, 10]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        population.individuals = evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])


if __name__ == '__main__':
    unittest.main()
