import unittest
from ..problem import Problem
from ..individual import Individual
from ..job import Job


class JobProblem(Problem):
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

    def evaluate_inequality_constraints(self, x):
        return []


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_individual_evaluation(self):
        problem = JobProblem()
        individual = Individual([1, 2, 2])
        job = Job(problem)
        job.evaluate(individual)
        self.assertEqual(individual.costs, [9])


if __name__ == '__main__':
    unittest.main()
