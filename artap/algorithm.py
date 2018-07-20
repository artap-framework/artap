from .problem import Problem
from .utils import *

from scipy.optimize import minimize
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


class ScipyNelderMead(Algorithm):
    """ Class is prepared for usage of Nelder-Mead method from package SciPy."""

    def __init__(self, problem: Problem, name = "Nelder-Mead"):
        super().__init__(problem, name)
        
        self.method = "nelder-mead"
        self.number_of_objectives = len(self.problem.costs)
        self.rel_tol = 1e-8

    def run(self):    
        initial_vector = self.problem.parameters_values
        # TODO: parameters (tol=1e-3)
        
        x0 = np.array(initial_vector)        
        minimize(self.problem.evaluate_individual, x0, method="nelder-mead")

        
    
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
        # pareto_front = []
        # parameter = []
        # pareto_parameters = []
        # i = 0
        # j = 0
        
        # for selected_individual in population:        
        #     is_pareto = True

        #     for individual in population:
        #         if (selected_individual.costs[0] > individual.costs[0]) and \
        #             (selected_individual.costs[1] < individual.costs[1]):

        #             is_pareto = False

        #         if (selected_individual.costs[0] > individual.costs[0]) \
        #             and (selected_individual.costs[1] < individual.costs[1]):

        #             is_pareto = False

        #     if is_pareto:
        #         pareto_front.append(selected_individual.costs)
        #         pareto_parameters.append(selected_individual.parameters])
        #         print(selected_individual.parameters])
        #         j = j + 1

        #     i = i + 1



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
