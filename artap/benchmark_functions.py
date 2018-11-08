from numpy import exp, cos, sin, sqrt


class Rosenbrock:
    """
    The unconstrained Rosenbrock function --also known as Rosenbrock's valley or Rosenbrock's banana function --
    The global minimum is inside a long, narrow, parabolic shaped flat valley. To find the valley is trivial
    f*(X) = f(X*) is at the point X* = (1,1). However to converge to hte global minimum is difficult.

    $f(X) = 0.5*(100*(x-y^2)^2.+ (1-x)^2)$

    Search domain: -30 <= (x, y) <= 30
    """

    @classmethod
    def eval(cls, X):
        """
        :param X: a two dimensional array/list/tuple, which contains the X[x,y]
        :return: f(X)
        """

        x = X[0]
        y = X[1]
        a = 1. - x
        b = y - x * x

        return 0.5 * (a * a + b * b * 100.0)


class AckleyN2:
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

    @classmethod
    def eval(cls, X):
        x = X[0]
        y = X[1]

        return -200. * exp(-0.02 * (x ** 2 + y ** 2) ** 0.5)


class Ackley4Modified:
    """
    Ackley 4 or Modified Ackley Function (Continuous, Differentiable, Non-Separable, Scalable, Multimodal)

    f(x)=\sum_{i=1}^{n-1}( e^{-0.2}\sqrt{x_i^2+x_{i+1}^2} + 3(cos(2x_i) + sin(2x_{i+1})))

    Description:

        - not convex
        - defined on n-dimensional space
        - non-separable
        - differentiable
        - continous
        - scalable

    Search Domain

        The function can be defined on any input domain but it is usually evaluated on xi∈[−35,35] for i=1,…,n

    Solution

    On the 2-dimensional space, the function has one global minima at f(x∗)=−4.590101633799122
    located at x∗=(−1.51,−0.755)

    """
    @classmethod
    def eval(cls, X):
        dim = len(X)

        value = 0.
        for i in range(0, dim - 1):
            value += exp(-0.2) * sqrt(X[i] ** 2. + X[i + 1] ** 2.) + 3. * (cos(2 * X[i]) + sin(2 * X[i + 1]))

        return value


class Binh_and_Korn:
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
    $g_{1}(x,y) = (x-8)^2 + (y+3)^2 \leq 7.7$

    search domain: 0 <= x <=5, 0 <= y <= 3

    The solution is approximately:

    f(x) = 2.8873e-10*x^6-1.2854e-7*x^5+2.2318*x^4-0.0019*x^3+0.087*x^2-2.3012*x+46.1968

    """

    @classmethod
    def eval(cls, x_list):
        x = x_list[0]
        y = x_list[1]
        f1 = 4 * pow(x, 2) + 4 * pow(y, 2)
        f2 = pow(x - 5, 2) + pow(y - 5, 2)
        target = [f1, f2]
        return target

    @classmethod
    def constraints(cls, x_list):
        # 0 <= x <=5, 0 <= y <= 3
        x = x_list[0]
        y = x_list[1]
        g1 = max(0, 25 - pow(x - 5, 2) - pow(y, 2))
        g2 = max(0, pow(x - 8, 2) + pow(y + 3, 2) - 7.7)
        violation = [g1, g2]
        return violation
