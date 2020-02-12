import unittest
import os

from artap.executor import LocalComsolExecutor
from artap.problem import Problem, ProblemType
from artap.algorithm import DummyAlgorithm
from artap.population import Population

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
        self.type = ProblemType.comsol
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


class TestSimpleComsolOptimization(unittest.TestCase):

    @unittest.skipIf(__comsol__ is False, "require Comsol Multiphysics")
    def test_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = ComsolProblem()
        table = [[10, 10]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])


if __name__ == '__main__':
    unittest.main()
