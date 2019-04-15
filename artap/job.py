from abc import ABCMeta, abstractmethod
from .utils import VectorAndNumbers
from .individual import Individual
from .population import Population
from copy import deepcopy
from multiprocessing import Queue, Process, Manager
import os, time


class Job(metaclass=ABCMeta):
    def __init__(self, problem, population):
        self.problem = problem
        self.population = population

    @abstractmethod
    def evaluate(self, x):
        pass

    def evaluate_scalar(self, x):
        costs = self.evaluate(x)
        return costs[0]


class JobSimple(Job):
    def __init__(self, problem, population=Population()):
        super().__init__(problem, population)

    def evaluate(self, x):
        individual = Individual(x)

        # check the constraints
        constraints = self.problem.evaluate_constraints(individual.vector)

        if constraints:
            individual.feasible = sum(map(abs, constraints))

        # problem cost function evaluate only in that case when the problem is fits the constraints
        t_out = self.problem.options['max_running_time']
        if t_out is None or not isinstance(t_out, float):
            individual.costs = self.problem.surrogate.evaluate(individual.vector)
        else:
            interval = max(t_out / 100, 1)

            manager = Manager()
            ret_value = manager.dict()
            work_p = Process(target=self.problem.surrogate.evaluate, args=(individual.vector, ))
            start = time.time()
            work_p.start()

            while time.time()-start<t_out:
                if work_p.is_alive():
                    time.sleep(interval)
                else:
                    # if the process is ready, break
                    work_p.join()
                    individual.costs = ret_value.values()
                    break
            else:
                print('Ciao!')
                work_p.terminate()
                individual.feasible = float('inf')
                work_p.join()

        # add to population
        self.population.individuals.append(individual)
        # write to datastore
        if self.problem.options["save_level"] == "individual":
            self.problem.data_store.write_individual(individual)

        individual.is_evaluated = True

        return individual.costs


class JobQueue(Job):
    def __init__(self, problem, shared_list, queue: Queue, population=Population()):
        super().__init__(problem, population)

        self.shared_list = shared_list
        self.queue = queue

    def evaluate(self, x):
        global individual
        if self.shared_list is not None:
            for item in self.shared_list:
                if item[0] == os.getpid():
                    individual = deepcopy(item[1])
        else:
            individual = Individual(x)
        while not individual.is_evaluated:
            # check the constraints
            constraints = self.problem.evaluate_constraints(individual.vector)

            if constraints:
                individual.feasible = sum(map(abs, constraints))

            # problem cost function evaluate only in that case when the problem is fits the constraints
            try:
                individual.costs = self.problem.surrogate.evaluate(individual.vector)
            except TimeoutError:
                individual.vector = VectorAndNumbers.gen_vector(self.problem.parameters)
                continue

            individual.is_evaluated = True

        if self.queue is not None:
            self.queue.put(individual)

        # add to population
        self.population.individuals.append(individual)
        #  write to datastore - not working parallel
        #  self.problem.data_store.write_individual(individual)

        return individual.costs
