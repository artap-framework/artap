import unittest
from artap.benchmark_functions import Rosenbrock


class TestRosenbrock(unittest.TestCase):
    """ Tests for the synthetic benchmark functions """

    def test_rosenbrock2d(self):
        test2d = Rosenbrock(**{'dimension':2})
        self.assertAlmostEqual(test2d.evaluate([1.0, 1.0]), 0.0)

    def test_rosenbrock10d(self):
        test2d = Rosenbrock(**{'dimension':10})
        self.assertAlmostEqual(test2d.evaluate([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 0.0)


if __name__ == '__main__':
    unittest.main()