import unittest
from artap.individual import Individual
from artap.benchmark_robust import Synthetic1D, Synthetic2D, Synthetic5D, Synthetic10D


class TestSynthetic1D(unittest.TestCase):

    def test_synthetic1d(self):
        test = Synthetic1D()
        self.assertAlmostEqual(test.evaluate(Individual([11.0]))[0], 3.23, 3)
        self.assertAlmostEqual(test.evaluate(Individual([1.6]))[0], 3.205, 2)


class TestSynthetic2D(unittest.TestCase):

    def test_synthetic2d(self):
        test = Synthetic2D()
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 4.0]))[0], 1.21112, 4)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 1.0]))[0], 1.00096, 4)


class TestSynthetic5D(unittest.TestCase):

    def test_synthetic5d(self):
        test = Synthetic5D()
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 4.0, 1.3, 5.0, 5.0]))[0], 1.200000000, 4)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 1.0, 3.0, 2.0, 5.0]))[0], 1.000, 4)

        self.assertAlmostEqual(test.evaluate(Individual([10., 1.0, 6.0, 7.0, 8.0]))[0], .7)
        self.assertAlmostEqual(test.evaluate(Individual([1.0, 3.0, 8.0, 9.5, 2.0]))[0], .75)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 1.0, 3.0, 2.0, 5.0]))[0], 1.0)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 4.0, 1.3, 5.0, 5.0]))[0], 1.2, 5)

        self.assertAlmostEqual(test.evaluate(Individual([5.0, 2.0, 9.6, 7.3, 8.6]))[0], 1.0)
        self.assertAlmostEqual(test.evaluate(Individual([7.5, 8.0, 9.0, 3.2, 4.6]))[0], .6, 4)
        self.assertAlmostEqual(test.evaluate(Individual([5.7, 9.3, 2.2, 8.4, 7.1]))[0], .5)
        self.assertAlmostEqual(test.evaluate(Individual([5.5, 7.2, 5.8, 2.3, 4.5]))[0], .2, 4)

        self.assertAlmostEqual(test.evaluate(Individual([4.7, 3.2, 5.5, 7.1, 3.3]))[0], 0.4)
        self.assertAlmostEqual(test.evaluate(Individual([9.7, 8.4, 0.6, 3.2, 8.5]))[0], 0.1)


class TestSynthetic10D(unittest.TestCase):

    def test_synthetic10d(self):
        test = Synthetic10D()
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0]))[0],
                               1.200000000, 4)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0]))[0], 1.000,
                               4)
        self.assertAlmostEqual(test.evaluate(Individual([10., 1.0, 6.0, 7.0, 8.0, 1.0, 1.0, 6.0, 7.0, 8.0]))[0], 0.7)
        self.assertAlmostEqual(test.evaluate(Individual([1.0, 3.0, 8.0, 9.5, 2.0, 1.0, 3.0, 8.0, 9.5, 2.0]))[0], 0.75)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0]))[0], 1.0)
        self.assertAlmostEqual(test.evaluate(Individual([3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0]))[0], 1.2)
