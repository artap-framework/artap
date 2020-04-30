"""
Implementation of the Semi analytical TEAM Benchmark problem in Artap.

The ProblemAnalytical class contains the description oe optimization problem, 10 design parameters, 1-3 goal functions,
the initialization of the database and the functions for the realized semi-analytical calculation.

The detailed description of the analytical model can be founc here: doi....
"""

import math
import pylab as pl

from scipy import integrate
from artap.problem import Problem
from artap.individual import Individual
from artap.algorithm_nlopt import NLopt, LN_BOBYQA
from artap.datastore import FileDataStore
from artap.results import Results


class ProblemAnalytical(Problem):
    def set(self):

        self.name = "Semi-Analytical solution"

        # The problem has 10 parameters, because the optimized coil has 20 turns, but during the solution, only the
        # symmetrycal cases has been assumed. Other simplification is that only the x coordinate of the turn can be
        # changed.
        #
        # Note: 'initial_value' should be given for the nl_opt and the bayesopt methods, not sufficient for genetic
        #        algorithms
        self.parameters = [{'name': 'x1', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x2', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x3', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x4', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x5', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x6', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x7', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x8', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x9', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]},
                           {'name': 'x10', 'initial_value': 0.01, 'bounds': [5.01e-3, 50e-3]}]

        # The three, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

        # Initialize a database to store the data into the given space
        self.data_store = FileDataStore(self, database_name="/tmp/team_multi.db", mode="write")

    def intl22(self, R2, R, dZ, phi):
        return math.sqrt(R2 ** 2 + R ** 2 - 2.0 * R2 * R * math.cos(phi) + dZ ** 2)

    def intg(self, R2, R, dZ):
        # div J = 0 - nonconstant current density
        f = lambda phi: math.log(R2 - R * math.cos(phi) + self.intl22(R2, R, dZ, phi)) * math.cos(phi)
        # constant current density
        # f = lambda phi: R * math.cos(phi)**2 * math.log(R2 - R * math.cos(phi) + self.intl22(R2, R, dZ, phi)) + math.cos(phi) * self.intl22(R2, R, dZ, phi)
        return integrate.quad(f, 0, 2.0 * math.pi, epsabs=1e-3, epsrel=1e-3)[0]

    def inth(self, R2, R, dZ):
        # div J = 0 - nonconstant current density
        f = lambda phi: - math.log(dZ + self.intl22(R2, R, dZ, phi))
        return integrate.quad(f, 0, 2.0 * math.pi, epsabs=1e-3, epsrel=1e-3)[0]

    def integral(self, rc, zc, R, Z):

        w = 0.001
        h = 0.0015

        R1 = rc
        R2 = rc + w
        Z1 = zc
        Z2 = zc + h

        mu0 = 4.0 * math.pi * 1e-7
        Jext = 2e6
        # div J = 0 - nonconstant current density
        C = mu0 * Jext * w * h / (4 * math.pi * (Z2 - Z1) * math.log(R2 / R1))
        # constant current density
        # C = mu0 * Jext / (4.0 * math.pi)

        # upper coil
        Bru = C * (self.intg(R2, R, Z2 - Z) - self.intg(R2, R, Z1 - Z) - self.intg(R1, R, Z2 - Z) + self.intg(R1, R,
                                                                                                              Z1 - Z))
        Bzu = C * (self.inth(R2, R, Z2 - Z) - self.inth(R2, R, Z1 - Z) - self.inth(R1, R, Z2 - Z) + self.inth(R1, R,
                                                                                                              Z1 - Z))

        # lower coil
        Brl = C * (self.intg(R2, R, -Z1 - Z) - self.intg(R2, R, -Z2 - Z) - self.intg(R1, R, -Z1 - Z) + self.intg(R1, R,
                                                                                                                 -Z2 - Z))
        Bzl = C * (self.inth(R2, R, -Z1 - Z) - self.inth(R2, R, -Z2 - Z) - self.inth(R1, R, -Z1 - Z) + self.inth(R1, R,
                                                                                                                 -Z2 - Z))

        return [Bru + Brl, Bzu + Bzl]

    def integral_all(self, R, Z, x):
        Br = 0.0
        Bz = 0.0

        for k in range(0, 9):
            rc = x[k]
            zc = k * 1.5e-3

            B = self.integral(rc, zc, R, Z)

            Br = Br + B[0]
            Bz = Bz + B[1]

        return [Br, Bz]

    def evaluate(self, individual):
        B0 = 2e-3

        dxy = 0.5e-3
        nx = 8
        ny = 8
        dx = (5e-3 - dxy) / (nx - 1)
        dy = (5e-3 - dxy) / (ny - 1)
        f1 = 0.0
        f2 = 0.0
        f3 = 0.0

        for i in range(0, nx):
            xx = dxy + i * dx
            for j in range(0, ny):
                yy = dxy + j * dy

                [Br, Bz] = self.integral_all(xx, yy, individual.vector)
                Bp1s = math.sqrt((Br - 0.0) ** 2 + (Bz - B0) ** 2)
                f1 = max(f1, Bp1s)

                dxsi = 0.5e-3
                [Brp, Bzp] = self.integral_all(xx + dxsi, yy, individual.vector)
                [Brm, Bzm] = self.integral_all(xx - dxsi, yy, individual.vector)
                Bp2 = math.sqrt((Brp - Br) ** 2 + (Bzp - Bz) ** 2) + math.sqrt((Brm - Br) ** 2 + (Bzm - Bz) ** 2)
                f3 = max(f2, Bp2)

        f2 = sum(individual.vector) * 1e3

        return [f1, f2]


def optim_single():
    problem = ProblemAnalytical()

    # optimization
    algorithm = NLopt(problem)
    algorithm.options['algorithm'] = LN_BOBYQA
    algorithm.options['n_iterations'] = 100

    algorithm.run()

    b = Results(problem)
    b.pareto_plot()


def check_analytical():
    """
    Checks the functionality of the semi analytical function.
    :return:
    """
    vec = [0.00808, 0.0149, 0.00674, 0.0167, 0.00545, 0.0106, 0.0117, 0.0111, 0.01369, 0.00619]
    # vec = [5e-3] * 10
    # vec = [10e-3] * 10
    ind = Individual(vec)
    problem_analytical = ProblemAnalytical()
    a = problem_analytical.evaluate(ind)

    print("anal ", a)


def check_plot():
    """
    This function makes a plot from the solution along the z axis at r = 0.00619 m.
    Compares the function of the semi-analytical integral values with 20 different points, which calculated by Agros.
    """

    problem_analytical = ProblemAnalytical()

    # Agros
    za = pl.linspace(0, 0.03, 20)
    Bra = [1.50901e-10, -5.11533e-6, -1.11251e-5, -1.91503e-5, -3.08628e-5, -4.90497e-5, -7.81889e-5, -0.000124345,
           -0.000167617, -1.92214e-6, 0.000169002, 0.000127021, 8.07604e-5, 5.16543e-5, 3.38259e-5, 2.27073e-5,
           1.56076e-5, 1.09697e-5, 7.88858e-6, 5.78184e-6]
    Bza = [3.22309e-5, 3.34485e-5, 3.72951e-5, 4.43861e-5, 5.60296e-5, 7.48665e-5, 0.000107128, 0.000170325,
           0.000319292, 0.000505151, 0.000322344, 0.000170171, 0.000105039, 7.12451e-5, 5.08364e-5, 3.73934e-5,
           2.81052e-5, 2.14857e-5, 1.66542e-5, 1.30694e-5]

    z = pl.linspace(0, 0.03, 100)
    Br = []
    Bz = []

    for i in range(len(z)):
        r1 = 0.00619
        z1 = 9 * 1.5e-3
        B = problem_analytical.integral(r1, z1, 0.005, z[i])

        Br.append(B[0])
        Bz.append(B[1])

    # Plot the comparison of the analytical and the agros solution
    pl.subplot(2, 1, 1)
    pl.plot(z, Bz, label="Semi-analytical method")
    pl.plot(za, Bza, 'x', label="Agros")
    pl.ylabel("Bz [T]")
    pl.legend()
    pl.subplot(2, 1, 2)
    pl.plot(z, Br, label="Semi-analytical method")
    pl.plot(za, Bra, 'x', label="Agros")
    pl.ylabel("Br [T]")
    pl.xlabel('r [m]')
    pl.show()


# check_analytical()
check_plot()
optim_single()
