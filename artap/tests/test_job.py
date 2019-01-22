import unittest
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.individual import Individual
from artap.job import Job


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
        self.options['max_processes'] = 1

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
        problem = TestProblem("Test_Job")
        individual = Individual([1, 2, 2])
        job = Job(problem)
        result = job.evaluate(individual.vector)
        self.assertEqual(result, [9])


if __name__ == '__main__':
    unittest.main()
