import unittest
from ..individual import Individual
from ..benchmark_pareto import BiObjectiveTestProblem, DTLZI,DTLZII, DTLZIII, DTLZIV


class TestBiobjective(unittest.TestCase):

    def test_biobjective(self):
        test2d = BiObjectiveTestProblem()
        self.assertAlmostEqual(test2d.evaluate(Individual([1.0, 1.0]))[1], 2.)


"""
Comparison is based on the following paper:

  [1]  Durillo, Juan J., José García-Nieto, Antonio J. Nebro, Carlos A. Coello Coello, Francisco Luna, and Enrique Alba. 
       "Multi-objective particle swarm optimizers: An experimental comparison."
        In International conference on evolutionary multi-criterion optimization, 
        pp. 495-509. Springer, Berlin, Heidelberg, 2009.

Common parameters
-----------------

    Swarm/Generation size: 100 particles
    Iterations: 250

"""


class TestDTLZI(unittest.TestCase):

    def test_dtlzI(self):
        test2d = DTLZI(**{'dimension': 8, 'm':3})

        # The optimal values of this function are on a hyperplane
        x = [0.5, 0.5, 0.5, 0.5,0.5, 0.5, 0.5, 0.5]
        f0 = test2d.evaluate(Individual(x))[0]
        f1 = test2d.evaluate(Individual(x))[1]
        f2 = test2d.evaluate(Individual(x))[2]

        self.assertAlmostEqual(f0+f1+f2, 0.5)


class TestDTLZII(unittest.TestCase):

    def test_dtlzII(self):
        test2d = DTLZII(**{'dimension': 12, 'm':3})

        # The optimal values of this function are on a hyperplane
        x = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        f0 = test2d.evaluate(Individual(x))[0]
        f1 = test2d.evaluate(Individual(x))[1]
        f2 = test2d.evaluate(Individual(x))[2]

        self.assertAlmostEqual(f0**2.0+f1**2.0+f2**2.0, 1.0)



class TestDTLZIII(unittest.TestCase):

    def test_dtlzIII(self):
        test2d = DTLZIII(**{'dimension': 12, 'm':3})

        # The optimal values of this function are on a hyperplane
        x = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        f0 = test2d.evaluate(Individual(x))[0]
        f1 = test2d.evaluate(Individual(x))[1]
        f2 = test2d.evaluate(Individual(x))[2]

        self.assertAlmostEqual(f0**2.0+f1**2.0+f2**2.0, 1.0)


class TestDTLZIV(unittest.TestCase):

    def test_dtlzIV(self):
        test2d = DTLZIV(**{'dimension': 12, 'm':3})

        # The optimal values of this function are on a hyperplane
        x = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        f0 = test2d.evaluate(Individual(x))[0]
        f1 = test2d.evaluate(Individual(x))[1]
        f2 = test2d.evaluate(Individual(x))[2]

        self.assertAlmostEqual(f0**2.0+f1**2.0+f2**2.0, 1.0)
