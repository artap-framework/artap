import math
import unittest

from ..problem import Problem
from ..individual import Individual
from ..benchmark_functions import Booth
from ..surrogate import SurrogateModelEval
from ..surrogate_scikit import SurrogateModelScikit
from ..operators import LHSGenerator
from ..algorithm_sweep import SweepAlgorithm

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RationalQuadratic, ExpSineSquared
# from sklearn.gaussian_process.kernels RBF, Matern, DotProduct, WhiteKernel, ConstantKernel
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor, GradientBoostingRegressor


class MyProblemSin(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        return [x[0] * math.sin(x[0])]


class TestSurrogateScikit(unittest.TestCase):
    def _check_scikit_one(self, problem, threshold=5.0):
        xmeas = [0., 0.5, 1., 2., 3., 4., 5., 5.4, 6., 7., 7.7, 8., 10.]

        problem.surrogate.train_step = len(xmeas)

        # train
        for val in xmeas:
            problem.surrogate.evaluate(Individual([val]))

        x_ref = Individual([5.1])
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]

        # more steps - some methods are stochastic
        step = 1
        while True:
            # eval surrogate
            value_surrogate = problem.surrogate.predict(x_ref.vector)[0]

            percent = 100.0 * math.fabs(value_problem - value_surrogate) / math.fabs(value_problem)
            problem.logger.info("{}: surrogate.value: step {})".format(problem.name, step))
            problem.logger.info(
                "{}: eval = {}, pred = {}, diff = {} ({} %)".format(problem.name, value_problem, value_surrogate,
                                                                    math.fabs(value_problem - value_surrogate),
                                                                    percent))
            problem.logger.info("{}: score = {}, lml = {}, lml_grad = {}".format(problem.name, problem.surrogate.score,
                                                                                 problem.surrogate.lml,
                                                                                 problem.surrogate.lml_gradient))

            if percent < threshold:
                self.assertLess(percent, threshold)
                break
            else:
                problem.surrogate.train()
                step += 1

    def test_eval(self):
        problem = Booth()
        problem.surrogate = SurrogateModelEval(problem)

        x_ref = Individual([2.5, 1.5])
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.predict(x_ref)[0]

        problem.logger.info(
            "{}: surrogate.value: evaluation = {}, prediction = {}, difference = {}".format(problem.name,
                                                                                            value_problem,
                                                                                            value_surrogate,
                                                                                            math.fabs(value_problem -
                                                                                                      value_surrogate)))
        self.assertLess(math.fabs(value_problem - value_surrogate), 1e-8)

    def _test_scikit_gaussian_process_one(self):
        problem = MyProblemSin()
        problem.surrogate = SurrogateModelScikit(problem)
        problem.surrogate.sigma_threshold = 0.1

        kernel = 1.0 * ExpSineSquared(length_scale=1.0, periodicity=3.0, length_scale_bounds=(0.1, 10.0),
                                      periodicity_bounds=(1.0, 10.0))
        problem.surrogate.regressor = GaussianProcessRegressor(kernel=kernel)

        self._check_scikit_one(problem, 5.0)

    def test_scikit_gradient_boosting_regressor_one(self):
        problem = MyProblemSin()
        problem.surrogate = SurrogateModelScikit(problem)

        problem.surrogate.regressor = GradientBoostingRegressor()

        self._check_scikit_one(problem, 7.0)

    def test_scikit_bagging_regressor_one(self):
        problem = MyProblemSin()
        problem.surrogate = SurrogateModelScikit(problem)

        problem.surrogate.regressor = BaggingRegressor()

        self._check_scikit_one(problem, 7.0)

    def test_scikit_random_tree_regressor_one(self):
        problem = MyProblemSin()
        problem.surrogate = SurrogateModelScikit(problem)

        problem.surrogate.regressor = RandomForestRegressor(n_estimators=20)

        self._check_scikit_one(problem, 10.0)

    def test_scikit_gaussian_process_two(self):
        problem = Booth()
        problem.surrogate = SurrogateModelScikit(problem)
        # set custom regressor
        kernel = 1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1)
        problem.surrogate.regressor = GaussianProcessRegressor(kernel=kernel)
        # set threshold
        problem.surrogate.sigma_threshold = 0.01
        problem.surrogate.train_step = 12

        # train
        problem.surrogate.evaluate(Individual([1.0, 3.1]))
        problem.surrogate.evaluate(Individual([1.3, 3.2]))
        problem.surrogate.evaluate(Individual([1.8, 2.7]))
        problem.surrogate.evaluate(Individual([0.9, 3.3]))
        problem.surrogate.evaluate(Individual([0.8, 3.1]))
        problem.surrogate.evaluate(Individual([1.4, 2.8]))
        problem.surrogate.evaluate(Individual([0.1, 3.0]))
        problem.surrogate.evaluate(Individual([0.2, 3.4]))
        problem.surrogate.evaluate(Individual([0.95, 3.03]))
        problem.surrogate.evaluate(Individual([0.98, 2.96]))
        problem.surrogate.evaluate(Individual([1.02, 2.98]))
        problem.surrogate.evaluate(Individual([1.01, 2.99]))

        x_ref = Individual([0.2, 3.1])
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.predict(x_ref.vector)[0]

        percent = 100.0 * math.fabs(value_problem - value_surrogate) / math.fabs(value_problem)
        problem.logger.info(
            "{}: surrogate.value: eval = {}, pred = {}, diff = {} ({} %)".format(problem.name, value_problem,
                                                                                 value_surrogate,
                                                                                 math.fabs(
                                                                                     value_problem - value_surrogate),
                                                                                 percent))

        self.assertLess(percent, 5.0)

    def test_scikit_gaussian_process_lhs_two(self):
        problem = Booth()
        problem.set_init_values(**{'initial_value':[0.,0.]})
        problem.surrogate = SurrogateModelScikit(problem)
        # set custom regressor
        kernel = 1.0 * RationalQuadratic(length_scale=1.0)
        problem.surrogate.regressor = GaussianProcessRegressor(kernel=kernel)

        # set threshold
        problem.surrogate.sigma_threshold = 0.01
        problem.surrogate.train_step = 100

        # sweep analysis (for training)
        gen = LHSGenerator(problem.parameters)
        gen.init(problem.surrogate.train_step)
        algorithm_sweep = SweepAlgorithm(problem, generator=gen)
        algorithm_sweep.run()

        x_ref = Individual([2.00, -2.00])
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.predict(x_ref.vector)[0]

        percent = 100.0 * math.fabs(value_problem - value_surrogate) / math.fabs(value_problem)
        problem.logger.info(
            "{}: surrogate.value: eval = {}, pred = {}, diff = {} ({} %)".format(problem.name, value_problem,
                                                                                 value_surrogate,
                                                                                 math.fabs(
                                                                                     value_problem - value_surrogate),
                                                                                 percent))

        self.assertLess(percent, 5.0)



if __name__ == '__main__':
    unittest.main()
