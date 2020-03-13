from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .individual import Individual
import collections
from .job import Job


class GradientDescent(Algorithm):
    """ Gradient descent algorithms """

    def __init__(self, problem: Problem, name="GradientDescent"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='n_iterations', default=10,
                             desc='Maximum number of iterations')

        self.options.declare(name='x0', default=0,
                             desc='initial point')

        self.options.declare(name='h', default=0.1,
                             desc='step')

    def evaluate_gradient_richardson(self, population, individual):
        x0 = individual.vector
        gradient = [0] * len(x0)

        h = 1e-6
        job = Job(self.problem, population)
        y = job.evaluate_scalar(x0)
        for i in range(len(x0)):
            x = x0.copy()
            x[i] += h
            y_h = job.evaluate_scalar(x)
            d_0_h = gradient[i] = (y_h - y) / h
            x[i] += h
            y_2h = job.evaluate_scalar(x)
            d_0_2h = (y_2h - y) / 2 / h
            gradient[i] = (4 * d_0_h - d_0_2h) / 3

        return gradient

    def evaluate_gradient(self, individual):
        x0 = individual.vector
        gradient = [0] * len(x0)
        x0 = individual.parameters
        y = self.evaluate(x0)
        h = 1e-6
        for i in range(len(x0)):
            x = x0.copy()
            x[i] += h
            y_h = self.evaluate(x)
            if isinstance(y_h, collections.Iterable):
                m = len(y_h)
                gradient[i] = []
                for j in range(m):
                    gradient[i].append((y_h[j] - y[j]) / h)
            else:
                gradient[i] = (y_h - y) / h

        return gradient

    def run(self):
        population = Population()
        # append population
        self.problem.populations.append(population)

        # TODO: add adaptive step size
        n = self.options["n_iterations"]
        x = [] * n
        dx = [] * n
        x.append(self.options["x0"])
        dx.append([0, 0])
        h = self.options["h"]
        for i in range(1, n):
            x.append([])
            dx.append([])
            individual = Individual(x[i-1])
            gradient = self.evaluate_gradient_richardson(population, individual)
            dx[i] = gradient

            for j in range(len(x[i-1])):
                x[i].append(x[i-1][j] - h * gradient[j])

            if i > 1:
                d = 0
                n = 0
                for j in range(len(x[i])):
                    n += (dx[i][j] - dx[i-1][j]) * (x[i][j] - x[i-1][j])
                    d += (dx[i][j] - dx[i-1][j])**2
                h = n / d
            population.individuals.append(individual)
