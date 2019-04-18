from .problem import Problem
from .utils import ConfigDictionary
from .job import JobSimple, JobQueue
from .population import Population

from multiprocessing import Process, Manager, Queue, cpu_count
from abc import ABCMeta, abstractmethod


class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.options = ConfigDictionary()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')
        self.options.declare(name='calculate_gradients', default=False,
                             desc='Enable calculating of gradients')
        # max(int(2 / 3 * cpu_count(), 1)
        self.options.declare(name='max_processes', default=1,
                             desc='Max running processes')

        # initial population size
        self.population_size = 0

    @abstractmethod
    def run(self):
        pass

    def gen_initial_population(self):
        individuals = self.generator.generate()
        # set current size
        self.population_size = len(individuals)
        # evaluate individuals
        individuals = self.evaluate(individuals)

        population = Population(individuals)
        return population

    def evaluate(self, individuals: list):
        if self.options["max_processes"] > 1:
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

            if ((i % self.options['max_processes']) == 0) or (j >= len(individuals)):
                for process in processes:
                    process.join()
                    processes = []

        # collect the results
        individuals = []
        for item in range(queue.qsize()):
            individuals.append(queue.get())
            # write to datastore
            if self.problem.options["save_level"] == "individual":
                self.problem.data_store.write_individual(individuals[-1])
        queue.close()
        queue.join_thread()

        return individuals

    def evaluate_gradient(self, individuals: list):
        i = 0
        n = len(self.problem.parameters)
        gradients = []
        gradient = []
        for individual in individuals:
            i += 1
            gradient.append(individual.costs.copy())
            if i == n:
                i = 0
                gradients.append(gradient.copy())
                gradient.clear()


class DummyAlgorithm(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, name='DummyAlgorithm'):
        super().__init__(problem, name)

    def run(self):
        pass
