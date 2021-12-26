from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from .operators import GradientEvaluator, RandomGenerator
from .individual import Individual
import time
import math


class GradientDescent(GeneticAlgorithm):
    """ Gradient descent algorithms """

    def __init__(self, problem: Problem, generator=None, name="GradientDescent"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='n_iterations', default=10,
                             desc='Maximum number of iterations')
        self.options.declare(name='step', default=0.1,
                             desc='Step')
        self.options.declare(name='minimal_step', default=1e-6,
                             desc='Minimal step')
        self.options.declare(name='algorithm', default="fixed",
                             desc='Type of algorithm: fixed, adaptive, adagrad, rmsprop, adam')
        self.options.declare(name='c', default=1e-4,
                             desc='Armijo coefficient (Adaptive)')
        self.options.declare(name='beta1', default=1e-4,
                             desc='Coefficient beta 1 (Adam)')
        self.options.declare(name='beta2', default=1e-4,
                             desc='Coefficient beta 2 (Adam)')
        self.options.declare(name='decay_rate', default=1e-4,
                             desc='Decay Rate (RMSprop)')

        # compute gradients
        self.evaluator = GradientEvaluator(self)
        self.individual_features['gradient'] = dict()

        # set default generator
        if generator is None:
            self.generator = RandomGenerator(self.problem.parameters, self.individual_features)
            self.generator.init(1)
        else:
            self.generator = generator

    def step_fixed(self, individual):
        x = []
        for i in range(len(individual.vector)):
            x.append(individual.vector[i] - self.options["step"] * individual.features['gradient'][i])

        return x

    def step_adaptive(self, individual):
        # Armijo line search
        h_t = self.options["step"]
        c = self.options["c"]

        grad_sqr = 0
        for i in range(len(individual.vector)):
            grad_sqr = grad_sqr + individual.features['gradient'][i] ** 2

        x_static = []
        for i in range(len(individual.vector)):
            x_static.append(individual.vector[i])
        individual_static = Individual(x_static, self.individual_features)
        self.evaluate([individual_static])

        while True:
            x_armijo = []
            for i in range(len(individual.vector)):
                x_armijo.append(individual.vector[i] - h_t * individual.features['gradient'][i])
            individual_armijo = Individual(x_armijo, self.individual_features)
            self.evaluate([individual_armijo])

            satisfied = True
            for i in range(len(individual.costs)):
                if individual_armijo.costs[i] > individual_static.costs[i] - c * h_t * grad_sqr:
                    satisfied = False
            if satisfied:
                return x_armijo

            # step too small
            if h_t < self.options["minimal_step"]:
                return x_armijo

            h_t = h_t / 2.0

    def step_adagrad(self, individual):
        x = []
        for i in range(len(individual.vector)):
            self.cache_grad_sqr[i] += individual.features['gradient'][i] ** 2

            x.append(individual.vector[i] - self.options["step"] * individual.features['gradient'][i] /
                     (math.sqrt(self.cache_grad_sqr[i] + 1e-6)))

        return x

    def step_rmsprop(self, individual):
        x = []
        for i in range(len(individual.vector)):
            self.cache_grad_sqr[i] += self.options["decay_rate"] * self.cache_grad_sqr[i] \
                                      + (1.0 - self.options["decay_rate"]) * individual.features['gradient'][i] ** 2

            x.append(individual.vector[i] - self.options["step"] * individual.features['gradient'][i] /
                     (math.sqrt(self.cache_grad_sqr[i] + 1e-6)))

        return x

    def step_adam(self, individual):
        x = []
        for i in range(len(individual.vector)):
            self.adam_t += 1

            self.cache_grad[i] += self.options["beta1"] * self.cache_grad[i] \
                                  + (1.0 - self.options["beta1"]) * individual.features['gradient'][i]
            self.cache_grad_sqr[i] += self.options["beta2"] * self.cache_grad_sqr[i] \
                                      + (1.0 - self.options["beta2"]) * individual.features['gradient'][i] ** 2

            # calculates the bias-corrected estimates
            m_corrected = self.cache_grad[i] / (1.0 - self.options["beta1"] ** self.adam_t)
            v_corrected = self.cache_grad_sqr[i] / (1.0 - self.options["beta2"] ** self.adam_t)

            x.append(individual.vector[i] - self.options["step"] * m_corrected / (math.sqrt(v_corrected + 1e-8)))

        return x

    def run(self):
        # optimization
        t_s = time.time()
        self.problem.logger.info("GradientDescent")

        # cache
        self.adam_t = 0
        self.cache_grad = [0] * len(self.problem.parameters)
        self.cache_grad_sqr = [0] * len(self.problem.parameters)

        # generate initial point
        individuals = self.generator.generate()

        # append to problem
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        self.evaluate(individuals)

        for j in range(self.options["n_iterations"]):
            new_individuals = []
            for individual in individuals:
                # get new position
                if self.options["algorithm"] == "fixed":
                    x = self.step_fixed(individual)
                elif self.options["algorithm"] == "adaptive":
                    x = self.step_adaptive(individual)
                elif self.options["algorithm"] == "adagrad":
                    x = self.step_adagrad(individual)
                elif self.options["algorithm"] == "rmsprop":
                    x = self.step_rmsprop(individual)
                elif self.options["algorithm"] == "adam":
                    x = self.step_adam(individual)
                else:
                    raise "Algorithm '{}' is defined.".format(self.options["algorithm"])

                # create a new individual
                individual = Individual(x, self.individual_features)
                individual.population_id = j + 1
                new_individuals.append(individual)

                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            self.evaluate(new_individuals)
            individuals = new_individuals

        t = time.time() - t_s
        self.problem.logger.info("GradientDescent: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()
