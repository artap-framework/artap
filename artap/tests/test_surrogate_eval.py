import math
import unittest

from ..individual import Individual
from ..benchmark_functions import Booth
from ..surrogate import SurrogateModelEval


class TestSurrogateEval(unittest.TestCase):
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
