from .utils import flatten

from .surrogate import SurrogateModel

import numpy as np

from scipy.spatial import distance

from smt.surrogate_models import RBF, KRG, KPLS, IDW, RMTB, LS, QP, GENN, GEKPLS, KPLSK


class SurrogateModelSMT(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)

        self.train_step = 10
        self.sigma_threshold = 10
        self.score_threshold = 0.5

        # stats
        self.xxx = None

    @staticmethod
    def get_rbf_regressor(verbose=1):
        # Radial basis functions
        return RBF(d0=5, print_prediction=False)

    @staticmethod
    def get_idw_regressor(verbose=1):
        # Inverse-distance weighting
        return IDW(p=4)

    # @staticmethod
    # def get_rbtb_regressor(verbose=1):
        # Regularized minimal-energy tensor-product splines
        # return RMTB(xlimits=np.array(bench.limits()), order=4, num_ctrl_pts=20, energy_weight=1e-15, regularization_weight=0.0)

    @staticmethod
    def get_ls_regressor(verbose=1):
        # Least-squares approximation
        return LS()

    @staticmethod
    def get_qp_regressor(verbose=1):
        # Second-order polynomial approximation
        return QP()

    @staticmethod
    def get_krg_regressor(verbose=1):
        # Kriging
        return KRG(theta0=[1e-2])

    @staticmethod
    def get_kpls_regressor(verbose=1):
        # Kriging model that uses the partial least squares
        return KPLS(theta0=[1e-2])

    @staticmethod
    def get_kplsk_regressor(verbose=1):
        # Kriging model that uses the partial least squares
        return KPLSK(theta0=[1e-2])

    def init_default_regressor(self):
        # default regressor
        self.regressor = self.get_rbf_regressor()
        self.has_epsilon = False

    def predict(self, x, *args):
        if self.trained:
            return self.regressor.predict_values(np.array([x]))
        else:
            assert 0

    def train(self):
        self.trained = False
        assert(len(self.x_data) == len(self.y_data))

        # print(self.x_data)

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

        # set trained
        # self.trained = self.score >= self.score_threshold

        self.trained = True

    def evaluate(self, individual):
        evaluate = True

        if self.trained:
            p = self.predict(individual.vector)
            # REMOVE
            # p_value = self.problem.evaluate(individual)
            # print(individual.vector, p, p_value, abs(p - p_value))
            if self.regressor.supports["variances"]:
                sigma = self.regressor.predict_variances(np.array([individual.vector]))
            else:
                sigma = 0

            # compute minimal parameter distance
            dist = 0.0
            if self.distance_threshold > 0.0:
                dist = self.compute_distance(individual.vector)

                #print("dist = {}".format(dist))
                #print("sigma = {}".format(sigma))

            # estimated value
            value = flatten(p[0])

            # check distance increase counter
            # print("dist = {}".format(dist))
            if dist <= self.distance_threshold:
                self.predict_counter += 1
                evaluate = False

            # HACK
            # if not evaluate:
            #     m = float("inf")
            #     for i in range(len(self.y_data)):
            #         m = min(self.y_data[i][0], m)
            #         # m = min(self.y_data[i], m)
            #     if value[0] < m:
            #     # if value < m:
            #         self.predict_counter -= 1
            #         evaluate = True

        if evaluate:
            # evaluate problem
            value = self.problem.evaluate(individual)
            # increase counter
            self.eval_counter += 1
            # add training date to surrogate model
            self.add_data(individual.vector, value)

            if self.eval_counter % self.train_step == 0:
                # init default regressor
                if self.regressor is None:
                    self.init_default_regressor()

                # train model
                self.train()

        # print("Evaluate = {}, \t value = {}".format(evaluate, value))
        self.problem.logger.info("surrogate: predict / eval counter: {0:5.0f} / {1:5.0f}, total: {2:5.0f}".format(self.problem.surrogate.predict_counter, self.problem.surrogate.eval_counter,
                                                                                                                self.problem.surrogate.predict_counter + self.problem.surrogate.eval_counter))
        return value
