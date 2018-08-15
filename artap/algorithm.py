from .problem import Problem 
from .population import Population, Population_NSGA_II 
from .individual import Individual_NSGA_II, Individual

import numpy as np
from abc import ABCMeta,abstractmethod
import random
from numpy import mean, std

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
        population = Population(self.problem)
        population.gen_random_population(self.population_size, self.vector_length, self.problem.parameters)
        population.evaluate()
        population.save()
        
        self.problem.add_population(population)        
        
        self.current_population += 1 
        return population
    
    def select(self):
        population = self.problem.populations[-1]        


    def form_new_population(self):
        population = gen_population(self.population_size, self.vector_length, self.problem.parameters)
        self.problem.add_population(population)
        self.problem.evaluate_population(self.current_population)        
        self.current_population += 1 

    def run(self):
        pass


class NSGA_II(GeneticAlgorithm):

    def __init__(self, problem :Problem, name = "NSGAII Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.prob_cross = 0.6
        self.prob_mutation = 0.05
    
    def gen_initial_population(self):        
        population = Population_NSGA_II(self.problem)
        population.gen_random_population(self.population_size, self.vector_length, self.problem.parameters)
        population.evaluate()
        population.save()
        self.problem.populations.append(population)
    
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

    def fast_non_dominated_sort(self, population):
        pareto_front = []
        front_number = 1
        #population = self.problem.populations[-1]        
        for p in population:
            for q in population:
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
        #individuals = population.individuals.copy()
        individuals = population

        for i in range(0,len(individuals)-1):
            for j in range(i+1,len(individuals)):
                if individuals[i].vector[dim] < individuals[j].vector[dim]:
                    temp = individuals[i]
                    individuals[i] = individuals[j]
                    individuals[j] = temp
                    
        return individuals
    
    def calculate_crowd_dis(self, population):
        infinite = float("inf")
            
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
                
        for p in population:
            p.crowding_distance = p.crowding_distance / len(self.problem.parameters)
            
    
    def tournment_select(self, parents, part_num=2): # binary tournment selection
        
        participants = random.sample(parents, part_num)
        best = participants[0]
        best_rank = participants[0].front_number
        best_crowding_distance = participants[0].crowding_distance
        
        for p in participants[1:] :
            if p.front_number < best_rank or \
            (p.front_number == best_rank and p.crowding_distance > best_crowding_distance):
                best = p
                best_rank = p.front_number
                best_crowding_distance = p.crowding_distance
                
        return best

    def generate(self, parents):
        # generate two children from two parents
        
        children = []
        while len(children) < self.population_size:
            parent1 = self.tournment_select(parents)
            parent2 = self.tournment_select(parents)
            while parent1 == parent2 :
                parent2 = self.tournment_select(parents)
                
            child1,child2 = self.cross(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            children.append(child1)
            children.append(child2)
        return children


    def cross(self, p1, p2): # the random linear operator
        if random.uniform(0,1) >= self.prob_cross:
            return p1,p2
        
        parameter1,parameter2 = [],[]
        linear_range = 2
        alpha = random.uniform(0,linear_range)
        for j in range(0,len(p1.vector)):
            parameter1.append(alpha*p1.vector[j] +
                            (1-alpha)*p2.vector[j] )
            parameter2.append((1-alpha)*p1.vector[j] +
                            alpha*p2.vector[j] )
        c1 = Individual_NSGA_II(parameter1, self.problem )
        c2 = Individual_NSGA_II(parameter2, self.problem)
        return c1,c2


    def mutation(self, p): # uniform random mutation
        mutation_space = 0.1
        vector = []
        i = 0
        for  parameter in self.problem.parameters.items():            
            if random.uniform(0,1) < self.prob_mutation:
                para_range = mutation_space*(parameter[1]['bounds'][0] - parameter[1]['bounds'][1])
                mutation = random.uniform(-para_range,para_range)
                vector.append(p.vector[i]+mutation)
            else :
                vector.append(p.vector[i])
            i += 1

        p_new = Individual_NSGA_II(vector, self.problem)            
        return p_new


    def select(self):        
        pass        

   
    def form_new_population(self):
        pass        


    def run(self):
        self.gen_initial_population()
        self.problem.populations[self.current_population-1].plot()           
        parent_individuals = self.problem.populations[0].individuals
        individuals = parent_individuals
        costs_number = len(self.problem.costs)
        child_individuals = []

        for it in range(self.problem.max_population_number):   
                        
            individuals = parent_individuals + child_individuals
            for individual in individuals:
                individual.evaluate()
        
            self.fast_non_dominated_sort(individuals)            
            self.calculate_crowd_dis(individuals)
            
            parents = []
            front = 1

            while len(parents) < self.population_size:
                for individual in individuals:
                    if individual.front_number == front:
                        parents.append(individual)
                        if len(parents) == self.population_size:
                            break
                front = front + 1

            
            population = Population_NSGA_II(self.problem, individuals)
            population.save()
            self.problem.add_population(population)
            self.problem.populations[-1].plot()            
            self.current_population += 1

            child_individuals = self.generate(parent_individuals)         

class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name = 'Sensitivity analysis'):
            self.parameters = parameters
            super().__init__(problem, name)

    def run(self):        
        vector = []
        for parameter in self.problem.parameters.items():
            vector.append(float(parameter[1]['initial_value']))        
        
        population = None
        for parameter_name in self.parameters:
            parameter_values = []
            population = Population(self.problem)
            
            index = 0
            selected_parametr = None
            for parameter in self.problem.parameters.items():
                if parameter[0] == parameter_name:
                    selected_parametr = parameter
                    break                
                index +=1
            
            individuals = []    
            for i in range(self.problem.max_population_size):               
                value = Individual.gen_number(selected_parametr[1]['bounds'], selected_parametr[1]['precision'])
                vector[index] = value
                parameter_values.append(value)
                individual = Individual(vector.copy(), self.problem)
                individuals.append(individual)
                        
            population.individuals = individuals
            population.evaluate()     
            costs = []
            # TODO: Make also for multiobjective
            for individual in population.individuals:
                costs.append(individual.costs[0])
            
            print(parameter_values)
            print(costs)
            
            print(mean(costs))
            print(std(costs))
            print(mean(parameter_values))
            print(std(parameter_values))

            self.problem.populations.append(population)

               
               