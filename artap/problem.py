import sqlite3
from string import Template

"""
 Module is dedicated to describe optimization problem. 
"""

class Population:
    number = 0
    def __init__(self, individuals = []):
        self.length = len(individuals)
        self.number = Population.number
        Population.number += 1
        self.individuals = individuals

        for i in range(len(self.individuals)):
            self.individuals[i].population_number = self.number 

    def toString(self):
        string = "population number: " + str(self.number)
        return string

    def print(self):
        print(self.toString())

class Problem:
    """ Is a main class wich collects information about optimization task """    
           
    def __init__(self, name, parameters, costs):                        
        self.name = name    
        self.parameters = parameters
        self.costs = {cost:0 for cost in costs}
        self.datastore = DataStore()
        self.id = self.datastore.add_problem(name)
        self.table_name = self.name + "_" + str(self.id)
        self.create_table_individual()

        
    def create_table_individual(self):
        self.datastore.create_table_individual(self.table_name, self.parameters, self.costs)    

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def set_function(self, function):
        self.function = function.eval
    
    def evaluate(self, x):
        individ = Individual(self)        
        individ.evaluate(x)        
        if len(individ.costs) == 1:
            return individ.costs[0]
        else:
            return individ.costs

    def read_from_database(self):        
        self.data = self.datastore.read_all()
        
        
        

    def  plot_data(self):
        vector = []
        cost = []
        vector_length = len(self.parameters)

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


class Individual:
    """
       Collects information about one point in design space.
    """   
    number = 0    
    
    def __init__(self, problem: Problem):        
        self.problem = problem
        self.length = len(problem.parameters)        
        self.costs = []                
        self.number = 0
        self.function = problem.function
        self.population_id = 0        

    def toString(self):
        string = "["
        for number in self.vector:
            string += str(number) + ", "
        string = string[:len(string)-1]
        string += "]\n"
        return string

    
    def toDatabase(self): 
        id = self.number        
        cmd_exec_tmp = Template("INSERT INTO $table (id, problem_id, population_id, ")  # TODO: rewrite using string templates
        cmd_exec = cmd_exec_tmp.substitute(table = self.problem.table_name)        

        
        if type(self.costs != list):
            costs = [self.costs]
        else:
            costs = self.costs
        
        for parameter_name in self.problem.parameters.keys():
            cmd_exec += parameter_name + ","
        
        for cost_name in self.problem.costs.keys():
            cmd_exec += cost_name + ","

        cmd_exec = cmd_exec[:-1]  # delete last comma
        cmd_exec += ") VALUES (?, ?, ?, "

        for i in range(len(self.vector) + len(costs) - 1):
            cmd_exec += " ?,"
        cmd_exec += " ?);"           
               
        params = [id , self.problem.id, self.population_id]
        
        for i in range(len(self.vector)):
            params.append(self.vector[i])
        
        for cost in self.costs:
            params.append(cost)

        self.problem.datastore.write_individual(cmd_exec, params)    
        
        
    def evaluate(self, vector):        
        self.vector = vector        
        self.length = len(vector)        
        costs = self.function(vector)            

        if type(costs) != list:
            self.costs = [costs]
        else:
            self.costs = costs
        print(self.costs)
        self.number = Individual.number
        Individual.number += 1        
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
                        
            self.parameters = {'x_0': 10,'x_1': 10}
            self.costs = ['F1']                    
            super().__init__(name, self.parameters, self.costs)
            
            self.max_population_number = 1
            self.max_population_size = 1
            self.function = func
            self.create_table_individual()
            


if __name__ == "__main__":    
    from function import Function
    from datastore import DataStore
    datastore = DataStore()
    datastore.create_database()
    problem = MyProblem("Problem")   

    x = list(problem.parameters.values())
    problem.evaluate(x)
    
else:
    from .function import Function
    from .datastore import DataStore