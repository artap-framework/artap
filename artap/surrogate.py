from .utils import ConfigDictionary

from abc import ABCMeta, abstractmethod

# surrogate
# from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel as C
# from sklearn.neural_network import MLPClassifier


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

        self.options = ConfigDictionary()
        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')

    def add_data(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    def init_default_regressor(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self, x):
        pass


class SurrogateModelEval(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)
        self.trained = True

    def train(self):
        pass

    def evaluate(self, x):
        self.eval_counter += 1
        return self.problem.evaluate(x)


class SurrogateModelGaussianProcess(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)

        self.options.declare(name='train_step', default=10, lower=0,
                             desc='Train step')
        self.options.declare(name='sigma_threshold', default=0.1, lower=0,
                             desc='Sigma threshold')

    def init_default_regressor(self):
        # default kernel
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-6, 3e2))
        # default regressor
        self.regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5)

    def train(self):
        # print(self.x_data, self.y_data)
        self.regressor.fit(self.x_data, self.y_data)
        self.trained = True

    def evaluate(self, x):
        evaluate = True

        if self.trained:
            p, sigma = self.regressor.predict([x], return_std=True)
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
                # speed up
                if counter_eff > 30:
                    self.options['train_step'] = int(self.options['train_step'] * 1.3)
                self.problem.logger.info("Surrogate: learning: {}, predict eff: {}, train_step: {}"
                                  .format(self.predict_counter, counter_eff, self.options['train_step']))

                # clf = linear_model.SGDRegressor()
                # clf = linear_model.SGDRegrBayesianRidgeessor()
                # clf = linear_model.LassoLars()
                # clf = linear_model.TheilSenRegressor()
                # clf = linear_model.LinearRegression()

                # init default regressor
                if not self.regressor:
                    self.init_default_regressor()

                # train model
                self.train()

                # DEBUG
                """
                p, sigma = self.regressor.predict([x], return_std=True)
                value_eval = value
                self.problem.logger.info(
                    "SurrogateGaussianProcess: predict: x: {}, eval: {}, prediction: {}, sigma: {}".format(x, value_eval, p[0], sigma))
                """

        return value
