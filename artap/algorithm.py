from .problem import Problem
from .utils import *

import numpy as np
from abc import ABCMeta,abstractmethod
import random

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


class NSGA_II(GeneticAlgorithm):

    def __init__(self, problem :Problem, name = "NSGAII Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.prob_cross = 0.6
        self.prob_mutation = 0.05

    def gen_initial_population(self):        
        super().gen_initial_population()        
        for individual in self.problem.populations[0].individuals:
            individual.dominate = set()
            individual.domination_counter = 0
            individual.front_number = 0
            individual.crowding_distance = 0
   
    def is_dominate(self, p, q):
        dominate = False        
        for i in range(0, len(self.problem.costs)):
            if p.costs[i] > q.costs[i] :
                return False
            if p.costs[i] < q.costs[i] :
                dominate = True
                
        # TODO: Constrains
        #for i in range(0,len(p.violation)):
        #    if p.violation[i] > q.violation[i] :
        #        return False
        #    if p.violation[i] < q.violation[i] :
        #        dominate = True
                
        return dominate


    def crossover(self):
        pass

    def mutate(self):
        pass

    def fast_non_dominated_sort(self):
        pareto_front = []
        front_number = 1
        population = self.problem.populations[-1]        
        for p in population.individuals:
            for q in population.individuals:
                if p is q :
                    continue
                if self.is_dominate(p, q):
                    p.dominate.add(q)
                elif self.is_dominate(q, p):
                    p.domination_counter = p.domination_counter + 1

            if p.domination_counter == 0 :
                p.front_number = front_number
                pareto_front.append(p)

        while not len(pareto_front)==0:
            front_number += 1
            temp_set = []
            for p in pareto_front:
                for q in p.dominate:
                    q.domination_counter -= 1
                    if q.domination_counter==0 and q.front_number==0 :
                        q.front_number = front_number
                        temp_set.append(q)
            pareto_front = temp_set
        
    # TODO: faster algorithm
    def sort_by_coordinate(self, population, dim): 
        individuals = population.individuals.copy()


        for i in range(0,len(individuals)-1):
            for j in range(i+1,len(individuals)):
                if individuals[i].vector[dim] < individuals[j].vector[dim]:
                    temp = individuals[i]
                    individuals[i] = individuals[j]
                    individuals[j] = temp
                    
        return individuals
    
    def calculate_crowd_dis(self, population):
        infinite = 100000.0 # TODO: Is it OK? Number instead of float("inf")
            
        for dim in range(0, len(self.problem.parameters)):
            new_list = self.sort_by_coordinate(population,dim)
            
            new_list[0].crowding_distance += infinite
            new_list[-1].crowding_distance += infinite
            max_distance = new_list[0].vector[dim] - new_list[-1].vector[dim]
            for i in range(1,len(new_list)-1):
                distance = new_list[i-1].vector[dim] - new_list[i+1].vector[dim]
                if max_distance == 0 :
                    new_list[i].crowding_distance = 0
                else :
                    new_list[i].crowding_distance += distance/max_distance
                
        for p in population.individuals :
            p.crowding_distance = p.crowding_distance / len(self.problem.parameters)
            
    
    def tournment_select(self, parents, part_num=2): # binary tournment selection
        
        participants = random.sample(parents, part_num)
        best = participants[0]
        best_rank = participants[0].front_number
        best_crowding_distance = participants[0].crowding_distance
        
        for p in participants[1:] :
            if p.front_rank < best_rank or \
            (p.front_rank == best_rank and p.crowding_distance > best_crowding_distance):
                best = p
                best_rank = p.front_rank
                best_crowding_distance = p.crowding_distance
                
        return best

    def generate(self, parents):
        # generate two children from two parents
        
        children = set()
        while len(children) < self.p_size:
            parent1 = self.tournment_select(parents)
            parent2 = self.tournment_select(parents)
            while parent1 == parent2 :
                parent2 = self.tournment_select(parents)
                
            child1,child2 = self.cross(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            children.add(child1)
            children.add(child2)
        return children


    def cross(self, p1, p2): # the random linear operator
        if random.uniform(0,1) >= self.prob_cross:
            return p1,p2
        
        parameter1,parameter2 = [],[]
        linear_range = 2
        alpha = random.uniform(0,linear_range)
        for j in range(0,len(p1.parameter)):
            parameter1.append(alpha*p1.parameter[j] +
                            (1-alpha)*p2.parameter[j] )
            parameter2.append((1-alpha)*p1.parameter[j] +
                            alpha*p2.parameter[j] )
        c1 = NSGA2Individual(parameter1)
        c2 = NSGA2Individual(parameter2)
        return c1,c2


    def mutation(self, p): # uniform random mutation
        mutation_space = 0.1
        parameter = []
        for i in range(0,len(p.parameter)):
            if random.uniform(0,1) < self.prob_mutation:
                para_range = mutation_space*(self.parameter_upper_bound[i]-self.parameter_lower_bound[i])
                mutation = random.uniform(-para_range,para_range)
                parameter.append(p.parameter[i]+mutation)
            else :
                parameter.append(p.parameter[i])

        p_new = NSGA2Individual(parameter)            
        return p_new


    def select(self):        
        self.fast_non_dominated_sort()
        self.calculate_crowd_dis(self.problem.populations[-1])
        self.problem.populations[-1].plot()
        

   
    def form_new_population(self):
        population = gen_population(self.population_size, self.vector_length, self.problem.parameters)
        self.problem.add_population(population)
        for individual in self.problem.populations[-1].individuals:
            individual.dominate = set()
            individual.domination_counter = 0
            individual.front_number = 0
            individual.crowding_distance = 0

        self.problem.evaluate_population(self.current_population)
        self.current_population += 1 
        
