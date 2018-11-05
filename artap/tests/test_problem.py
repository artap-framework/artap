import unittest
from artap.problem import Problem
from artap.algorithm_scipy import ScipyNelderMead
from artap.benchmark_functions import AckleyN2, Ackley4Modified, Rosenbrock


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        result = 0
        for i in x:
            result += i * i

        return result


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = MyProblem("LocalPythonProblem")
        algorithm = ScipyNelderMead(problem)
        algorithm.run()
        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, 0)


class AckleyN2Test(Problem):
    """Test with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x': {'initial_value': 2.13}, 'y': {'initial_value': 2.13}}
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        return AckleyN2.eval(x)


class TestAckleyN2(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = AckleyN2Test("LocalPythonProblem")
        algorithm = ScipyNelderMead(problem)
        algorithm.run()
        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, -200, 3)


class AckleyN4Test(Problem):
    """Test with a simple 2 variable Ackley N4 formula"""

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x': {'initial_value': 1.}, 'y': {'initial_value': -1.}}
        # NOTE: the algorithm finds a local optima if it's starts from [10, 10]
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        return Ackley4Modified.eval(x)


class TestAckleyN4(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = AckleyN4Test("LocalPythonProblem")
        algorithm = ScipyNelderMead(problem)
        algorithm.run()
        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, -4.59, 3)


class RosenbrockTest(Problem):
    """Test with a simple 2 variable Rosenbrock """

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x': {'initial_value': 5.}, 'y': {'initial_value': 5.}}
        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        return Rosenbrock.eval(x)


class TestRosenbrock(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        problem = RosenbrockTest("LocalPythonProblem")
        algorithm = ScipyNelderMead(problem)
        algorithm.run()
        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, 0, 3)


if __name__ == '__main__':
    unittest.main()

