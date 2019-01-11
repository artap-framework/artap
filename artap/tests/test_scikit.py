import math

import unittest
from scipy import integrate

from artap.problem import Problem
# from artap.algorithm_nlopt import NLopt, LN_BOBYQA
from artap.algorithm_genetic import NSGA_II
# from artap.algorithm_bayesopt import BayesOptSerial

from artap.benchmark_functions import Booth

from artap.results import Results

# import numpy as np
# from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel as C
# from sklearn.neural_network import MLPClassifier


class MyProblem(Problem):
    def __init__(self, name, costs):
        parameters = {'x1': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x2': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x3': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x4': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x5': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x6': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x7': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x8': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x9': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
                      'x10': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]}}

        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1

    def intl22(self, R2, R, dZ, phi):
        return math.sqrt(R2 ** 2 + R ** 2 - 2.0 * R2 * R * math.cos(phi) + dZ ** 2)

    def intg(self, R2, R, dZ):
        # div J = 0 - nonconstant current density
        f = lambda phi: math.log(R2 - R * math.cos(phi) + self.intl22(R2, R, dZ, phi)) * math.cos(phi)
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

        # upper coil
        Bru = C * (self.intg(R2, R, Z2 - Z) - self.intg(R2, R, Z1 - Z) - self.intg(R1, R, Z2 - Z) + self.intg(R1, R, Z1 - Z))
        Bzu = C * (self.inth(R2, R, Z2 - Z) - self.inth(R2, R, Z1 - Z) - self.inth(R1, R, Z2 - Z) + self.inth(R1, R, Z1 - Z))

        # lower coil
        Brl = C * (self.intg(R2, R, -Z1 - Z) - self.intg(R2, R, -Z2 - Z) - self.intg(R1, R, -Z1 - Z) + self.intg(R1, R, -Z2 - Z))
        Bzl = C * (self.inth(R2, R, -Z1 - Z) - self.inth(R2, R, -Z2 - Z) - self.inth(R1, R, -Z1 - Z) + self.inth(R1, R, -Z2 - Z))

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

    def eval(self, x):
        pass


class MyProblemOne(MyProblem):
    def __init__(self, name):
        super().__init__(name, costs=['F1'])

    def eval(self, x):
        B0 = 2e-3

        dxy = 0.5e-3
        nx = 8
        ny = 8
        dx = (5e-3 - dxy) / (nx - 1)
        dy = (5e-3 - dxy) / (ny - 1)

        f1 = 0.0
        for i in range(0, nx):
            xx = dxy + i * dx
            for j in range(0, ny):
                yy = dxy + j * dy

                [Br, Bz] = self.integral_all(xx, yy, x)
                Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
                f1 = max(f1, Bp1s)

        return f1

class MyProblemMultiTwo(MyProblem):
    def __init__(self, name):
        super().__init__(name, costs=['F1', 'F2'])

    def eval(self, x):
        B0 = 2e-3

        dxy = 0.5e-3
        nx = 8
        ny = 8
        dx = (5e-3 - dxy) / (nx - 1)
        dy = (5e-3 - dxy) / (ny - 1)

        f1 = 0.0
        f2 = sum(x) * 1e3
        for i in range(0, nx):
            xx = dxy + i * dx
            for j in range(0, ny):
                yy = dxy + j * dy

                [Br, Bz] = self.integral_all(xx, yy, x)
                Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
                f1 = max(f1, Bp1s)

        return [f1, f2]


class MyProblemMultiThree(MyProblem):
    def __init__(self, name):
        super().__init__(name, costs=['F1', 'F2', 'F3'])

    def eval(self, x):
        B0 = 2e-3

        dxy = 0.5e-3
        nx = 8
        ny = 8
        dx = (5e-3 - dxy) / (nx - 1)
        dy = (5e-3 - dxy) / (ny - 1)

        f1 = 0.0
        f2 = sum(x)*1e3
        f3 = 0.0
        for i in range(0, nx):
            xx = dxy + i * dx
            for j in range(0, ny):
                yy = dxy + j * dy

                [Br, Bz] = self.integral_all(xx, yy, x)
                Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
                f1 = max(f1, Bp1s)

                dxsi = 0.5e-3
                [Brp, Bzp] = self.integral_all(xx + dxsi, yy, x)
                [Brm, Bzm] = self.integral_all(xx - dxsi, yy, x)
                Bp3 = math.sqrt((Brp - Br) ** 2 + (Bzp - Bz) ** 2) + math.sqrt((Brm - Br) ** 2 + (Bzm - Bz) ** 2)
                f3 = max(f3, Bp3)

        return [f1, f2, f3]

class MyProblemBooth(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-10, 10], 'precision': 1e-1}}

        # costs = {'F': {'type': Problem.MINIMIZE, 'value': 0.0}}
        costs = ['F']
        super().__init__(name, parameters, costs)
        self.options['max_processes'] = 1
        self.options['save_level'] = "population"

        self.counter = 0

        # surrogate model
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        kernel = 1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0), nu=1.5)
        self.surrogate = GaussianProcessRegressor(kernel=kernel)
        # self.surrogate = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

        self.surrogate_prepared = False
        self.surrogate_predict_counter = 0
        self.surrogate_eval_counter = 0
        self.counter_step = 40

    def eval(self, x):
        self.counter += 1

        if self.counter % self.counter_step == 0:
            # surrogate model
            counter_eff = 100.0 * self.surrogate_predict_counter / self.counter
            # speed up
            if (counter_eff > 30):
                self.counter_step = int(self.counter_step * 1.5)
            print("learning", self.counter, ", predict eff: ", counter_eff, ", counter_step: ", self.counter_step)

            x_data = []
            y_data = []
            for population in self.populations:
                for individual in population.individuals:
                    if individual.is_evaluated:
                        x_data.append(individual.parameters)
                        y_data.append(individual.costs[0])

            #print("x_data", x_data)
            #print("y_data", y_data)

            #clf = linear_model.SGDRegressor()
            #clf = linear_model.SGDRegrBayesianRidgeessor()
            #clf = linear_model.LassoLars()
            #clf = linear_model.TheilSenRegressor()
            #clf = linear_model.LinearRegression()

            self.surrogate.fit(x_data, y_data)
            self.surrogate_prepared = True

        evaluation = True
        if self.surrogate_prepared:
            p, sigma = self.surrogate.predict([x], return_std=True)
            # p = self.surrogate.predict([x])

            # sigma = 0
            if sigma < 0.01:
                value = p[0]
                self.surrogate_predict_counter += 1
                evaluation = False
                # print("x: ", x, "prediction: ", p[0], ", sigma: ", sigma)
            else:
                # value = Booth.eval(x)
                self.surrogate_eval_counter += 1
                # print("x: ", x, "prediction: ", p[0], ", value: ", value, "diff: ", math.fabs(p - value), ", sigma: ", sigma)

        if evaluation:
            value = Booth.eval(x)

        return value


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def xtest_local_problem_one(self):
        problem = MyProblemBooth("LocalPythonProblem")

        # algorithm = BayesOptSerial(problem)
        # algorithm.options['verbose_level'] = 0
        # algorithm.options['n_iterations'] = 100

        # algorithm = NLopt(problem)
        # algorithm.options['algorithm'] = LN_BOBYQA
        # algorithm.options['n_iterations'] = 200

        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 80
        algorithm.options['max_population_size'] = 20

        algorithm.run()

        print("surrogate_predict_counter: ", problem.surrogate_predict_counter)
        print("surrogate_eval_counter: ", problem.surrogate_eval_counter)

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum, 1e-6, 3)


if __name__ == '__main__':
    unittest.main()