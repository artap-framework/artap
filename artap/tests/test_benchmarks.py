import unittest
from artap.benchmark_functions import Rosenbrock, Ackley, Schwefel, Sphere


class TestRosenbrock(unittest.TestCase):

    def test_rosenbrock2d(self):
        test2d = Rosenbrock(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate([1.0, 1.0]), 0.0)

    def test_rosenbrock10d(self):
        test2d = Rosenbrock(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 0.0)


class TestAckley(unittest.TestCase):
    """ Tests for the synthetic benchmark functions """

    def test_ackley(self):
        test2d = Ackley(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate([0.0, 0.0]), 0.0)

    def test_ackley10d(self):
        test2d = Ackley(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), 0.0)


class TestSphere(unittest.TestCase):

    def test_sphere(self):
        test7d = Sphere(**{'dimension': 7})
        self.assertAlmostEqual(test7d.evaluate(test7d.global_optimum_coords), 0.0)


class TestSchwefel(unittest.TestCase):

    def test_schwefel(self):
        test2d = Schwefel(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate([420.9687, 420.9687]), 0, 4)

        test10d = Schwefel(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(test2d.global_optimum_coords), 0, 4)


if __name__ == '__main__':
    unittest.main()
