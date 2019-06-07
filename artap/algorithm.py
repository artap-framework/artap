from .problem import Problem
from .utils import ConfigDictionary
from .job import JobSimple, JobQueue
from .population import Population

from multiprocessing import Process, Manager, Queue, cpu_count
from abc import ABCMeta, abstractmethod
import copy
import numpy as np


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
        new_individuals = []
        processes = []
        i = 0
        n = len(individuals)
        while i < n:
            j = 0
            shared_list = manager.list([])
            queue = Queue()
            job = JobQueue(self.problem, shared_list, queue)
            while (j < self.options["max_processes"]) and ((i + j) < n):
                individual = individuals[i + j]
                if not individual.is_evaluated:
                    p = Process(target=job.evaluate, args=(individual.vector,))
                    processes.append(p)
                    p.start()
                    shared_list.append([p.pid, individual])
                    j += 1

            for process in processes:
                process.join()

            processes = []
            i += j

            for item in range(queue.qsize()):
                new_individuals.append(copy.deepcopy(queue.get()))
                # write to datastore
                if self.problem.options["save_level"] == "individual":
                    self.problem.data_store.write_individual(new_individuals[-1])
            queue.close()
            queue.join_thread()
        return new_individuals

    def evaluate_gradient(self, individuals: list, gradient_individuals: list):
        # Todo: Make operator Gradient consisting of current gradient generator and evaluate_gradient
        # individuals.sort(key=lambda x: abs(x.depends_on))
        n_params = len(individuals[0].vector)
        for j in range(len(individuals)):
            table = []
            for i in range(len(gradient_individuals)):
                individual = gradient_individuals[i]
                if individual.depends_on == j:
                    table.append(individual)

            gradient = np.zeros(n_params)
            for k in range(len(table)):
                index = table[k].modified_param
                gradient[index] = ((individuals[j].costs[0] - table[k].costs[0]) / 1e-6)

            individuals[j].gradient = gradient

        return individuals


class DummyAlgorithm(Algorithm):
    """
    Dummy class for testing
    """

    def __init__(self, problem, name='DummyAlgorithm'):
        super().__init__(problem, name)

    def run(self):
        pass
