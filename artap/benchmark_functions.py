from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator  # , FormatStrFormatter
import numpy as np
from numpy import exp, cos, sin, sqrt, linspace


class BenchmarkFunction:
    """
    The general class
    """

    def __init__(self):
        self.dimension: int
        self.bounds = []
        self.global_optimum: float
        self.global_optimum_coords: list

    def eval(self, x: list):
        pass

    def eval_constraints(self, x: list):
        pass

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = linspace(self.bounds[0][0], self.bounds[0][1])
        y = linspace(self.bounds[1][0], self.bounds[1][1])
        [x, y] = np.meshgrid(x, y)
        n = len(x)
        m = len(y)
        z = np.zeros([n, m])
        for i in range(n):
            for j in range(m):
                z[i, j] = self.eval([x[i, j], y[i, j]])

        surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        # ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        # pl.show()


class Rosenbrock(BenchmarkFunction):
    """
    The unconstrained Rosenbrock function --also known as Rosenbrock's valley or Rosenbrock's banana function --
    The global minimum is inside a long, narrow, parabolic shaped flat valley. To find the valley is trivial
    f*(X) = f(X*) is at the point X* = (1,1). However to converge to hte global minimum is difficult.

    $f(X) = 0.5*(100*(x-y^2)^2.+ (1-x)^2)$

    Search domain: -30 <= (x, y) <= 30
    """

    def __init__(self):
        super().__init__()
        self.bounds = [[-30, 30],
                       [-30, 30]]

    def eval(self, x):
        """
        :param x: a two dimensional array/list/tuple, which contains the X[x,y]
        :return: f(X)
        """

        a = 1. - x[0]
        b = x[1] - x[0] * x[0]

        return 0.5 * (a * a + b * b * 100.0)

    def eval_constraints(self, x):
        """
        :param x: a two dimensional array/list/tuple, which contains the X[x,y]
        :return:
        """
        violate_constraints = False
        if (x[0] > self.bounds[0][1]) or (x[0] < self.bounds[0][0]):
            violate_constraints = True
        if (x[1] > self.bounds[1][1]) or (x[1] < self.bounds[1][0]):
            violate_constraints = True

        return violate_constraints


class AckleyN2(BenchmarkFunction):
    """
    Ackley Nr. 2 test function is declared by the following formula:

    minimize:
         $f(x,y) = -200*exp(-0.2*sqrt(x^2+y^2))$


    search domain:
        -32 <= x,y <= 32


    Description and Features

        - convex
        - defined on 2-dimensional space
        - non-separable
        - differentiable

    Solution

    The function has a global minimum at f(x∗)=−200
    located at x∗=(0,0)
   """

    def __init__(self):
        super().__init__()
        self.bounds = [[-32, 32],
                       [-32, 32]]

    def eval(self, x):
        return -200. * exp(-0.02 * (x[0] ** 2 + x[1] ** 2) ** 0.5)


class Ackley4Modified:
    """
    Ackley 4 or Modified Ackley Function (Continuous, Differentiable, Non-Separable, Scalable, Multimodal)

    f(x)=\sum_{i=1}^{n-1}( e^{-0.2}\sqrt{x_i^2+x_{i+1}^2} + 3(cos(2x_i) + sin(2x_{i+1})))

    Description:

        - not convex
        - defined on n-dimensional space
        - non-separable
        - differentiable
        - continuous
        - scalable

    Search Domain

        The function can be defined on any input domain but it is usually evaluated on xi∈[−35,35] for i=1,…,n

    Solution

    On the 2-dimensional space, the function has one global minima at f(x∗)=−4.590101633799122
    located at x∗=(−1.51,−0.755)

    """

    @classmethod
    def eval(cls, x):
        dim = len(x)

        value = 0.
        for i in range(0, dim - 1):
            value += exp(-0.2) * sqrt(x[i] ** 2. + x[i + 1] ** 2.) + 3. * (cos(2 * x[i]) + sin(2 * x[i + 1]))

        return value


class BinhAndKorn:
    """
    This problem is often attributed to Binh and Korn, but is also mentioned in A Osyczka, H Tamura,
    Pareto set distribution method for multicriteria optimization using genetic algorithm.

    The problem is searching the minimum of the following function:

    $min(f_{1}(x,y),f_{2}(x,y))$

    where

        $f_{1}(x,y) = 4x^2 + 4y^2$
        $f_{2}(x,y) = (x-5)^2 + (y-5)^2 $

    subject to the following constraints:

    $g_{1}(x,y) = (x-5)^2 + y^2 \leq 25$
    $g_{2}(x,y) = (x-8)^2 + (y+3)^2 \leq 7.7$

    search domain: 0 <= x <=5, 0 <= y <= 3

    """

    @staticmethod
    def approx(x):
        """
        Estimates the pareto front of the Binh_and_Korn function in the following domain: [10;100]

        The approximate function is:

        f = a0+a1*x+a2*x^2+a3*x^3+a4*x^4+a5*x^5

        a0 = 4.564170954344949e+01 +/- 2.827448422117511e-01
        a1 = -1.939843031431697e+00 +/- 5.958429263576211e-02
        a2 = 5.327835893656892e-02 +/- 3.214348835707173e-03
        a3 = -7.960654974842228e-04 +/- 6.602271055507837e-05
        a4 = 5.666751361667045e-06 +/- 5.691036855808526e-07
        a5 = -1.505297721151948e-08 +/- 1.733740155631940e-09

        fitted on a platypus calculation: algorithm nsga II, 10 000 evaluations

        :param x: the value of the f1 function
        :return:
        """

        a0 = 4.564170954344949e+01
        a1 = -1.939843031431697e+00
        a2 = 5.327835893656892e-02
        a3 = -7.960654974842228e-04
        a4 = 5.666751361667045e-06
        a5 = -1.505297721151948e-08

        return a0 + a1 * x + a2 * x ** 2. + a3 * x ** 3. + a4 * x ** 4. + a5 * x ** 5.

    @classmethod
    def eval(cls, x):
        f1 = 4 * pow(x[0], 2) + 4 * pow(x[1], 2)
        f2 = pow(x[0] - 5, 2) + pow(x[1] - 5, 2)
        target = [f1, f2]

        return target

    @classmethod
    def constraints(cls, x):
        # 0 <= x <=5, 0 <= y <= 3
        g1 = min(0, 25 - pow(x[0] - 5, 2) - pow(x[1], 2))
        g2 = min(0, pow(x[0] - 8, 2) + pow(x[1] + 3, 2) - 7.7)
        violation = [g1, g2]
        return violation


class Booth:
    """
    Booth function
    """

    @classmethod
    def eval(cls, x):
        return (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2


if __name__ == '__main__':
    test = Rosenbrock()
    test.plot()
    test = AckleyN2()
    test.plot()
