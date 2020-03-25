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
        # create initial population and evaluate individuals
        population = self.gen_initial_population()
        self.problem.populations.append(population)
        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))
