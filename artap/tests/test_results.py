import unittest

from ..problem import Problem
from ..algorithm_sweep import SweepAlgorithm
from ..operators import CustomGenerator
from ..results import Results


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "JobProblem"
        self.parameters = {'x_1': {'initial_value': 10}}
        self.costs = ['F_1']

    def evaluate(self, individual):
        result = 0
        for i in individual.vector:
            result += i*i

        return [result]

    def evaluate_constraints(self, individual):
        pass


class TestResults(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def setUp(self):
        self.problem = TestProblem()

        generator = CustomGenerator()
        generator.init([[4.0], [-1.0], [2.0]])

        algorithm = SweepAlgorithm(self.problem, generator=generator)
        algorithm.options['max_processes'] = 2
        algorithm.run()

        self.results = Results(self.problem)

    def test_individuals(self):
        self.assertEqual(len(self.problem.individuals), 3)

        self.assertAlmostEqual(self.problem.individuals[0].vector[0], 4.0)
        self.assertAlmostEqual(self.problem.individuals[1].vector[0], -1.0)
        self.assertAlmostEqual(self.problem.individuals[2].vector[0], 2.0)
        self.assertAlmostEqual(self.problem.individuals[0].costs[0], 16.0)
        self.assertAlmostEqual(self.problem.individuals[1].costs[0], 1.0)
        self.assertAlmostEqual(self.problem.individuals[2].costs[0], 4.0)

    def test_parameter_names(self):
        parameter_names = self.results.parameter_names()
        self.assertEqual(parameter_names[0], "x_1")
