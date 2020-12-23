from .surrogate import SurrogateModelPredict

import numpy as np

from smt.surrogate_models import RBF


class SurrogateModelSMT(SurrogateModelPredict):
    def __init__(self, problem):
        super().__init__(problem)

        self.train_step = -1
        self.sigma_threshold = 10
        self.score_threshold = 0.5

    def init_default_regressor(self):
        # default regressor
        self.regressor = RBF(d0=5, print_prediction=False)
        self.has_epsilon = False

    def predict(self, x, *args):
        if self.trained:
            return self.regressor.predict_values(np.array([x]))
        else:
            assert 0

    def predict_variances(self, x, *args):
        if self.trained:
            return self.regressor.predict_variances(np.array([x]), *args)
        else:
            assert 0

    def train(self):
        self.trained = False
        assert(len(self.x_data) == len(self.y_data))

        # print(self.x_data)
        # print("Trained set: {}".format(len(self.x_data)))

        self.regressor.options["print_global"] = False
        self.regressor.set_training_values(np.array(self.x_data), np.array(self.y_data))
        self.regressor.train()

        if self.eval_stats:
            # score
            pass
            # self.score = self.regressor.score(self.x_data, self.y_data)
            # print("self.score = {} : {}".format(len(self.x_data), self.score))
            # lml (Gaussian regressor)
            # if "log_marginal_likelihood" in dir(self.regressor):
            #    self.lml, self.lml_gradient = self.regressor.log_marginal_likelihood(self.regressor.kernel_.theta, eval_gradient=True)

        self.trained = True

