import math
import unittest

from artap.problem import Problem
from artap.benchmark_functions import Booth
from artap.surrogate import SurrogateModelEval, SurrogateModelGaussianProcess

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel as C


class MyProblemSin(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 10]}}

        costs = ['F']

        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def evaluate(self, x):
        return [x[0] * math.sin(x[0])]


class MyProblemBooth(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10]},
                      'x_2': {'initial_value': 1.5, 'bounds': [-10, 10]}}

        costs = ['F']

        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def evaluate(self, x):
        return [Booth.eval(x)]


class TestSurrogate(unittest.TestCase):

    def check_one(self, problem):
        problem.surrogate.options['train_step'] = 7

        # train
        for val in [1., 2., 3., 5., 6., 7., 8.]:
            problem.surrogate.evaluate([val])

        x_ref = [4.9]
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.evaluate(x_ref)[0]

        problem.logger.info("surrogate.counter: evaluation = {}, prediction = {}".format(problem.surrogate.eval_counter, problem.surrogate.predict_counter))
        problem.logger.info("surrogate.value: evaluation = {}, prediction = {}, difference = {}".format(value_problem, value_surrogate, math.fabs(value_problem - value_surrogate)))

        self.assertTrue(problem.surrogate.predict_counter > 0)
        self.assertLess(math.fabs(value_problem - value_surrogate), 0.025)

    def test_eval(self):
        problem = MyProblemBooth("MyProblemBooth")
        problem.surrogate = SurrogateModelEval(problem)

        x_ref = [2.5, 1.5]
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.evaluate(x_ref)[0]

        self.assertLess(math.fabs(value_problem - value_surrogate), 1e-8)

    def test_gaussian_process_one(self):
        problem = MyProblemSin("MyProblemSin")
        problem.surrogate = SurrogateModelGaussianProcess(problem)
        # default kernel
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-6, 3e2))
        problem.surrogate.regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
        problem.surrogate.options['sigma_threshold'] = 0.05

        self.check_one(problem)

    def xtest_gaussian_process_two(self):
        problem = MyProblemBooth("MyProblemBooth")
        problem.surrogate = SurrogateModelGaussianProcess(problem)
        # set custom regressor
        # kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-6, 3e2))
        kernel = 1.0 * RBF(length_scale=100.0, length_scale_bounds=(1e-2, 1e3))
        problem.surrogate.regressor = GaussianProcessRegressor(kernel=kernel, alpha=0.0)

        # train
        problem.surrogate.evaluate([1.0, 3.1])
        problem.surrogate.evaluate([1.3, 3.2])
        problem.surrogate.evaluate([1.8, 2.7])
        problem.surrogate.evaluate([0.9, 3.3])
        problem.surrogate.evaluate([0.8, 3.1])
        problem.surrogate.evaluate([1.4, 2.8])
        problem.surrogate.evaluate([0.1, 3.0])
        problem.surrogate.evaluate([0.2, 3.4])
        problem.surrogate.evaluate([0.95, 3.03])
        problem.surrogate.evaluate([0.98, 2.96])
        problem.surrogate.evaluate([1.02, 2.98])
        problem.surrogate.evaluate([1.01, 2.99])

        # set threshold
        problem.surrogate.options['sigma_threshold'] = 2.0
        problem.surrogate.options['train_step'] = 12

        x_ref = [1.01, 3.02]
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.evaluate(x_ref)[0]

        problem.logger.info("surrogate.counter: evaluation = {}, prediction = {}".format(problem.surrogate.eval_counter, problem.surrogate.predict_counter))
        problem.logger.info("surrogate.value: evaluation = {}, prediction = {}, difference = {}".format(value_problem, value_surrogate, math.fabs( value_problem - value_surrogate)))

        self.assertTrue(problem.surrogate.predict_counter > 0)
        self.assertLess(math.fabs(value_problem - value_surrogate), 0.03)


if __name__ == '__main__':
    unittest.main()
