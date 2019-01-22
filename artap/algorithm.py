from .problem import Problem
from .population import Population
from .individual import Individual
from .utils import ConfigDictionary
from .job import Job

from multiprocessing import Process, Manager, Queue
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

    @abstractmethod
    def run(self):
        pass

    def evaluate(self, individuals: list, population_id: int = None):
        if self.problem.options["max_processes"] > 1:
            individuals = self.evaluate_parallel(individuals, population_id)
        else:
            individuals = self.evaluate_serial(individuals, population_id)

        return individuals

    def evaluate_serial(self, individuals: list, population_id: int = None):
        job = Job(self.problem)
        for individual in individuals:
            if not individual.is_evaluated:
                individual.costs = job.evaluate(individual.vector, population_id)
        return individuals

    def evaluate_parallel(self, individuals: list, population_id: int):
        manager = Manager()
        shared_list = manager.list([])
        queue = Queue()
        job = Job(self.problem, shared_list, queue)
        processes = []

        i = 0
        j = 0
        for individual in individuals:
            if not individual.is_evaluated:
                p = Process(target=job.evaluate, args=(individual.vector, population_id))
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


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

    def run(self):
        parameters = []
        for parameter in self.problem.parameters.items():
            parameters.append(float(parameter[1]['initial_value']))

        for parameter_name in self.parameters:
            parameter_values = []
            population = Population(self.problem)

            index = 0
            selected_parameter = None
            for parameter in self.problem.parameters.items():
                if parameter[0] == parameter_name:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.problem.options['max_population_size']):
                value = Individual.gen_number(selected_parameter[1]['bounds'], selected_parameter[1]['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy(), self.problem)
                individuals.append(individual)

            population.individuals = individuals
            population.evaluate()
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

            self.problem.populations.append(population)


class EvalAll(Algorithm):

    def __init__(self, problem, individuals: list, name='Sensitivity analysis'):
        self.individuals = individuals
        super().__init__(problem, name)

    def run(self):
        self.evaluate_serial(self.individuals)
