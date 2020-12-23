import math
import unittest

from ..problem import Problem
from ..results import Results
from ..surrogate_smt import SurrogateModelSMT
from ..operators import LHSGenerator
from ..algorithm_sweep import SweepAlgorithm
from ..algorithm_nlopt import NLopt, LN_BOBYQA
from ..algorithm_genetic import NSGAII

import numpy as np
from smt.surrogate_models import RBF, MGP


class ProblemBranin(Problem):
    """
    Describe simple one objective optimization problem.
    x_min =  (-pi , 12.275), (pi , 2.275), (9.42478, 2.475), f(x) = 0.397887.
    """

    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 3, 'bounds': [-5, 10]},
                           {'name': 'x_2', 'initial_value': 10, 'bounds': [-5, 15]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector

        # a = 1
        # b = 5.1 / (4 * math.pi**2)
        # c = 5 / math.pi
        # r = 6
        # s = 10
        # t = 1 / (8 * math.pi)
        #
        # term1 = - a * (x[1] - b * x[0]**2 + c * x[0] - r)**2
        # term2 = - s * (1 - t) * math.cos(x[0])
        #
        # y = - term1 + term2 + s

        y = (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2

        return [y]

    def predict(self, individual):
        sigma_MGP, sigma_KRG = self.surrogate.predict_variances(individual.vector, True)

        if sigma_MGP < 1e-6:
            self.surrogate.train_step *= 1.3

            value_problem = self.evaluate(individual)
            value_surrogate = self.surrogate.predict(individual.vector)
            # print(individual.vector, value_problem, value_surrogate, sigma_MGP, sigma_KRG)

            return value_surrogate

        return None


class ProblemSphere1D(Problem):
    """
    Describe simple one objective optimization problem.
    """

    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 5, 'bounds': [-10, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector

        y = x[0]**2

        return [y]

    def predict(self, individual):
        sigma_MGP, sigma_KRG = self.surrogate.predict_variances(individual.vector, True)

        if sigma_MGP < 1.00:
            # value_problem = self.evaluate(individual)
            value_surrogate = self.surrogate.predict(individual.vector)
            # print(individual.vector, value_problem, value_surrogate, sigma_MGP, sigma_KRG)

            return value_surrogate

        return None


class TestSurrogateFunction(unittest.TestCase):
    def test_function(self):
        problem = ProblemBranin()
        # problem = ProblemSphere1D()

        # surrogate
        problem.surrogate = SurrogateModelSMT(problem)
        # set custom regressor
        # problem.surrogate.regressor = RBF(d0=5, print_prediction=False)
        problem.surrogate.regressor = MGP(theta0=[1e-2], n_comp=2, print_prediction=False)

        # DoE - Latin - Hypercube
        gen = LHSGenerator(parameters=problem.parameters)
        gen.init(number=100)

        algorithm_sweep = SweepAlgorithm(problem, generator=gen)
        algorithm_sweep.run()

        # train model
        problem.surrogate.train()

        # set train step
        problem.surrogate.train_step = 50

        # run optimization
        # algorithm = NLopt(problem)
        # algorithm.options['verbose_level'] = 0
        # algorithm.options['algorithm'] = LN_BOBYQA
        # algorithm.options['xtol_abs'] = 1e-6
        # algorithm.options['xtol_rel'] = 1e-3
        # algorithm.options['ftol_rel'] = 1e-3
        # algorithm.options['ftol_abs'] = 1e-6
        # algorithm.options['n_iterations'] = 50
        # algorithm.run()

        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 40
        algorithm.options['max_population_size'] = 10
        algorithm.options['max_processes'] = 10
        algorithm.run()

        b = Results(problem)
        optimum = b.find_optimum('F_1')  # Takes last cost function
        # print(optimum.vector, optimum.costs)
        self.assertGreater(optimum.vector[0], 0.9)
        self.assertLess(optimum.vector[0], 1.1)
        self.assertGreater(optimum.vector[1], 2.8)
        self.assertLess(optimum.vector[1], 3.2)
        self.assertLess(optimum.costs[0], 0.05)
        self.assertGreater(problem.surrogate.predict_counter, 100)

        problem.logger.info("surrogate: predict / eval counter: {0:5.0f} / {1:5.0f}, total: {2:5.0f}".format(
            problem.surrogate.predict_counter,
            problem.surrogate.eval_counter,
            problem.surrogate.predict_counter + problem.surrogate.eval_counter))
