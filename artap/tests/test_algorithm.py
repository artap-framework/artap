import unittest
from artap.problem import Problem
from artap.individual import Individual
from artap.operators import CustomGeneration, LHCGeneration
from artap.algorithm import DummyAlgorithm
from artap.algorithm_sweep import SweepAlgorithm


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10, 'bounds': [-10, 30]}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_sweep_evaluate_parallel(self):
        problem = TestProblem("Test_Job")

        gen = LHCGeneration(problem.parameters)
        gen.init(4)

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.options['max_processes'] = 2
        algorithm.run()

        individuals = problem.data_store.individuals
        # values
        self.assertEqual(len(individuals), 4)
        self.assertTrue(problem.parameters['x_1']['bounds'][0] <= individuals[0].vector[0] <= problem.parameters['x_1']['bounds'][1] and
                        problem.parameters['x_1']['bounds'][0] <= individuals[1].vector[0] <= problem.parameters['x_1']['bounds'][1] and
                        problem.parameters['x_1']['bounds'][0] <= individuals[2].vector[0] <= problem.parameters['x_1']['bounds'][1] and
                        problem.parameters['x_1']['bounds'][0] <= individuals[3].vector[0] <= problem.parameters['x_1']['bounds'][1])

    def test_sweep_evaluate_serial(self):
        problem = TestProblem("Test_Job")

        gen = CustomGeneration(problem.parameters)
        gen.init([[1, 2, 2], [3, 3, 2]])

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.run()

        individuals = problem.data_store.individuals
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])

    def test_dummy_evaluate_serial(self):
        problem = TestProblem("Test_Job")

        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])

        algorithm = DummyAlgorithm(problem)

        individuals = algorithm.evaluate(individuals=[i1, i2])
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])

    def test_dummy_evaluate_parallel(self):
        problem = TestProblem("Test_Job")

        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])

        algorithm = DummyAlgorithm(problem)
        algorithm.options['max_processes'] = 2

        individuals = algorithm.evaluate(individuals=[i1, i2])
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])


if __name__ == '__main__':
    unittest.main()
