import unittest
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.individual import Individual
from artap.population import Population
from artap.job import JobSimple


class JobProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]

    def evaluate_constraints(self, x):
        pass


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_individual_evaluation(self):
        problem = JobProblem("JobProblem")
        individual = Individual([1, 2, 2])
        job = JobSimple(problem)
        job.evaluate(individual)
        self.assertEqual(individual.costs, [9])


if __name__ == '__main__':
    unittest.main()
