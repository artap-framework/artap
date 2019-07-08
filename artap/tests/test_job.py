import unittest
from artap.problem import Problem
from artap.individual import Individual
from artap.job import JobSimple


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

    def evaluate_constraints(self, individual):
        pass


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_individual_evaluation(self):
        problem = JobProblem()
        individual = Individual([1, 2, 2])
        job = JobSimple(problem)
        job.evaluate(individual)
        self.assertEqual(individual.costs, [9])


if __name__ == '__main__':
    unittest.main()
