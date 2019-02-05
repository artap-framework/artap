from .problem import Problem
from .population import Population
from .utils import ConfigDictionary
from .job import JobSimple, JobQueue

from multiprocessing import Process, Manager, Queue
from abc import ABCMeta, abstractmethod


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.options = ConfigDictionary()

        # current population
        self.population = Population()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')
        self.options.declare(name='calculate_gradients', default=False,
                             desc='Enable calculating of gradients')
        self.options.declare(name='max_population_size', default=1,
                             desc='Maximal number of individuals in population')

    @abstractmethod
    def run(self):
        pass

    def evaluate(self, individuals: list):
        if self.problem.options["max_processes"] > 1:
            individuals = self.evaluate_parallel(individuals)
        else:
            individuals = self.evaluate_serial(individuals)

        return individuals

    def evaluate_serial(self, individuals: list):
        job = JobSimple(self.problem)
        for individual in individuals:
            if not individual.is_evaluated:
                individual.costs = job.evaluate(individual.vector)
                individual.is_evaluated = True

        # collect the results
        return individuals

    def evaluate_parallel(self, individuals: list):
        manager = Manager()
        shared_list = manager.list([])
        queue = Queue()
        job = JobQueue(self.problem, shared_list, queue)
        processes = []

        i = 0
        j = 0
        for individual in individuals:
            if not individual.is_evaluated:
                p = Process(target=job.evaluate, args=(individual.vector,))
                processes.append(p)
                p.start()
                shared_list.append([p.pid, individual])
                i += 1
                j += 1

            if ((i % self.problem.options['max_processes']) == 0) or (j >= len(individuals)):
                for process in processes:
                    process.join()
                    processes = []

        # collect the results
        individuals = []
        for item in range(queue.qsize()):
            individuals.append(queue.get())
        queue.close()
        queue.join_thread()

        return individuals


class EvalAll(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, individuals: list, name='Sensitivity analysis'):
        self.individuals = individuals
        super().__init__(problem, name)

    def run(self):
        pass

    # def evaluate_gradient(self):
    #     self.gradient = self.problem.evaluate_gradient(self)
    #     if self.problem.options['max_processes'] > 1:
    #         if Individual.gradients is not None:
    #             Individual.gradients.put([self.number, self.gradient])
    #
    #     return self.gradient

    # def evaluate(self, x, population: Population):
    #     if population is None:
    #         population = Population()
    #     individual = Individual(x, self, population)
    #
    #     # check the constraints
    #     constraints = self.problem.evaluate_constraints(individual.vector)
    #
    #     if constraints:
    #         individual.feasible = sum(map(abs, constraints))
    #
    #     # problem cost function evaluate only in that case when the problem is fits the constraints
    #
    #     # TODO: find better solution for surrogate
    #     if self.problem.surrogate:
    #         costs = self.problem.evaluate_surrogate(individual.vector)
    #     else:
    #         # increase counter
    #         self.problem.eval_counter += 1
    #         # eval
    #         costs = self.problem.evaluate(individual.vector)
    #
    #     individual.costs = costs
    #
    #     # scipy uses the result number, the genetic algorithms using the property value
    #
    #     individual.is_evaluated = True
    #     if self.problem.options['save_level'] == "individual" and self.problem.working_dir:
    #         self.problem.data_store.write_individual(individual.to_list())
    #
    #     if self.problem.options['max_processes'] > 1:
    #         if self.queue is not None:
    #             self.queue.put([individual.id, costs, individual.feasible])
    #
    #     population.individuals.append(individual)
    #     self.problem.populations.append(population)
    #     return costs

    # def evaluate_gradient(self):
    #     self.gradient = self.problem.evaluate_gradient(self)
    #     if self.problem.options['max_processes'] > 1:
    #         if Individual.gradients is not None:
    #             Individual.gradients.put([self.number, self.gradient])
    #
    #     return self.gradient
