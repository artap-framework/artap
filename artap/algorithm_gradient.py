from .algorithm_genetic import GeneticAlgorithm
from .operators import GradientEvaluator
from .operators import RandomGenerator
import time


class GradientAlgorithm(GeneticAlgorithm):
    """
    Gradients calculation
    """

    def __init__(self, problem, name='GradientAlgorithm'):
        super().__init__(problem, name)
        self.evaluator = GradientEvaluator(self)
        self.generator = RandomGenerator(problem.parameters)

    def run(self):
        self.generator.init(self.options['max_population_size'])
        t_s = time.time()

        # create initial population
        individuals = self.generator.generate()

        # append to problem
        for individual in individuals:
            self.problem.individuals.append(individual)

        # evaluate individuals
        self.evaluate(individuals)

        t = time.time() - t_s
        self.problem.logger.info("Gradient: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()

