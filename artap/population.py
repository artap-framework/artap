from multiprocessing import Process
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

    def to_string(self):
        string = "population number: " + str(self.number) + " \n"
      
        for individual in self.individuals:
            string += individual.to_string() + ", "
        
        return string

    def print(self):
        print(self.to_string())
      
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
        Population.evaluate_individuals(self.individuals, self.problem)

    @staticmethod
    def evaluate_individuals(individuals, problem):
        processes = []
        i = 0
        time.sleep(1)
        for individual in individuals:
            i += 1
            if i % 10 == 0:
                time.sleep(1)
            if not individual.is_evaluated:
                individual.problem = problem
                p = Process(target=individual.evaluate, args=[])
                processes.append(p)
                p.start()

        for process in processes:
            process.join()

        for i in range(Individual.results.qsize()):
            result = Individual.results.get()
            for individual in individuals:
                if individual.number == result[0]:
                    individual.costs = result[1]
                    individual.is_solved = True


class Population_NSGA_II(Population):

    def __init__(self, problem, individuals=None):
            if individuals is None:
                individuals = []
            super().__init__(problem, individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual_NSGA_II.gen_individuals(population_size, self.problem, self.number)
