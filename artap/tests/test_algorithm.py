import unittest
from artap.problem import Problem
from artap.datastore import DummyDataStore
from artap.individual import Individual
from artap.algorithm import EvalAll


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_evaluate_serial(self):
        problem = TestProblem("Test_Job")
        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])
        algorithm = EvalAll(problem)
        individuals = algorithm.evaluate(individuals=[i1, i2])
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])

    def test_evaluate_parallel(self):
        problem = TestProblem("Test_Job")
        problem.options['max_processes'] = 4
        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])
        algorithm = EvalAll(problem)
        individuals = algorithm.evaluate(individuals=[i1, i2])
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])


if __name__ == '__main__':
    unittest.main()
