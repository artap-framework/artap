from string import Template
from abc import ABC, abstractmethod
from .individual import Individual, Individual_NSGA_II

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc


class Population:
    
    size = 0
    number = 0

    def __init__(self, problem, individuals = []):
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
            individual.problem.datastore.write_individual(individual.to_list())

    def print(self):
        print(self.toString())
      
    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual.gen_individuals(population_size, self.problem, self.number)
        return self.individuals
                       
    def evaluate(self):    
        for individual in self.individuals:
            if individual.is_evaluated == False:
                individual.evaluate()    

    
class Population_NSGA_II(Population):

    def __init__(self, problem, individuals = []):
            return super().__init__(problem, individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual_NSGA_II.gen_individuals(population_size, self.problem, self.number)