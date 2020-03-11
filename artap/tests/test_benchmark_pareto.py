import unittest
from artap.individual import Individual
from artap.benchmark_pareto import BiObjectiveTestProblem, DTLZI

class TestBiobjective(unittest.TestCase):

    def test_biobjective(self):
        test2d = BiObjectiveTestProblem()
        self.assertAlmostEqual(test2d.evaluate(Individual([1.0, 1.0]))[1], 2.)


class TestDTLZI(unittest.TestCase):

    def test_dtlzI(self):
        test2d = DTLZI(**{'dimension': 4, 'm':3})

        # The optimal values of this function are on a hyperplane

        f0 = test2d.evaluate(Individual([0.5, 0.5, 0.5, 0.5]))[0]
        f1 = test2d.evaluate(Individual([0.5, 0.5, 0.5, 0.5]))[1]
        f2 = test2d.evaluate(Individual([0.5, 0.5, 0.5, 0.5]))[2]

        self.assertAlmostEqual(f0+f1+f2, 0.5)




