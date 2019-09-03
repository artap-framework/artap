from .utils import flatten

from .surrogate import SurrogateModel

import warnings

from scipy.spatial import distance

from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor, ExtraTreesRegressor, BaggingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, DotProduct, WhiteKernel, ConstantKernel, RationalQuadratic, ExpSineSquared

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV


class SurrogateModelScikit(SurrogateModel):
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

    @staticmethod
    def get_mlp_regressor(search=False, verbose=1):
        # Neural network models
        # Multi-layer Perceptron regressor
        gp = MLPRegressor(hidden_layer_sizes=(6), activation='logistic', solver='lbfgs')

        if search:
            parameters = {
                'solver': ['lbfgs'],
                'max_iter': [1000, 1500, 2000],
                'alpha': [1.e-01, 1.e-05, 1.e-09],
                "hidden_layer_sizes": [(3), (10), (20), (50)],
                'random_state': [0, 2, 4, 5, 8, 9],
                "activation": ['logistic', 'relu']
            }

            gp = GridSearchCV(gp, parameters, n_jobs=-1, verbose=verbose)
            # gp = RandomizedSearchCV(gp, parameters, n_jobs=-1, verbose=verbose)

        return gp

    @staticmethod
    def get_extra_trees_regressor(search=False, verbose=1):
        # Ensemble Methods - decision trees
        gp = ExtraTreesRegressor(n_estimators=10)

        if search:
            parameters = {
                'bootstrap': [True],
                'max_depth': [80, 90, 100, 110],
                'max_features': [2],
                'min_samples_leaf': [3, 4, 5],
                'min_samples_split': [8, 10, 12],
                'n_estimators': [10, 50, 100, 500]
            }

            gp = GridSearchCV(gp, parameters, n_jobs=-1, verbose=verbose)

        return gp

    @staticmethod
    def get_random_forest_regressor(search=False, verbose=1):
        # Ensemble Methods - decision trees
        gp = RandomForestRegressor(n_estimators=10)

        if search:
            parameters = {
                'bootstrap': [True],
                'max_depth': [80, 90, 100, 110],
                'max_features': [2],
                'min_samples_leaf': [3, 4, 5],
                'min_samples_split': [8, 10, 12],
                'n_estimators': [10, 50, 100, 500]
            }
            # parameters = {
            #     'bootstrap': [True],
            #     'max_depth': [80, 90],
            #     'max_features': [2],
            #     'min_samples_leaf': [3],
            #     'min_samples_split': [8],
            #     'n_estimators': [10]
            # }

            gp = GridSearchCV(gp, parameters, n_jobs=-1, verbose=verbose)

        return gp

    @staticmethod
    def get_gaussian_process_regressor(search=False, verbose=1):

        ker_rbf1 = RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0))
        ker_rbf2 = ConstantKernel(1.0, constant_value_bounds="fixed") * RBF(1.0, length_scale_bounds=(1e-1, 10.0))
        ker_rq = ConstantKernel(1.0, constant_value_bounds="fixed") * RationalQuadratic(alpha=0.1, length_scale=1)
        ker_expsine = ConstantKernel(1.0, constant_value_bounds="fixed") * ExpSineSquared(1.0, 5.0, periodicity_bounds=(1e-2, 1e1))

        kernel_list = [ker_rbf1, ker_rbf2, ker_rq, ker_expsine]

        gp = GaussianProcessRegressor(kernel=RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)))

        if search:
            parameters = {
                "kernel": kernel_list,
                "alpha": [1e-12, 1e-8, 1e-4, 1e-1, 1e1],
                # "alpha": [1e-10],
                "optimizer": ["fmin_l_bfgs_b"],
                "n_restarts_optimizer": [1, 3, 10, 20],
                # "n_restarts_optimizer": [9],
                "normalize_y": [False],
                "copy_X_train": [True],
                "random_state": [0]
            }

            # grid_search = GridSearchCV(gp, param_grid=param_grid, n_jobs=-1, scoring=None) #
            # grid_search = BayesSearchCV(gp, search_spaces=param_grid)
            # grid_search = RandomizedSearchCV(gp, param_distributions=param_grid, n_jobs=-1, n_iter=1, scoring='neg_mean_squared_error')

            gp = GridSearchCV(gp, parameters, n_jobs=-1, verbose=verbose)

        return gp


    """
    # Ensemble Methods
    # AdaBoost regressor
    regressor_test(AdaBoostRegressor(DecisionTreeRegressor(max_depth=4), n_estimators=300))
    # Bagging regressor
    regressor_test(BaggingRegressor(n_estimators=10))
    # Gradient Boosting for regression
    regressor_test(GradientBoostingRegressor(n_estimators=500, max_depth=4, min_samples_split=2, learning_rate=0.01, loss='ls'))
    # Decision Trees
    # Extremely randomized tree regressor
    regressor_test(ExtraTreeRegressor())
    # Decision tree regressor
    regressor_test(DecisionTreeRegressor())
    # Generalized Linear Models
    # regressor_test(SGDRegressor())
    # Nearest Neighbors
    # Regression based on k-nearest neighbors
    regressor_test(KNeighborsRegressor(n_neighbors=6, weights='distance'))
    # Regression based on neighbors within a fixed radius
    regressor_test(RadiusNeighborsRegressor())
    regressor_test(KernelRidge(alpha=1.0))
    regressor_test(SVR(kernel='rbf', C=1e4, gamma=0.1))
    """

    def init_default_regressor(self):
        # default kernel
        kernel = 1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1)
        # default regressor
        self.regressor = GaussianProcessRegressor(kernel=kernel)
        self.has_epsilon = True

    def predict(self, x, *args):
        if self.trained:
            if self.has_epsilon:
                return self.regressor.predict([x], return_std=True)
            else:
                return self.regressor.predict([x])
        else:
            assert 0

    def train(self):
        # disable sklearn warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # print(len(self.x_data), len(self.y_data))
            # print(self.x_data, self.y_data)
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

    def evaluate(self, individual):
        evaluate = True

        if self.trained:
            # disable sklearn warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                if self.has_epsilon:
                    p, sigma = self.predict(individual.vector)
                else:
                    p = self.predict(individual.vector)
                    sigma = 0

            # compute minimal parameter distance
            if self.distance_metric is not None:
                dist = float("inf")
                for parameter in self.x_data:
                    if self.distance_metric == 'chebyshev':
                        dist = min(dist, distance.chebyshev(individual.vector, parameter))
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
            value = self.problem.evaluate(individual)
            # increase counter
            self.eval_counter += 1
            # add training date to surrogate model
            # self.add_data(np.array(x), np.array(value))
            self.add_data(individual.vector, value)

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
