import sqlite3
from string import Template
from .datastore import DataStore
from random import random
from numpy.random import normal
from abc import *

class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """   
    number = 0    
    
    def __init__(self, x, problem, population_id = 0):        
        self.vector = x
        self.problem = problem
        self.length = len(self.vector)
        self.costs = []                
        
        self.number = Individual.number
        Individual.number += 1    
        
        self.population_id = population_id
        self.is_evaluated = False

    def toString(self):
        string = "["
        for number in self.vector:
            string += str(number) + ", "
        string = string[:len(string)-1]
        string += "]"
        string += "; costs:["
        for number in self.costs:
            string += str(number) + ", "        
        string += "]\n"
        return string

    
    def toDatabase(self):  
        id = self.number        
        cmd_exec_tmp = Template("INSERT INTO $table (id, population_id, ")  # TODO: rewrite using string templates
        cmd_exec = cmd_exec_tmp.substitute(table = "data")        
        
        if type(self.costs) != list:
            costs = [self.costs]
        else:
            costs = self.costs
        
        for parameter_name in self.problem.parameters.keys():
            cmd_exec += parameter_name + ","
        
        for cost_name in self.problem.costs.keys():
            cmd_exec += cost_name + ","

        cmd_exec = cmd_exec[:-1]  # delete last comma
        cmd_exec += ") VALUES (?, ?, "

        for i in range(len(self.vector) + len(costs) - 1):
            cmd_exec += " ?,"
        cmd_exec += " ?);"           
               
        params = [id, self.population_id]
        
        for i in range(len(self.vector)):
            params.append(self.vector[i])
        
        for cost in self.costs:
            params.append(cost)

        self.problem.datastore.write_individual(cmd_exec, params)    
                
    def evaluate(self):        
        # problem cost function evaluate     
        costs = self.problem.eval(self.vector)            

        if type(costs) != list:
            self.costs = [costs]
        else:
            self.costs = costs
        
        self.is_evaluated = True        
        return costs


    def set_id(self):
        self.number = Individual.number
        Individual.number += 1
    
    @classmethod
    def gen_individuals(cls, number, problem, population_id):
        individuals = []            
        for i in range(number):
            individuals.append(cls.gen_individual(problem, population_id))
        return individuals

    @classmethod
    def gen_individual(cls, problem, population_id = 0):
        vector = cls.gen_vector(cls, len(problem.parameters), problem.parameters)
        return cls(vector, problem)

    @staticmethod
    def gen_vector(cls, vector_length, parameters: dict):    
            
        vector = []
        for parameter in parameters.items():
                    
            if not('bounds' in parameter[1]):
                bounds = None
            else:
                bounds = parameter[1]['bounds']

            if not('precision' in parameter[1]):
                precision = None
            else:
                precision = parameter[1]['precision']
            
            if (precision == None) and (bounds == None):
                vector.append(cls.gen_number())
                continue
            
            if (precision == None):
                vector.append(cls.gen_number(bounds=bounds))
                continue

            if (bounds == None):
                vector.append(cls.gen_number(precision=precision))
                continue

            vector.append(cls.gen_number(bounds, precision))

        return vector

    @classmethod
    def gen_number(cls, bounds = [], precision = 0, distribution = "uniform"):

        if bounds == []:
            bounds = [0, 1]
        
        if precision == 0:
            precision = 1e-12
            
        if distribution == "uniform":                
            number = random() * (bounds[1] - bounds[0]) + bounds[0] 
            number = round(number / precision) * precision 

        if distribution == "normal":
            mean = (bounds[0] + bounds[1]) / 2
            std = (bounds[1] - bounds[0]) / 6
            number = normal(mean, std)

        return number

class Individual_NSGA_II(Individual):
    
    def __init__(self, x, problem, population_id = 0):
        super().__init__(x, problem, population_id)
        self.dominate = set()
        self.domination_counter = 0
        self.front_number = 0
        self.crowding_distance = 0




if __name__ == '__main__':
    parameters = {'x_1': {'initial_value':10}, 
                  'x_2': {'initial_value':10}}

    vector = Individual.gen_vector(2, parameters)
    print(vector)
    

    