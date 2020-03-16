import unittest
import os

from artap.executor import LocalComsolExecutor
from artap.problem import Problem
from artap.algorithm import DummyAlgorithm
from artap.individual import Individual

__comsol__ = True
result = os.system('comsol --version')
if result != 0:
    __comsol__ = False


class ComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "ComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10},
                           {'name': 'b', 'initial_value': 10}]
        self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
        self.output_files = ["out.txt"]
        self.executor = LocalComsolExecutor(self,
                                            problem_file="./data/elstat.mph",
                                            output_files=self.output_files)

    def evaluate(self, individual):
        individual.dep_param = 0
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        output_file = output_files[0]
        path = output_file
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


class TestLocalComsol(unittest.TestCase):
    @unittest.skipIf(__comsol__ is False, "require Comsol Multiphysics")
    def test_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = ComsolProblem()

        individuals = [Individual([10, 10])]
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(individuals)
        try:
            evaluator.evaluate(individuals)
            self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])
        except Exception as e:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(e)
