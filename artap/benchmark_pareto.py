from artap.benchmark_functions import BenchmarkFunction
from math import cos, pi, sin
import numpy as np


class BiObjectiveTestProblem(BenchmarkFunction):
    """
    The goal of this example to show, how we can use Artap to solve a simple,
    bi-objective optimization problem.

    The problem is defined in the following way [GDE3]:

    Minimize f1 = x1
    Minimize f2 = (1+x2) / x1

    subject to
            x1 e [0.1, 1]
            x2 e [0, 5]

    The Pareto - front of the following problem is known, it is a simple
    hyperbola. This problem is very simple for an Evolutionary algorithm, it finds its solution within 20-30 generations.
    NSGA - II algorithm is used to solve this example.

    References
    ----------

    .: [GDE3] The third Evolution Step of Generalized Differential Evolution
    Saku Kukkonen, Jouni Lampinen

    """

    def set(self):
        self.name = 'Biobjective Test Problem'
        self.parameters = [{'name': 'x_1', 'bounds': [0.1, 1.]},
                           {'name': 'x_2', 'bounds': [0.0, 5.0]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def pareto_front(self, x):
        """ x -> y """
        x = x.vector
        return 1. / x[0]

    def evaluate(self, individual):
        # The individual.vector function contains the problem parameters in the appropriate (previously defined) order
        f1 = individual.vector[0]
        f2 = (1 + individual.vector[1]) / individual.vector[0]
        return [f1, f2]


class PoloniFunction(BenchmarkFunction):
    """
    Poloni (POL) function is a classic test function for multi-objective optimization methods as its Pareto optimal
    solutions are not continous and non-convex.

    References:
    ---------

    [1] Lei, Gang; Zhu, Jianguo; Guo, Youguang, "Design Optimization Methods for Electrical Machines", 2016

    [2] Lei G, Shao KR, Guo YG, Zhu JG (2012), "Multiobjective sequential optimization method for the design of
        industrial electromagnetic devices. IEEE Trans Magn 48(11):4538–4541"

    section: 4.4.2
    formula: 4.13 and 3.13
    """

    def set(self, **kwargs):
        self.name = 'Booth Function'

        self.set_dimension = 2.0
        self.parameters = [{'name': 'x', 'bounds': [-pi, pi]},
                           {'name': 'y', 'bounds': [-pi, pi]}]

        self.global_optimum = 0.0
        self.global_optimum_coords = [1., 3.]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x1 = x.vector[0]
        x2 = x.vector[1]

        A1 = 0.5 * np.sin(1.) - 2. * np.cos(1.) + np.sin(2.) - 1.5 * np.cos(2.)
        A2 = 1.5 * np.sin(1.) - np.cos(1.) + 2. * np.sin(2.) - 0.5 * np.cos(2.)

        B1 = 0.5 * np.sin(x1) - 2. * np.cos(x1) + np.sin(x2) - 1.5 * np.cos(x2)
        B2 = 1.5 * np.sin(x1) - np.cos(x1) + 2. * np.sin(x2) - 0.5 * np.cos(x2)

        f1 = 1. + (A1 - B1) ** 2. + (A2 - B2) ** 2.
        f2 = (x1 + 3.) ** 2. + (x2 + 1.) ** 2.

        return [f1, f2]


class DTLZI(BenchmarkFunction):
    """
    The number of dimensions should be n = m + k -1, where m is the number of the objectives and
    k is an arbitrary number, which should be bigger than 1.

    .. math::

        \left.\matrix{ {\rm Minimize} & f_{1}({\rm x})={1\over 2}x_{1}x_{2}\cdots x_{M-1}(1+g({\rm x}_{M})),
        \hfill\cr {\rm Minimize} & f_{2}({\rm x})={1\over 2}x_{1}x_{2}\cdots (1-x_{M-1})(1+g({\rm x}_{M})),
        \hfill\cr \vdots & \vdots\hfill \cr {\rm Minimize} & f_{M-1}({\rm x})={1\over 2}x_{1}(1-x_{2})(1+g({\rm x}_{M})),
        \hfill\cr {\rm Minimize}& f_{M}({\rm x})={1\over 2}(1-x_{1})(1+g({\rm x}_{M})),
        \hfill\cr {\rm Subject}\,{\rm to}& 0\leq x_{i}, \leq 1, \quad {\rm for}
        i=1,2, \ldots, n.\hfill}\right\}\eqno{\hbox{(7)}}

        References
        ----------

        [1] Deb, K., Thiele, L., Laumanns, M., & Zitzler, E. (2002, May).
            Scalable multi-objective optimization test problems.
            In Proceedings of the 2002 Congress on Evolutionary Computation.
            CEC'02 (Cat. No. 02TH8600) (Vol. 1, pp. 825-830). IEEE.
    """

    def set(self, **kwargs):
        self.name = 'DTLZ I Test Problem'

        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = [0.5 for x in range(self.dimension)]  ###
        self.global_optimum_coords = [0.5 for x in range(self.dimension)]

        # single objective problem
        self.costs = self.generate_objective_functions(**kwargs)

    def pareto_front(self, x):
        """ x -> y """

        p_f = []
        for i in range(0, len(self.costs)):
            p_f.append(0.5)
        return p_f

    def evaluate(self, x):

        k = 5  # k >= 1, it can be k = 5 is the offered value,

        m = len(self.costs)
        x = x.vector
        scores = []
        for i in range(0, m):
            fi = 0.5
            for j in range(0, m - i - 1):
                fi *= x[j]

            if i > 0:
                fi *= (1. - x[m - i - 1])

            # g(xm)
            gm = float(k)
            for i in range(0, k):
                gm += (x[len(x) - i - 1] - 0.5) ** 2. - cos(20. * pi * (x[len(x) - i - 1] - 0.5))
            fi = fi * (1 + 100. * gm)
            scores.append(fi)

        return scores


class DTLZII(BenchmarkFunction):
    """
    The number of dimensions should be n = m + k -1, where m is the number of the objectives and
    k is an arbitrary number, which should be bigger than 1.

    .. math::
        \matrix{ {\rm Minimize} & fi({\rm x})=(1+g({\rm x}_{M}))\cos(x_{1}\pi/2)\cdots\cos(x_{M-1}\pi/2),
        \hfill\cr {\rm Minimize} & f_{2}({\rm x})=(1+g({\rm x}_{M}))\cos(x_{1}\pi/2)\cdots\sin(x_{M-1}\pi/2),
        \hfill\cr \vdots & \vdots \hfill\cr {\rm Minimize} & f_{M}({\rm x})=(1+g({\rm x}_{M}))\sin(x_{1}\pi/2),
        \hfill\cr & 0\leq x_{i}\leq 1,\quad {\rm for} i=1,2, \ldots, n,
        \hfill\cr {\rm where} & g({\rm x}_{M})=\sum_{x_{i}\in {\rm x}_{M}}(x_{i}-0.5)^{2}.\hfill}\eqno{\hbox{(9)}}


        References
        ----------

        [1] Deb, K., Thiele, L., Laumanns, M., & Zitzler, E. (2002, May).
            Scalable multi-objective optimization test problems.
            In Proceedings of the 2002 Congress on Evolutionary Computation.
            CEC'02 (Cat. No. 02TH8600) (Vol. 1, pp. 825-830). IEEE.
    """

    def set(self, **kwargs):
        self.name = 'DTLZ II Test Problem'

        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = [0.5 for x in range(self.dimension)]  ###
        self.global_optimum_coords = [0.5 for x in range(self.dimension)]

        # single objective problem
        self.costs = self.generate_objective_functions(**kwargs)

    def pareto_front(self, x):
        """ x -> y """

        p_f = []
        for i in range(0, len(self.costs)):
            p_f.append(0.5)
        return p_f

    def evaluate(self, x):

        k = 10  # k >= 1, it can be k = 5 is the offered value,

        m = len(self.costs)
        x = x.vector
        scores = []
        for i in range(0, m):
            fi = 1.0
            for j in range(0, m - i - 1):
                fi *= cos(0.5 * x[j] * pi)

            if i > 0:
                fi *= sin(x[m - i] * pi / 2.)
            gm = 0.
            for i in range(0, k):
                gm += (x[len(x) - i - 1] - 0.5) ** 2.
            fi *= (1. + gm)
            scores.append(fi)

        return scores


class DTLZIII(BenchmarkFunction):
    """
    This is the same function like DTLZ II, with the g function of the DTLZ I problem.

    The number of dimensions should be n = m + k -1, where m is the number of the objectives and
    k is an arbitrary number, which should be bigger than 1.


        References
        ----------

        [1] Deb, K., Thiele, L., Laumanns, M., & Zitzler, E. (2002, May).
            Scalable multi-objective optimization test problems.
            In Proceedings of the 2002 Congress on Evolutionary Computation.
            CEC'02 (Cat. No. 02TH8600) (Vol. 1, pp. 825-830). IEEE.
    """

    def set(self, **kwargs):
        self.name = 'DTLZ III Test Problem'

        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = [0.5 for x in range(self.dimension)]  ###
        self.global_optimum_coords = [0.5 for x in range(self.dimension)]

        # single objective problem
        self.costs = self.generate_objective_functions(**kwargs)

    def pareto_front(self, x):
        """ x -> y """

        p_f = []
        for i in range(0, len(self.costs)):
            p_f.append(0.5)
        return p_f

    def evaluate(self, x):

        k = 10  # k >= 1, it can be k = 5 is the offered value,

        m = len(self.costs)
        x = x.vector
        scores = []
        for i in range(0, m):
            fi = 1.0
            for j in range(0, m - i - 1):
                fi *= cos(0.5 * x[j] * pi)

            if i > 0:
                fi *= sin(x[m - i] * pi / 2.)
            # gm = 0.
            # for i in range(0, k):
            #     gm += (x[len(x) - i-1] - 0.5) ** 2.
            # fi *= (1. +  gm)
            # scores.append(fi)
            # g(xm)
            gm = float(k)
            for i in range(0, k):
                gm += (x[len(x) - i - 1] - 0.5) ** 2. - cos(20. * pi * (x[len(x) - i - 1] - 0.5))
            fi = fi * (1 + 100. * gm)
            scores.append(fi)

        return scores


class DTLZIV(BenchmarkFunction):
    """
    xi -> xi**alpha, where alpha = 100

        References
        ----------

        [1] Deb, K., Thiele, L., Laumanns, M., & Zitzler, E. (2002, May).
            Scalable multi-objective optimization test problems.
            In Proceedings of the 2002 Congress on Evolutionary Computation.
            CEC'02 (Cat. No. 02TH8600) (Vol. 1, pp. 825-830). IEEE.
    """

    def set(self, **kwargs):
        self.name = 'DTLZ II Test Problem'

        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=0.0, ub=1.0)

        self.global_optimum = [0.5 for x in range(self.dimension)]  ###
        self.global_optimum_coords = [0.5 for x in range(self.dimension)]

        # single objective problem
        self.costs = self.generate_objective_functions(**kwargs)

    def pareto_front(self, x):
        """ x -> y """

        p_f = []
        for i in range(0, len(self.costs)):
            p_f.append(0.5)
        return p_f

    def evaluate(self, x):

        k = 10  # k >= 1, it can be k = 5 is the offered value,

        alpha = 100
        m = len(self.costs)
        x = x.vector
        scores = []
        for i in range(0, m):
            fi = 1.0
            for j in range(0, m - i - 1):
                fi *= cos(0.5 * x[j] ** alpha * pi)

            if i > 0:
                fi *= sin(x[m - i] ** alpha * pi / 2.)
            gm = 0.
            for i in range(0, k):
                gm += (x[len(x) - i - 1] - 0.5) ** 2.
            fi *= (1. + gm)
            scores.append(fi)

        return scores


# TODO : finish the dtlz 5-7 problems and the dtlz test problems https://deap.readthedocs.io/en/master/api/benchmarks.html#deap.benchmarks.zdt1


class CEC2020MMF1(BenchmarkFunction):
    """
    Properties
    =================================================================
    Scalable number of variables :        x
    Scalable number of objectives:        x
    Pareto optima known:                  yes
    Pareto front geometry:                convex
    Pareto set geometry:                  nonlinear
    Scalable number of Pareto set:        x
    Nr of global optimums:                2
    NR of local optimums:                 1
    =================================================================

    Solution
    --------
    global pareto set:

    x1 = x1
    x2 = sin(6*pi*abs(x1-2)+pi)

    global pareto front:    f2 =  1 - sqrt(f1) , where 0<=f1<=1

    :param x1: [1,3]
    :param x2: [-1,1]
    :return: [f1, f2]
    """

    def set(self, **kwargs):
        self.name = 'CEC2020 -- MMF1 --'

        self.set_dimension = 2.0
        self.parameters = [{'name': 'x1', 'bounds': [1.0, 3.0]},
                           {'name': 'x2', 'bounds': [-1.0, 1.0]}]

        #self.global_optimum = 0.0
        #self.global_optimum_coords = [1., 3.]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x1 = x.vector[0]
        x2 = x.vector[1]

        a = np.where(x1 < 2., 1., np.e)
        f1 = np.abs(x1 - 2)
        f2 = 1 - np.abs(x1 - 2) ** 0.5 + 2. * (x2 - (a ** x1) * np.sin(6. * np.pi * np.abs(x1 - 2.) + np.pi)) ** 2.
        return [f1, f2]


class CEC2020MMF2(BenchmarkFunction):
    """
    Properties
    =================================================================
    Scalable number of variables :        x
    Scalable number of objectives:        x
    Pareto optima known:                  yes
    Pareto front geometry:                convex
    Pareto set geometry:                  nonlinear
    Scalable number of Pareto set:        x
    Nr of global optimums:                2
    NR of local optimums:                 1
    =================================================================

    Solution
    --------
    global pareto set:

    x1 = x2**2  if x1<1
         (x2-1) if 1<x1<2
    x2 = x2

    global pareto front:    f2 =  1 - sqrt(f1) , where 0<=f1<=1

    :param x1: [0,1]
    :param x2: [0,2]
    :return: [f1, f2]
    """

    def set(self, **kwargs):
        self.name = 'CEC2020 -- MMF2 --'

        self.set_dimension = 2.0
        self.parameters = [{'name': 'x1', 'bounds': [0.0, 1.0]},
                           {'name': 'x2', 'bounds': [0.0, 2.0]}]

        #self.global_optimum = 0.0
        #self.global_optimum_coords = [1., 3.]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x1 = x.vector[0]
        x2 = x.vector[1]

        f1 = np.abs(x1)

        a = x1 ** 0.5

        f2a = 1 - a + 2. * (4. * (x2 - a)) ** 2. - 2. * np.cos(20.0 * np.pi / (2.0 ** 0.5) * (x2 - a)) + 2.
        f2b = 1 - a + 2. * (4. * (x2 - 1.0 - a)) ** 2. - 2. * np.cos(20.0 * np.pi / (2.0 ** 0.5) * (x2 - 1.0 - a)) + 2.

        f2 = np.where(x2 < 1., f2a, f2b)

        return [f1, f2]


if __name__ == '__main__':
    # visualcheck
    test = PoloniFunction()
    test.plot_2d()

    test = CEC2020MMF1()
    test.plot_2d(f=0)
    test.plot_2d(f=1)

    test = CEC2020MMF2()
    test.plot_2d(f=0)
    test.plot_2d(f=1)