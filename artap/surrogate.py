from .utils import flatten

import warnings
from abc import ABCMeta, abstractmethod

import numpy as np
from scipy.spatial import distance

# surrogate (default regressor)
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RationalQuadratic
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor, ExtraTreesRegressor

class SurrogateModel(metaclass=ABCMeta):
    def __init__(self, problem):
        # self.name = name
        self.problem = problem

        # surrogate model
        self.regressor = None

        self.x_data = []
        self.y_data = []

        self.trained = False

        # stats
        self.eval_counter = 0
        self.predict_counter = 0
        self.eval_stats = True

    def add_data(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    def init_default_regressor(self):
        pass

    @abstractmethod
    def train(self):
        pass

    def predict(self, x, *args):
        if self.trained:
            if self.has_epsilon:
                return self.regressor.predict([x], return_std=True)
            else:
                return self.regressor.predict([x])
        else:
            assert 0

    def compute(self, x):
        return self.problem.evaluate(x)

    @abstractmethod
    def evaluate(self, x):
        pass


class SurrogateModelEval(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)
        self.trained = True

    def train(self):
        pass

    def predict(self, x):
        return self.problem.evaluate(x)

    def evaluate(self, x):
        self.eval_counter += 1
        return self.problem.evaluate(x)


class SurrogateModelRegressor(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)

        self.train_step = 10
        self.sigma_threshold = 10
        self.score_threshold = 0.5
        self.distance_metric = 'chebyshev'
        self.distance_threshold = 1.0
        self.has_epsilon = False # some regressors has epsilon (GaussianProcessRegressor, ...)

        # stats
        self.score = None
        self.lml = None
        self.lml_gradient = None

    def init_default_regressor(self):
        # default kernel
        kernel = 1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1)
        # default regressor
        self.regressor = GaussianProcessRegressor(kernel=kernel)
        self.has_epsilon = True

    def train(self):
        # disable sklearn warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            print(len(self.x_data), len(self.y_data))
            print(self.x_data, self.y_data)
            self.regressor.fit(self.x_data, self.y_data)
            # self.regressor.fit(self.x_data, np.ravel(self.y_data, order='C'))
            # self.trained = True

        if self.eval_stats:
            # score
            self.score = self.regressor.score(self.x_data, self.y_data)
            # print("self.score = {} : {}".format(len(self.x_data), self.score))
            # lml (Gaussian regressor)
            if "log_marginal_likelihood" in dir(self.regressor):
                self.lml, self.lml_gradient = self.regressor.log_marginal_likelihood(self.regressor.kernel_.theta, eval_gradient=True)

        # set trained
        self.trained = self.score >= self.score_threshold
        self.trained = True

    def evaluate(self, x):
        evaluate = True

        if self.trained:
            # disable sklearn warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                if self.has_epsilon:
                    p, sigma = self.predict(x)
                else:
                    p = self.predict(x)
                    sigma = 0

            # compute minimal parameter distance
            if self.distance_metric is not None:
                dist = float("inf")
                for val in self.x_data:
                    if self.distance_metric == 'chebyshev':
                        dist = min(dist, distance.chebyshev(x, val))
                    else:
                        assert 0

                # print("dist = {}".format(dist))
                # print("sigma = {}".format(sigma))

            # estimated value
            value = flatten(p[0])

            """
            val = self.problem.evaluate(x)
            # self.problem.logger.info("SurrogateGaussianProcess: predict: x: {}, prediction: {}, sigma: {}".format(x, p[0], sigma))
            self.problem.logger.info("SurrogateGaussianProcess: predict: x: {}, prediction: {}, value: {}".format(x, p[0], val))
            value = val
            """

            # increase counter
            self.predict_counter += 1
            evaluate = False

        if evaluate:
            # evaluate problem
            value = self.problem.evaluate(x)
            # increase counter
            self.eval_counter += 1
            # add training date to surrogate model
            # self.add_data(np.array(x), np.array(value))
            self.add_data(x, value)

            if self.eval_counter % self.train_step == 0:
                # init default regressor
                if self.regressor is None:
                    self.init_default_regressor()

                # train model
                self.train()

        """
        if self.trained:
            p, sigma = self.predict([x], return_std=True)
            self.problem.logger.info(
                "SurrogateGaussianProcess: predict: x: {}, prediction: {}, sigma: {}".format(x, p[0], sigma))

            if sigma < self.options['sigma_threshold']:
                # estimated value
                value = p[0].tolist()

                # increase counter
                self.predict_counter += 1
                evaluate = False

        if evaluate:
            # evaluate problem
            value = self.problem.evaluate(x)
            # increase counter
            self.eval_counter += 1
            # add training date to surrogate model
            self.add_data(x, value)

            if self.eval_counter % self.options['train_step'] == 0:
                # surrogate model
                counter_eff = 100.0 * self.predict_counter / (
                            self.eval_counter + self.predict_counter)
                # speed up - increase train step
                if counter_eff > 30:
                    self.options['train_step'] = int(self.options['train_step'] * 1.3)
                self.problem.logger.info("Surrogate: learning: {}, predict eff: {}, train_step: {}"
                                  .format(self.predict_counter, counter_eff, self.options['train_step']))

                # init default regressor
                if self.regressor is not None:
                    self.init_default_regressor()

                # train model
                self.train()
        """
        return value
