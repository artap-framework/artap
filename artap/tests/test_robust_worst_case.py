import unittest

from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.algorithm import EvaluatorType


class RobustnessProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "ComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'tol': 1e-1},
                           {'name': 'b', 'initial_value': 10, 'tol': 1e-1}]
        self.costs = [{'name': 'F1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x_1 = individual.vector[0]
        x_2 = individual.vector[1]
        return [x_1**2 + x_2**2]


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_gradient(self):
        problem = RobustnessProblem()
        algorithm = ScipyOpt(problem, evaluator_type=EvaluatorType.GRADIENT)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        for individual in problem.populations[0].individuals:
            print(individual.features['gradient'])
            for child in individual.children:
                print(child)
            print("-------------------------")

    def test_worst_case(self):
        problem = RobustnessProblem()
        algorithm = ScipyOpt(problem, evaluator_type=EvaluatorType.WORST_CASE)
        algorithm.options['algorithm'] = 'Nelder-Mead'
        algorithm.options['tol'] = 1e-4
        algorithm.run()

        for individual in problem.populations[0].individuals:
            print(individual)
            for child in individual.children:
                print(child)
            print("-------------------------")


if __name__ == '__main__':
    unittest.main()
