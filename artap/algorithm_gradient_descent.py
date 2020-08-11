from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from .operators import GradientEvaluator, RandomGenerator
from .individual import Individual


class GradientDescent(GeneticAlgorithm):
    """ Gradient descent algorithms """

    def __init__(self, problem: Problem, name="GradientDescent"):
        super().__init__(problem, name)
        self.problem = problem

        self.evaluator = GradientEvaluator(self)
        self.options.declare(name='n_iterations', default=10,
                             desc='Maximum number of iterations')
        self.options.declare(name='x0', default=0,
                             desc='initial point')
        self.options.declare(name='h', default=0.1,
                             desc='step')

        self.individual_features['gradient'] = dict()
        self.generator = RandomGenerator(self.problem.parameters, self.individual_features)

    def run(self):
        h = self.options["h"]
        self.generator.init(self.options['max_population_size'])

        # generate
        individuals = self.generator.generate()

        # append to problem
        for individual in individuals:
            self.problem.individuals.append(individual)

        self.evaluate(individuals)

        # TODO: add adaptive step size
        for it in range(self.options['max_population_number']):
            for individual in individuals:
                x = []
                for i in range(len(individual.vector)):
                    x.append(individual.vector[i] - h * individual.features['gradient'][i])
                individual = Individual(x, self.individual_features)
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

            self.evaluate(individuals)


