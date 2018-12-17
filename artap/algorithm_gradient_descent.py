from .problem import Problem
from .algorithm import Algorithm
from .population import Population
from .individual import Individual


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

    def run(self):
        # TODO: add adaptive step size
        population = Population(self)
        self.problem.populations.append(population)
        n = self.options["n_iterations"]
        x = [0] * n
        dx = [0] * n
        x[0] = self.options["x0"]
        dx[0] = [0, 0]
        h = self.options["h"]
        for i in range(1, n):
            individual = Individual(x[i-1], self.problem)
            gradient = self.problem.evaluate_gradient_richardson(individual)
            x[i] = []
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
                print(h)

            population.individuals.append(individual)

        return x
