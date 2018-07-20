from .problem import Problem
from .utils import *

import numpy as np

from abc import ABCMeta,abstractmethod

class Algorithm(metaclass=ABCMeta):
    """ Base class for optimizaion algorithms. """

    def __init__(self, problem: Problem, name = "Algorithm"):
        self.name = name
        self.problem = problem

    @abstractmethod
    def run(self):
        pass
    
class GeneralEvolutionalAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem :Problem, name = "General Evolutionary Algorithm"):
        super().__init__(problem, name)            
        self.problem = problem        
    
    def gen_initial_population(self):
        pass

    def select(self):
        pass
    
    def form_new_population(self):
        pass


    def run(self):
        pass
        
    
class GeneticAlgorithm(GeneralEvolutionalAlgorithm):

    def __init__(self, problem :Problem, name = "General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.population_size = self.problem.max_population_size
        self.vector_length = len(self.problem.parameters)
        self.populations_number = self.problem.max_population_number 
        self.current_population = 0                       

    def gen_initial_population(self):        
        population = gen_population(self.population_size, self.vector_length, self.problem.parameters)
        self.problem.add_population(population)        
        self.problem.evaluate_population(self.current_population)
        self.current_population += 1 
    
    def select(self):
        population = self.problem.populations[-1]
        # population.print()

    def form_new_population(self):
        population = gen_population(self.population_size, self.vector_length, self.problem.parameters)
        self.problem.add_population(population)
        self.problem.evaluate_population(self.current_population)
        self.current_population += 1 


    def run(self):
        self.gen_initial_population()
        for i in range(self.populations_number):
            self.select()
            self.form_new_population()
