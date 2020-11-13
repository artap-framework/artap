import unittest
import os
import tempfile
import csv


from ..problem import Problem
from ..algorithm_sweep import SweepAlgorithm
from ..algorithm_genetic import NSGAII
from ..operators import CustomGenerator
from ..results import Results


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 10.0, 'bounds': [-10, 20]},
                           {'name': 'x_2', 'initial_value': 10.0, 'bounds': [-10, 20]}]
        self.costs = [{'name': 'F_1'}]

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
        generator.init([[4.0, 2.0], [-1.0, -3.0], [2.0, 4.0]])

        algorithm = SweepAlgorithm(self.problem, generator=generator)
        algorithm.options['max_processes'] = 1
        algorithm.run()

        self.results = Results(self.problem)

    def test_individuals(self):
        self.assertEqual(len(self.problem.individuals), 3)

        self.assertAlmostEqual(self.problem.individuals[0].vector[0], 4.0)
        self.assertAlmostEqual(self.problem.individuals[1].vector[0], -1.0)
        self.assertAlmostEqual(self.problem.individuals[2].vector[0], 2.0)
        self.assertAlmostEqual(self.problem.individuals[0].vector[1], 2.0)
        self.assertAlmostEqual(self.problem.individuals[1].vector[1], -3.0)
        self.assertAlmostEqual(self.problem.individuals[2].vector[1], 4.0)
        self.assertAlmostEqual(self.problem.individuals[0].costs[0], 20.0)
        self.assertAlmostEqual(self.problem.individuals[1].costs[0], 10.0)
        self.assertAlmostEqual(self.problem.individuals[2].costs[0], 20.0)

    def test_parameter_names(self):
        parameter_names = self.results.parameter_names()
        self.assertEqual(parameter_names[0], "x_1")

    def test_goal_names(self):
        goal_names = self.results.goal_names()
        self.assertEqual(goal_names[0], "F_1")

    def test_parameter_number(self):
        self.assertEqual(self.results.parameter_number(), 2)

    def test_goal_number(self):
        self.assertEqual(self.results.goal_number(), 1)

    def test_parameter_index(self):
        self.assertEqual(self.results.parameter_index('x_2'), 1)

    def test_goal_index(self):
        self.assertEqual(self.results.goal_index('F_1'), 0)

    def test_parameters(self):
        parameters = self.results.parameters()
        self.assertEqual(parameters[0], [4.0, 2.0])
        self.assertEqual(parameters[1], [-1.0, -3.0])
        self.assertEqual(parameters[2], [2.0, 4.0])

    def test_costs(self):
        costs = self.results.costs()
        self.assertEqual(len(costs), 3)
        self.assertEqual(costs[0][0], 20.0)
        self.assertEqual(costs[1][0], 10.0)
        self.assertEqual(costs[2][0], 20.0)

    def test_table(self):
        table = self.results.table(transpose=False)
        self.assertEqual(len(table), 3)
        self.assertEqual(table[1][2], 10.0)

        table = self.results.table(transpose=True)
        self.assertEqual(len(table), 3)
        self.assertEqual(table[1][2], 4.0)

    def test_goal_on_index(self):
        goal_on_index = self.results.goal_on_index("F_1")
        self.assertEqual(goal_on_index[0], [0, 1, 2])
        self.assertEqual(goal_on_index[1], [20.0, 10.0, 20.0])

        goal_on_index = self.results.goal_on_index()
        self.assertEqual(goal_on_index[0], [0, 1, 2])
        self.assertEqual(goal_on_index[1], [20.0, 10.0, 20.0])

    def test_parameter_on_index(self):
        parameter_on_index = self.results.parameter_on_index()
        self.assertEqual(parameter_on_index[0], [0, 1, 2])
        self.assertEqual(parameter_on_index[1], [4.0, -1.0, 2.0])
        self.assertEqual(parameter_on_index[2], [2.0, -3.0, 4.0])

        parameter_on_index = self.results.parameter_on_index("x_2")
        self.assertEqual(parameter_on_index[0], [0, 1, 2])
        self.assertEqual(parameter_on_index[1], [2.0, -3.0, 4.0])

    def test_goal_on_parameter(self):
        goal_on_parameter = self.results.goal_on_parameter("x_1", "F_1", sorted=True)
        self.assertEqual(goal_on_parameter[0], [-1.0, 2.0, 4.0])
        self.assertEqual(goal_on_parameter[1], [10.0, 20.0, 20.0])

        goal_on_parameter = self.results.goal_on_parameter("x_1", "F_1")
        self.assertEqual(goal_on_parameter[0], [4.0, -1.0, 2.0])
        self.assertEqual(goal_on_parameter[1], [20.0, 10.0, 20.0])

    def test_parameter_on_goal(self):
        parameter_on_goal = self.results.parameter_on_goal("F_1", "x_1", sorted=True)
        self.assertEqual(parameter_on_goal[0], [10.0, 20.0, 20.0])
        self.assertEqual(parameter_on_goal[1], [-1.0, 2.0, 4.0])

        parameter_on_goal = self.results.parameter_on_goal("F_1", "x_1")
        self.assertEqual(parameter_on_goal[0], [20.0, 10.0, 20.0])
        self.assertEqual(parameter_on_goal[1], [4.0, -1.0, 2.0])

    def test_parameter_on_parameter(self):
        parameter_on_parameter = self.results.parameter_on_parameter("x_1", "x_2", sorted=True)
        self.assertEqual(parameter_on_parameter[0], [-1.0, 2.0, 4.0])
        self.assertEqual(parameter_on_parameter[1], [-3.0, 4.0, 2.0])

        parameter_on_parameter = self.results.parameter_on_parameter("x_1", "x_2")
        self.assertEqual(parameter_on_parameter[0], [4.0, -1.0, 2.0])
        self.assertEqual(parameter_on_parameter[1], [2.0, -3.0, 4.0])

    def test_pareto_front(self):
        problem = TestProblem()

        algorithm = NSGAII(problem)
        algorithm.options['max_processes'] = 10
        algorithm.options['max_population_number'] = 30
        algorithm.options['max_population_size'] = 10
        algorithm.run()

        results = Results(problem)
        pareto_front = results.pareto_front()
        # print(pareto_front)
        # self.assertEqual()
        pass

    def test_export_to_csv(self):
        csv_filename = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".csv").name
        self.results.export_to_csv(csv_filename)

        with open(csv_filename, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = []
            for row in reader:
                rows.append(row)
            self.assertEqual(rows[0], ['population_id', 'x_1', 'x_2', 'F_1'])
            self.assertEqual(rows[1], ['0', '20.0', '4.0', '2.0'])
            self.assertEqual(rows[2], ['0', '10.0', '-1.0', '-3.0'])
            self.assertEqual(rows[3], ['0', '20.0', '2.0', '4.0'])

        # remove file
        os.remove(csv_filename)

    def test_population(self):
        individuals = self.results.population()
        self.assertEqual(len(individuals), 3)
        self.assertEqual(individuals[1].costs[0], 10.0)

