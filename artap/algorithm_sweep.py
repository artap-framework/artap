from .algorithm import Algorithm
from .job import JobSimple
from .operators import GradientGeneration
from .population import Population
import time


class SweepAlgorithm(Algorithm):
    """
    Sweep Analysis
    """

    def __init__(self, problem, generator=None, name='SweepAlgorithm'):
        super().__init__(problem, name)

        if generator is not None:
            self.generator = generator

        self.job = JobSimple(self.problem)

    def run(self):
        t_s = time.time()
        self.problem.logger.info(
            "Sweep: {}: {} individuals".format(self.generator.__class__.__name__, self.population_size))

        # create initial population and evaluate individuals
        population = self.gen_initial_population()

        if self.options['calculate_gradients'] is True:
            # TODO: Move to Algorithm class here only call calculate_gradients(individuals)
            gradient_generator = GradientGeneration(self.problem.parameters)
            gradient_generator.init(population.individuals)
            gradient_population = Population(gradient_generator.generate())
            gradient_population.individuals = self.evaluate(gradient_population.individuals)
            population.individuals = self.evaluate_gradient(population.individuals, gradient_population.individuals)

        # write population
        self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))
