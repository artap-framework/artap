from multiprocessing import Process, Queue
from .individual import Individual, Individual_NSGA_II
import time


class Population:
    
    size = 0
    number = 0

    def __init__(self, problem, individuals=None):

        if individuals is None:
            individuals = []

        self.length = len(individuals)
        self.problem = problem     
        self.number = Population.number
        
        self.individuals = individuals.copy()
        for individual in self.individuals:
            individual.population_id = self.number
            individual.set_id()

        Population.number += 1

    def __repr__(self):

        string = "population number: " + str(self.number) + " \n"

        for individual in self.individuals:
            string += individual.to_string() + ", "

        return string

    def extend(self, new_individuals):
        self.individuals.append(new_individuals)
        self.length = len(new_individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual.gen_individuals(population_size, self.problem, self.number)
        return self.individuals

    def gen_population_from_table(self, table):
        for parameters in table:
            individual = Individual_NSGA_II(parameters, self.problem, self.number)
            self.individuals.append(individual)

    def gen_uniform_population(self, values_per_range):
        j = 0
        for parameter in self.problem.parameters.items():
            inc = (parameter[1]['bounds'][1] - parameter[1]['bounds'][0]) / values_per_range
            parameters = self.problem.get_initial_values()
            parameters[j] = parameter[1]['bounds'][0]
            for i in range(values_per_range):
                parameters[j] += i * inc
                individual = Individual_NSGA_II(parameters.copy(), self.problem, self.number)
                self.individuals.append(individual)
            j += 1

    def evaluate(self):
        """
        The evaluate function calculate the value of the
        :return:
        """
        Individual.results = Queue()
        processes = []

        if self.problem.max_processes == 1:
            for individual in self.individuals:
                if not individual.is_evaluated:
                    individual.problem = self.problem
                    individual.evaluate()


        else:
            i = 0
            j = 0
            for individual in self.individuals:
                if not individual.is_evaluated:
                    individual.problem = self.problem
                    p = Process(target=individual.evaluate)
                    processes.append(p)
                    p.start()
                    i += 1
                    j += 1

                if ((i % self.problem.max_processes) == 0) or (j >= len(self.individuals)):
                    for process in processes:
                        process.join()
                        processes = []

            # collect the results
            for i in range(Individual.results.qsize()):
                result = Individual.results.get()
                for individual in self.individuals:
                    if individual.number == result[0]:
                        if type(result[1]) != list:
                            individual.costs.append(result[1])
                        else:
                            individual.costs.extend(result[1])
                        individual.feasible = result[2]
                        individual.is_solved = True

            Individual.results.close()
            Individual.results.join_thread()



class Population_NSGA_II(Population):

    def __init__(self, problem, individuals=None):
            if individuals is None:
                individuals = []
            super().__init__(problem, individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual_NSGA_II.gen_individuals(population_size, self.problem, self.number)
