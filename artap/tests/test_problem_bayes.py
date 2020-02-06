import unittest

from artap.problem import Problem

from artap.algorithm_bayes import Bayes, BayesianOptimization

from artap.benchmark_functions import Booth

import numpy as np


# PBOUNDS = {'p1': (-10, 10), 'p2': (-10, 10)}
PBOUNDS = {'x': (-2, 10)}


def target_func(x):
    # val = sum(x)
    # val = -Booth.eval(x)
    val = np.exp(-(x - 2)**2) + np.exp(-(x - 6)**2/10) + 1/ (x**2 + 1)
    # print(val, x)
    return val


class MyProblemOne(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "TestBayesOptParallel"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-2, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        return -(np.exp(-(x - 2)**2) + np.exp(-(x - 6)**2/10) + 1 / (x**2 + 1))


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "TestBayesOptSerial"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-10, 10]},
                      {'name': 'x_2', 'initial_value': 1.5, 'bounds': [-10, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        return [Booth.eval(individual.vector)]


class TestBayesOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_bayesoptimization(self):
        optimizer = BayesianOptimization(f=target_func,
                                         pbounds=PBOUNDS,
                                         random_state=np.random.RandomState(1))

        optimizer.maximize(init_points=5, n_iter=30, acq="ucb", kappa=10.0)
        print("maximum")
        print(optimizer.max)


if __name__ == '__main__':
    unittest.main()
