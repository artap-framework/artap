from .problem import Problem
import numpy as np
import scipy.special as sp

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


"""
Reliability Analysis Methods
"""


class FORM():
    def __init__(self, problem: Problem, name="First Order Reliability Method"):
        super().__init__(problem, name)

    def run(self):
        pass
