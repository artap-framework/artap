from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .job import Job
from .operators import GradientGeneration
from .population import Population
import time


class SweepAlgorithm(GeneralEvolutionaryAlgorithm):
    """
    Sweep Analysis
    """

    def __init__(self, problem, generator, name='SweepAlgorithm'):
        super().__init__(problem, name)

        self.generator = generator

    def run(self):
        t_s = time.time()
        # self.problem.logger.info("Sweep: {}: {} individuals".format(self.generator.__class__.__name__, self.population_size))

        # create initial population and evaluate individuals
        population = self.gen_initial_population()

        if self.options['calculate_gradients'] is True:
            # TODO: Move to Algorithm class here only call calculate_gradients(individuals)
            gradient_generator = GradientGeneration(self.problem.parameters)
            gradient_generator.init(population.individuals)
            gradient_population = Population(gradient_generator.generate())
            gradient_population.individuals = self.evaluate(gradient_population.individuals)
            population.individuals = self.evaluate_gradient(population.individuals, gradient_population.individuals)

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))
