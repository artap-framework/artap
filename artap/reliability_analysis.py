import time

from .algorithm import Algorithm
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .individual import Individual
from .operators import CustomGenerator
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

            if dist == 'norm':
                self.dist_func.append(getattr(stats, dist)(loc=mean, scale=sig))

            elif dist == 'uniform':
                self.dist_func.append(getattr(stats, dist)(loc=mean, scale=sig))

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


# ToDo: Convert this class to the optimization class.
class FORM(GeneralEvolutionaryAlgorithm):
    """Performs the FORM-HLRF algorithm
        The goal is to find the reliability index for a nonlinear limit state function g(Xi).

        HL_RF algorithm steps:
        1) Define the limit state function (𝑔) and the convergence criterion (tol = 1e-3), statistical characteristics
         of basic random variables (mean, standard deviation, and distribution function for each random variable).
        2) Transfer the random variables from 𝑋-space to 𝑈-space according to
            .. math::
                U = (X - \mu_X^{e}) / \sigma_X^{e}
        3) Compute the gradient vector and limit state function at point U𝑘.
        4) Compute the cost function using
            .. math::
                U^{k+1} = [(G(U^{k}) - \grad G(U^{k})U^{k}) / \norm{\grad G(U^{k})}] \alpha^{k}

            where \alpha^{k} is sensivity factor that can be calculated by:
            ..math::
                \alpha^{k} = -(\grad G(U^{k})) / \norm{\grad G(U^{k})}

        5) Transfer the basic random variables from 𝑈-space to 𝑋-space.
        6) Control the convergence conditions as below; if true then the method is converged, stop and go to step (7);
        else, 𝑘 = 𝑘+1 and go to step (2).
        7) Estimate the failure probability by
            ..math::
                P_f ~~ \phi(-\beta)
            where \phi is the CDF of the standard normal distribution and \beta = \norm{U^{*}} is the reliability index.

        ..Reference::

        [1] A Novel Algorithm for Structural Reliability Analysis Based on Finite Step Length and Armijo Line Search
            https://www.mdpi.com/2076-3417/9/12/2546
        [2] A Comparative Study of First-Order Reliability Method-Based Steepest Descent Search Directions for
         Reliability Analysis of Steel Structures, https://www.hindawi.com/journals/ace/2017/8643801/
        [3] Reliability analysis and optimal design under uncertainty - Focus on adaptive surrogate-based approaches
            https://tel.archives-ouvertes.fr/tel-01737299/document
    """

    def __init__(self, problem: Problem, name="First Order Reliability Method"):
        super().__init__(problem, name)
        self.min_val, self.max_val = 1, 10
        # self.size = self.options['max_population_size']
        self.dimension = len(self.problem.parameters)
        self.problem = problem
        self.mean = np.random.uniform(self.min_val, self.max_val, self.dimension)
        self.std = np.random.uniform(self.max_val - 1, self.max_val, self.dimension)
        self.cov = np.diag(self.std)
        self.tol = 1e-3
        self.generator = CustomGenerator(self.problem.parameters, self.individual_features)

    def generate(self):
        # X = StochasticModel(['norm', int(self.mean), int(self.std)],
        #                     ['norm', int(self.mean), int(self.std)])
        new_individuals = np.random.multivariate_normal(self.mean, self.cov, self.options['max_population_size'])
        self.generator.init(new_individuals)
        individuals = self.generator.generate()
        return individuals

    def make_individual(self):
        self.mean = Individual(self.mean, self.individual_features)
        self.std = Individual(self.std, self.individual_features)

    def derivative(self, problem, points):
        """Compute derivative of func at points using finite differences

           ddx = \\frac{func(points + eps) - func(points - eps)}{2 * eps}

        Args:
            problem (function): function with N parameters
            points (array): array with N-dimension
        Returns:
            derivative: list with derivative
            for instance:
                derivative[0] = d/d X1 func evaluated at points[0]
                derivative[1] = d/d X2 func evaluated at points[1]
        """
        d = []
        eps = 1e-8
        for i, p in enumerate(points.vector):
            step_up, step_down = points, points  # copy list

            # approximate derivative by tangent line with eps distance at
            step_up.vector[i] = p + eps
            step_down.vector[i] = p - eps
            d.append((problem.evaluate(step_up)[0] - problem.evaluate(step_down)[0]) / (2 * eps))

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
        mean = []
        individuals = self.generate()
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

            self.problem.data_store.sync_individual(individual)
            mean.append(np.mean(individual.vector))
        # X = self.generate()
        # initialize beta and alpha
        grad_g_x = self.derivative(self.problem, self.mean)
        self.evaluate(individuals)
        self.make_individual()
        mu_g = self.problem.evaluate(self.mean)
        grad_g_x = self.derivative(self.problem, self.mean)
        sig_g = self.std_linear(grad_g_x, self.std)
        beta = mu_g / sig_g
        alpha = - grad_g_x * self.std / sig_g

        # Initialize design points
        individuals = self.mean + beta * self.std * alpha
        start = time.time()
        self.problem.logger.info("CMA_ES: {}/{}".format(self.options['max_population_number'],
                                                        self.options['max_population_size']))
        while not convergence:

            for it in range(self.options['max_population_number']):
                # for i, dist in enumerate(X.dist_name):
                #     if dist != 'norm':
                #         # equivalent values
                #         X.std[i] = (1 / (X.dist_func[i].pdf(x[i]))
                #                     * stats.norm.pdf(
                #                     stats.norm.ppf(
                #                         X.dist_func[i].cdf(x[i]))))
                #         X.mean[i] = x[i] - X.std[i] * (stats.norm.ppf(
                #             X.dist_func[i].cdf(x[i])))

                # transform to standard space
                transform_individuals = (individuals - self.mean) / self.std

                # compute gradient of g with respect to z
                grad_g_x = self.derivative(self.problem, individuals)
                grad_g_z = grad_g_x * self.std

                beta_previous = beta
                beta = (self.problem.evaluate(*individuals) - grad_g_z @ transform_individuals) \
                       / np.linalg.norm(grad_g_z)
                alpha = - grad_g_z / np.linalg.norm(grad_g_z)

                # update design points in standard space
                transform_individuals = alpha * beta
                # transform to physical space
                physical_transform = self.mean + transform_individuals * self.std

                condition1 = np.linalg.norm(physical_transform - individuals)\
                             / np.linalg.norm(physical_transform) < self.tol
                condition2 = abs(np.round(beta, 3) - np.round(beta_previous, 3)) < self.tol
                if condition2 or condition1:
                    convergence = True
                if not convergence:
                    individuals = physical_transform
                    # iteration += 1
                    for individual in individuals:
                        # add to population
                        individual.population_id = it + 1
                        # append to problem
                        self.problem.individuals.append(individual)
                        # sync to datastore
                        self.problem.data_store.sync_individual(individual)

                # for individual in individuals:
                #     # add to population
                #     individual.population_id = it + 1
                #     # append to problem
                #     self.problem.individuals.append(individual)
                #     # sync to datastore
                #     self.problem.data_store.sync_individual(individual)

        return individuals, beta, iteration
