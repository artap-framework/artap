from .problem import Problem
from .algorithm_genetic import GeneticAlgorithm
from .operators import GradientEvaluator, RandomGenerator
from .population import Population
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

    def run(self):
        h = self.options["h"]

        self.generator = RandomGenerator(self.problem.parameters)
        self.generator.init(self.options['max_population_size'])
        self.gen_initial_population()

        # TODO: add adaptive step size
        for it in range(self.options['max_population_number']):
            population = Population()
            for individual in self.problem.populations[it].individuals:
                x = []
                for i in range(len(individual.vector)):
                    x.append(individual.vector[i] - h * individual.features['gradient'][i])
                individual = Individual(x)
                population.individuals.append(individual)
            self.evaluate(population.individuals)
            self.problem.populations.append(population)

