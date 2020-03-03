import unittest
from artap.individual import Individual
from artap.benchmark_functions import Rosenbrock, Ackley, Schwefel, Sphere, ModifiedEasom, Michaelwicz, Perm, Rastrigin, \
    SixHump, EqualityConstr, Griewank, Schubert, Zakharov, XinSheYang, XinSheYang2, XinSheYang3, Booth, GramacyLee, \
    AlpineFunction


class TestRosenbrock(unittest.TestCase):

    def test_rosenbrock2d(self):
        test2d = Rosenbrock(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual([1.0, 1.0]))[0], 0.0)

    def test_rosenbrock10d(self):
        test2d = Rosenbrock(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]))[0], 0.0)


class TestAckley(unittest.TestCase):
    """ Tests for the synthetic benchmark functions """

    def test_ackley(self):
        test2d = Ackley(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual([0.0, 0.0]))[0], 0.0)

    def test_ackley10d(self):
        test2d = Ackley(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))[0], 0.0)


class TestSphere(unittest.TestCase):

    def test_sphere(self):
        test7d = Sphere(**{'dimension': 7})
        self.assertAlmostEqual(test7d.evaluate(Individual(test7d.global_optimum_coords))[0], 0.0)


class TestSchwefel(unittest.TestCase):

    def test_schwefel(self):
        test2d = Schwefel(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual([420.9687, 420.9687]))[0], 0, 4)

        test10d = Schwefel(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], 0, 4)


class TestModifiedEasom(unittest.TestCase):

    def test_measom(self):
        test2d = ModifiedEasom(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], -1., 4)


class TestMichaelwicz(unittest.TestCase):

    def test_micha2d(self):
        test2d = Michaelwicz(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestPerm(unittest.TestCase):

    def test_perm(self):
        test2d = Perm(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_perm10(self):
        test2d = Perm(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestRastrigin(unittest.TestCase):

    def test_rastrigin(self):
        test2d = Rastrigin(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_rastrigin10(self):
        test2d = Rastrigin(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestSixhump(unittest.TestCase):
    # only 2d
    def test_sixhump(self):
        test2d = SixHump(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestEqualityConstr(unittest.TestCase):

    def test_equalityconstr(self):
        test2d = EqualityConstr(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_equlaityconstr10(self):
        test2d = EqualityConstr(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestGriewank(unittest.TestCase):

    def test_griewank(self):
        test2d = Griewank(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_griewank10(self):
        test2d = Griewank(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


# class TestSchubert(unittest.TestCase):
# only 2d
# def test_schubert(self):
#     test2d = Schubert(**{'dimension': 2})
#     self.assertAlmostEqual(test2d.evaluate(test2d.global_optimum_coords), test2d.global_optimum, 3)

class TestZacharov(unittest.TestCase):

    def test_zacharov(self):
        test2d = Zakharov(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_griewank10(self):
        test2d = Zakharov(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestXinSheYang(unittest.TestCase):

    def test_xinsheyang(self):
        test2d = XinSheYang(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_xinsheyang10(self):
        test2d = XinSheYang(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestXinSheYang2(unittest.TestCase):

    def test_xinsheyang22(self):
        test2d = XinSheYang2(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_xinsheyang210(self):
        test2d = XinSheYang2(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestXinSheYang3(unittest.TestCase):

    def test_xinsheyang32(self):
        test2d = XinSheYang3(**{'dimension': 2})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)

    def test_xinsheyang310(self):
        test2d = XinSheYang3(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestBooth(unittest.TestCase):

    def test_booth(self):
        test2d = Booth()
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestGramacyLee(unittest.TestCase):

    def test_booth(self):
        test2d = GramacyLee()
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


class TestAlpine(unittest.TestCase):

    def test_alpine(self):
        test2d = AlpineFunction(**{'dimension': 10})
        self.assertAlmostEqual(test2d.evaluate(Individual(test2d.global_optimum_coords))[0], test2d.global_optimum, 3)


if __name__ == '__main__':
    unittest.main()
