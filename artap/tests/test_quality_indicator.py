import unittest

from ..quality_indicator import gd, epsilon_add


class TestGenerationalDistance(unittest.TestCase):

    def test_2d(self):
        # 2d test - euclidean
        ref = [(1., 1.), (2., 1. / 2.), (3., 1. / 3.), (4., 1. / 4.), (5., 1. / 5)]  ### 1/x
        calc = [(1., 1.01), (2., 0.51), (4., 0.26)]

        self.assertAlmostEqual(gd(ref, calc), 0.01)

    def test_3d(self):
        # 3d test - chebyshev
        ref = [(1., 1., 1.), (2., 1. / 2., 1. / 2.), (3., 1. / 3., 1. / 3.), (4., 1. / 4., 1. / 4.),
               (5., 1. / 5, 1. / 5,)]  ### 1/x
        calc = [(1., 1.01, 1.01), (2., 0.51, 0.51), (4., 0.26, 0.26)]

        self.assertAlmostEqual(gd(ref, calc, norm='chebyshev'), 0.01)


class TestEpsUnaryAdd(unittest.TestCase):

    def test_2d(self):
        # 2d test - euclidean
        ref = [(1., 1.), (2., 0.5), (4., 1. / 4.)]  ### 1/x
        calc = [(1., 1.02), (2., 0.53), (4., 0.26)]

        self.assertAlmostEqual(epsilon_add(ref, calc), 0.03)



if __name__ == '__main__':
    unittest.main()
