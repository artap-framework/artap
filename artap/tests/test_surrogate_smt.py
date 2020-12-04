import math
import unittest

from ..problem import Problem
from ..individual import Individual
from ..benchmark_functions import Booth
from ..surrogate_smt import SurrogateModelSMT

from smt.surrogate_models import RBF, KRG, KPLS, IDW, RMTB, LS, QP, GENN, GEKPLS, KPLSK


class TestSurrogateSMT(unittest.TestCase):
    def _check_smt(self, regressor, percent=1.0):
        problem = Booth()
        problem.surrogate = SurrogateModelSMT(problem)
        # set custom regressor
        problem.surrogate.regressor = regressor
        # set threshold
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

        # check values
        x_ref = Individual([0.2, 3.1])
        # eval reference
        value_problem = problem.evaluate(x_ref)[0]
        # eval surrogate
        value_surrogate = problem.surrogate.predict(x_ref.vector)

        percent_check = 100.0 * math.fabs(value_problem - value_surrogate) / math.fabs(value_problem)
        problem.logger.info(
            "{}: surrogate.value: eval = {}, pred = {}, diff = {} ({} %)".format(problem.name, value_problem,
                                                                                 value_surrogate,
                                                                                 math.fabs(
                                                                                     value_problem - value_surrogate),
                                                                                 percent_check))

        self.assertLess(percent_check, percent)

    def test_smt_rbf(self):
        self._check_smt(RBF(d0=5, print_prediction=False))

    #def test_smt_idw(self):
    #    self._check_smt(IDW(p=4))

    def test_smt_kpls(self):
        self._check_smt(KPLS(theta0=[1e-2]))

    def test_smt_kplsk(self):
        self._check_smt(KPLSK(theta0=[1e-2]))

    #def test_smt_ls(self):
    #    self._check_smt(LS())

    def test_smt_qp(self):
        self._check_smt(QP())

    def test_smt_krg(self):
        self._check_smt(KRG(theta0=[1e-2]))
