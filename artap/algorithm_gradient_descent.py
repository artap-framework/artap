from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from .operators import GradientEvaluator, RandomGenerator
from .individual import Individual
import time


class GradientDescent(GeneticAlgorithm):
    """ Gradient descent algorithms """

    def __init__(self, problem: Problem, generator=None, name="GradientDescent"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='n_iterations', default=10,
                             desc='Maximum number of iterations')
        self.options.declare(name='h', default=0.1,
                             desc='step')

        # compute gradients
        self.evaluator = GradientEvaluator(self)
        self.individual_features['gradient'] = dict()

        # set default generator
        if generator is None:
            self.generator = RandomGenerator(self.problem.parameters, self.individual_features)
            self.generator.init(1)
        else:
            self.generator = generator

    def run(self):
        # optimization
        t_s = time.time()
        self.problem.logger.info("GradientDescent")

        h_initial = self.options["h"]

        # generate initial point
        individuals = self.generator.generate()

        # append to problem
        for individual in individuals:
            # append to problem
            self.problem.individuals.append(individual)
            # add to population
            individual.population_id = 0

        self.evaluate(individuals)

        # TODO: add adaptive step size
        for j in range(self.options["n_iterations"]):
            new_individuals = []
            for individual in individuals:
                x = []
                for i in range(len(individual.vector)):
                    x.append(individual.vector[i] - h_initial * individual.features['gradient'][i])
                individual = Individual(x, self.individual_features)
                individual.population_id = j+1
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
