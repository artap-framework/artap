from multiprocessing import Process

from .individual import Individual, Individual_NSGA_II


class Population:
    
    size = 0
    number = 0

    def __init__(self, problem, individuals=None):

        if individuals is None:
            individuals = []

        self.length = len(individuals)
        self.problem = problem     
        self.number = Population.number
        
        self.individuals = individuals
        for individual in self.individuals:
            individual.population_id = self.number
            individual.set_id()

        Population.number += 1

    def to_string(self):
        string = "population number: " + str(self.number) + " \n"
      
        for individual in self.individuals:
            string += individual.toString() + ", "        
        
        return string

    def save(self):
        for individual in self.individuals:            
            individual.problem.data_store.write_individual(individual.to_list())

    def print(self):
        print(self.to_string())
      
    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual.gen_individuals(population_size, self.problem, self.number)
        return self.individuals

    def evaluate(self):
        Population.evaluate_individuals(self.individuals, self.problem)

    @staticmethod
    def evaluate_individuals(individuals, problem):
        processes = []
        n = len(individuals)
        sets = int(n / 10)
        rest = int(n % 10)

        for j in range(sets+1):
            if j == sets:
                end = rest
            else:
                end = 10

            for individual in individuals[j*10:j*10+end]:
                individual.problem = problem
                p = Process(target=individual.evaluate, args=[])
                processes.append(p)
                p.start()

            for process in processes:
                process.join()

            for i in range(Individual.results.qsize()):
                result = Individual.results.get()
                for individual in individuals[j*10:j*10+end]:
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
