import unittest
from artap.benchmarks.synthetic_functions import eval_5d_synthetic, eval_10d_synthetic


class TestSynthetic(unittest.TestCase):
    """ Tests for the synthetic benchmark functions """

    def test_synthetic5d(self):
        self.assertAlmostEqual(eval_5d_synthetic([10., 1.0, 6.0, 7.0, 8.0]), .7)
        self.assertAlmostEqual(eval_5d_synthetic([1.0, 3.0, 8.0, 9.5, 2.0]), .75)
        self.assertAlmostEqual(eval_5d_synthetic([3.0, 1.0, 3.0, 2.0, 5.0]), 1.0)
        self.assertAlmostEqual(eval_5d_synthetic([3.0, 4.0, 1.3, 5.0, 5.0]), 1.2, 5)

        self.assertAlmostEqual(eval_5d_synthetic([5.0, 2.0, 9.6, 7.3, 8.6]), 1.0)
        self.assertAlmostEqual(eval_5d_synthetic([7.5, 8.0, 9.0, 3.2, 4.6]), .6, 4)
        self.assertAlmostEqual(eval_5d_synthetic([5.7, 9.3, 2.2, 8.4, 7.1]), .5)
        self.assertAlmostEqual(eval_5d_synthetic([5.5, 7.2, 5.8, 2.3, 4.5]), .2, 4)

        self.assertAlmostEqual(eval_5d_synthetic([4.7, 3.2, 5.5, 7.1, 3.3]), 0.4)
        self.assertAlmostEqual(eval_5d_synthetic([9.7, 8.4, 0.6, 3.2, 8.5]), 0.1)

    def test_synthetic10d(self):
        self.assertAlmostEqual(eval_10d_synthetic([10., 1.0, 6.0, 7.0, 8.0, 1.0, 1.0, 6.0, 7.0, 8.0]), 0.7)
        self.assertAlmostEqual(eval_10d_synthetic([1.0, 3.0, 8.0, 9.5, 2.0, 1.0, 3.0, 8.0, 9.5, 2.0]), 0.75)
        self.assertAlmostEqual(eval_10d_synthetic([3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0]), 1.0)
        self.assertAlmostEqual(eval_10d_synthetic([3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0]), 1.2)


if __name__ == '__main__':
    unittest.main()
