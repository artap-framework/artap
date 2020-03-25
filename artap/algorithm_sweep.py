from .algorithm_genetic import GeneralEvolutionaryAlgorithm
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

        # create initial population and evaluate individuals
        population = self.gen_initial_population()

        t = time.time() - t_s
        self.problem.logger.info("Sweep: elapsed time: {} s".format(t))
