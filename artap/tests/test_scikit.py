import math

import unittest
from scipy import integrate

from artap.problem import Problem
from artap.algorithm_nlopt import NLopt, LN_BOBYQA
from artap.algorithm_genetic import NSGA_II

from artap.benchmark_functions import Booth

from artap.results import Results

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

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

    def eval(self, x):
        return Booth.eval(x)

class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem_one(self):
        problem = MyProblemBooth("LocalPythonProblem")
        algorithm = NLopt(problem)
        algorithm.options['algorithm'] = LN_BOBYQA
        algorithm.options['n_iterations'] = 50
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum, 1e-6, 3)

if __name__ == '__main__':
    unittest.main()

"""

#!/usr/bin/python3

import numpy as np
from matplotlib import pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

np.random.seed(1)


def f(x):
    return x * np.sin(x)

# ----------------------------------------------------------------------
#  First the noiseless case
X = np.atleast_2d([1., 3., 5., 6., 7., 8.]).T

# Observations
y = f(X).ravel()

# Mesh the input space for evaluations of the real function, the prediction and
# its MSE
x = np.atleast_2d(np.linspace(0, 10, 1000)).T

# Instanciate a Gaussian Process model
kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

# Fit to data using Maximum Likelihood Estimation of the parameters
gp.fit(X, y)

# Make the prediction on the meshed x-axis (ask for MSE as well)
y_pred, sigma = gp.predict(x, return_std=True)

# Plot the function, the prediction and the 95% confidence interval based on
# the MSE
fig = plt.figure()
plt.plot(x, f(x), 'r:', label=u'$f(x) = x\,\sin(x)$')
plt.plot(X, y, 'r.', markersize=10, label=u'Observations')
plt.plot(x, y_pred, 'b-', label=u'Prediction')
plt.fill(np.concatenate([x, x[::-1]]),
         np.concatenate([y_pred - 1.9600 * sigma,
                        (y_pred + 1.9600 * sigma)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
plt.ylim(-10, 20)
plt.legend(loc='upper left')
# plt.show()







import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import scipy.stats as st

np.random.seed(1)

# Quadratic 2d potential
def func(x):
    return np.sum(x**2, axis=-1)


# Grid
lim = 1
res = 50
lin = np.linspace(-lim, lim, res)

# x1.shape = (50, 50)
x1, x2 = np.meshgrid(lin, lin)
# xx.shape = (2500, 2)
xx = np.vstack((x1.flatten(), x2.flatten())).T

# Analytic function values
y_analytic = func(xx)
y_analytic = y_analytic.reshape(-1, res)

# Observed data
obs = 15
# X.shape = (15, 2)
X = np.stack(
        (np.random.choice(lin, obs), np.random.choice(lin, obs)),
        axis=-1
)
y_obs = func(X)

kernel = RBF()
gp = GaussianProcessRegressor(kernel=kernel,
                              n_restarts_optimizer=10)
gp.fit(X, y_obs)
print("Learned kernel", gp.kernel_)
# y_mean.shape = (2500, )
# y_cov.shape = (2500, 2500)
y_mean, y_cov = gp.predict(xx, return_cov=True)

posterior_nums = 3
posteriors = st.multivariate_normal.rvs(mean=y_mean, cov=y_cov,
                                        size=posterior_nums)

fig, axs = plt.subplots(posterior_nums+1)

ax = axs[0]
ax.contourf(x1, x2, y_analytic)
ax.plot(X[:, 0], X[:, 1], "r.", ms=12)

for i, post in enumerate(posteriors, 1):
    axs[i].contourf(x1, x2, post.reshape(-1, res))

plt.tight_layout()
plt.show()

"""