from .algorithm import Algorithm
from .problem import Problem
import numpy as np
import scipy.special as sp
from scipy import stats

"""
Distributions
"""


class Distribution(object):
    def __init__(self, name=None, mean=None, std=None, startpoint=None):
        self.name = name
        self.mean = mean
        self.std = std
        if startpoint is None:
            self.startpoint = self.mean
        else:
            self.startpoint = startpoint

    def pdf(self, x):
        pass

    def cdf(self, x):
        pass


class Normal(Distribution):
    """Normal distribution
    """

    def __init__(self, name, mean, std):
        self.name = name
        self.mean = mean
        self.std = std
        Distribution.__init__(self, name, mean, std)

    def pdf(self, x):
        """
        probability density function
        """
        z = (x - self.mean) / self.std
        p = np.exp(-0.5 * z ** 2) / np.sqrt(2 * np.pi) / self.std
        return p

    def cdf(self, x):
        """
        cumulative distribution function
        """
        z = (x - self.mean) / self.std
        p = 0.5 + sp.erf(z / np.sqrt(2)) / 2
        return p

    def inv_cdf(self, x):
        """
        inverse cumulative distribution function
        """
        z = sp.erfinv(2 * x - 1) * np.sqrt(2)
        p = self.std * z + self.mean
        return p


class Uniform(Distribution):
    """Uniform distribution
    """

    def __init__(self, name, mean, std):

        self.name = name
        self.mean = mean
        self.std = std
        self.a = self.mean - 3 ** 0.5 * self.std
        self.b = self.mean + 3 ** 0.5 * self.std

        Distribution.__init__(self, name, mean, std)

    def pdf(self, x):
        """probability density function
        """
        if len(x) == 1:
            p = 1 * (self.b - self.a) ** (-1)
        else:
            p = []
            for i in range(len(x)):
                p.append(1 * (self.b - self.a) ** (-1))

        return p

    def cdf(self, x):
        """cumulative distribution function
        """
        P = (x - self.a) * (self.b - self.a) ** (-1)
        return P


class StochasticModel(object):
    """Creates an object with random variable attributes
    Args:
        list with: [distribution, mean, std]
    """

    def __init__(self, *args):
        self.dist_func = []
        mean = []
        std = []
        self.dist_name = []

        for dist, mu, sig in args:

            if dist == 'normal':
                self.dist_func.append(Normal(dist, mu, sig))

            elif dist == 'uniform':
                self.dist_func.append(Uniform(dist, mu, sig))

            self.dist_name.append(dist)
            mean.append(mu)
            std.append(sig)

        self.mean = np.array(mean)
        self.std = np.array(std)
        """ Correlation Matrix"""
        self.rho = np.identity(len(args))


"""
Reliability Analysis Methods
"""


class FORM(Algorithm):
    """Performs the FORM algorithm
        The goal is to find the reliability index for a nonlinear limit state function g(Xi).
    """

    def __init__(self, limit_state: Problem, name="First Order Reliability Method"):
        super().__init__(limit_state, name)
        self.min_val, self.max_val = 1, 10
        # self.size = self.options['max_population_size']
        self.dimension = 1
        self.limit_state = limit_state
        self.mean = np.random.uniform(self.min_val, self.max_val, self.dimension)
        self.std = np.random.uniform(self.max_val - 1, self.max_val, self.dimension)
        self.tol = 1e-3

    def generate(self):
        X = StochasticModel(['normal', int(self.mean), int(self.std)],
                            ['normal', int(self.mean), int(self.std)])
        return X

    def derivative(self, limit_state, points):
        """Compute derivative of func at points using finite differences

           ddx = \\frac{func(points + eps) - func(points - eps)}{2 * eps}

        Args:
            limit_state (function): function with N parameters
            points (array): array with N-dimension
        Returns:
            derivative: list with derivative
            for instance:
                derivative[0] = d/d X1 func evaluated at points[0]
                derivative[1] = d/d X2 func evaluated at points[1]
        """
        d = []
        eps = 1e-8
        for i, p in enumerate(points):
            step_up, step_down = list(points), list(points)  # copy list

            # approximate derivative by tangent line with eps distance at
            step_up[i] = p + eps
            step_down[i] = p - eps
            d.append((limit_state.evaluate(*step_up) - limit_state.evaluate(*step_down)) / (2 * eps))

        return np.array(d)

    def std_linear(self, grad_g_x, sig):
        """Compute the standard deviation of g(Xi) using linear approximation
            . math::
                sig_g = (sum_i^n (grad_g_xi * sig_Xi)^2)^(1/2)
        Args:
            grad_g_x (array): partial derivative of g with respect xi
            sig (array): standard deviation of variables
        Returns:
            std_g (float): standard deviation of g(Xi)
        """
        std_g = 0
        for dg_dx, s in zip(grad_g_x, sig):
            std_g += (dg_dx ** 2 * s ** 2)
        std_g = std_g ** (1 / 2)
        return std_g

    def run(self):
        iteration = 1
        convergence = False
        X = self.generate()
        # initial beta
        mu_g = self.limit_state.evaluate(*X.mean)
        grad_g_x = self.derivative(self.limit_state, X.mean)
        sig_g = self.std_linear(grad_g_x, X.std)
        beta = mu_g / sig_g
        alpha = - grad_g_x * X.std / sig_g

        # Initialize design points
        x = X.mean + beta * X.std * alpha

        while not convergence:

            for i, dist in enumerate(X.dist_name):
                if dist != 'norm':
                    # equivalent values
                    X.std[i] = (1 / (X.dist_func[i].pdf(x[i]))
                                * stats.norm.pdf(
                                stats.norm.ppf(
                                    X.dist_func[i].cdf(x[i]))))
                    X.mean[i] = x[i] - X.std[i] * (stats.norm.ppf(
                        X.dist_func[i].cdf(x[i])))

            # transform to standard space
            z = (x - X.mean) / X.std

            # compute gradient of g with respect to z
            grad_g_x = self.derivative(self.limit_state, x)
            grad_g_z = grad_g_x * X.std

            beta_previous = beta
            beta = (self.limit_state.evaluate(*x) - grad_g_z @ z) / np.linalg.norm(grad_g_z)
            alpha = - grad_g_z / np.linalg.norm(grad_g_z)

            # update design points in standard space
            z = alpha * beta
            # transform to physical space
            x_updt = X.mean + z * X.std

            condition1 = np.linalg.norm(x_updt - x) / np.linalg.norm(x_updt) < self.tol
            condition2 = abs(np.round(beta, 3) - np.round(beta_previous, 3)) < self.tol
            if condition2 or condition1:
                convergence = True
            if not convergence:
                x = x_updt
                iteration += 1
        return x, beta, iteration
