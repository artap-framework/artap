import sqlite3
from string import Template
from abc import ABC, abstractmethod

from .datastore import DataStore

"""
 Module is dedicated to describe optimization problem. 
"""

class Population:
    
    size = 0
    number = 0

    def __init__(self, problem, individuals = []):
        self.length = len(individuals)   
        self.problem = problem     
        self.number = Population.number
        Population.number += 1
        
        self.individuals = []

        for vector in individuals:
            individual = Individual(vector, self.problem, self.number)                        
            self.individuals.append(individual)

    def toString(self):
        string = "population number: " + str(self.number) + " \n"
      
        for individual in self.individuals:
            string += individual.toString() + ", "        
        
        return string


    def print(self):
        print(self.toString())

class Problem(ABC):
    """ Is a main class wich collects information about optimization task """    
           
    def __init__(self, name, parameters, costs):                                        
        self.name = name
        self.path_to_source_files = ""
        self.source_files = []
        self.path_to_results = ""                    
        self.parameters = parameters
        self.parameters_values = []
        for parameter in parameters.items():
            if 'initial_value' in parameter[1]:
                self.parameters_values.append(parameter[1]['initial_value'])    
            else:
                self.parameters_values.append(0)
        
        self.costs = {cost:0 for cost in costs}
        self.table_name = self.name
        self.datastore = DataStore(self.name)                
        self.create_table_individual()
        
        self.populations = []
        poppulation = Population(self)
        self.populations.append(poppulation)
        
    def add_population(self, individuals):
        population = Population(self, individuals)
        self.populations.append(population)
    
    def evaluate_population(self, population_number):
        for individual in self.populations[population_number].individuals:
            if individual.is_evaluated == False:
                individual.evaluate()

    
    def create_table_individual(self):
        self.datastore.create_table_individual(self.table_name, self.parameters, self.costs)    
    
    
    def evaluate_individual(self, x, population = 0):
        individ = Individual(x, self, population)        
        individ.evaluate()        
        self.populations[population].individuals.append(individ)
        
        if len(individ.costs) == 1:
            return individ.costs[0]
        else:
            return individ.costs

    def read_from_database(self):        
        self.data = self.datastore.read_all("data")
                       
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    @abstractmethod
    def eval(self):
        pass

    def plot_data(self):
        vector = []
        cost = []
        vector_length = len(self.parameters)
        self.read_from_database()

        for i in range(len(self.data)):
            vector.append(self.data[i][2:2 + vector_length])
            cost.append(self.data[i][2 + vector_length])

        import pylab as pl
        
        for j in range(vector_length):
            y = []
            for i in range(len(vector)):
                y.append(vector[i][j])
            pl.figure(j)        
            pl.plot(y)
            pl.grid() 
        
        pl.figure('Cost function')
        pl.plot(cost)
        
        pl.show()

class Individual:           # TODO: Add: precisions, bounds
    """
       Collects information about one point in design space.
    """   
    number = 0    
    
    def __init__(self, x, problem: Problem, population_id = 0):        
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

        self.toDatabase()        
        return costs

def func(vector):
    y = 0    
    for x in vector:
        y += x*x
    return y

class MyProblem(Problem):
        # Simple example for testing purposes
        def __init__(self, name):
                        
            self.parameters = {'x_0': 10}
            self.costs = ['F1']                    
            super().__init__(name, self.parameters, self.costs)
            
            self.max_population_number = 1
            self.max_population_size = 1
            self.function = func
            self.create_table_individual()
            


# if __name__ == "__main__":    
#     from datastore import DataStore
#     from algorithm import ScipyNelderMead
    
#     problem = MyProblem("Kavadratic_function")
#     function = Function(1, 1)
#     problem.set_function(function)        
#     algorithm = ScipyNelderMead()
#     algorithm.run(problem.evaluate, [10])  
#     problem.plot_data()
    
# else:
#     from .function import Function
#     from .datastore import DataStore