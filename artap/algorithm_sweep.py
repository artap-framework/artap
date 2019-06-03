from .algorithm import Algorithm
from .job import JobSimple, JobQueue
from .operators import RandomGeneration
import time


class SweepAlgorithm(Algorithm):
    """
    Sweep Analysis
    """

    def __init__(self, problem, generator=None, name='SweepAlgorithm'):
        super().__init__(problem, name)

        if generator is None:
            # set random generator
            self.generator = RandomGeneration(self.problem.parameters)
            self.generator.init(10)
        else:
            self.generator = generator

        self.job = JobSimple(self.problem)

    def run(self):
        t_s = time.time()
        self.problem.logger.info(
            "Sweep: {}: {} individuals".format(self.generator.__class__.__name__, self.population_size))

        # create initial population and evaluate individuals
        population = self.gen_initial_population()
        if self.problem.options['save_level'] == 'population':
            self.problem.data_store.write_population(population)

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))
