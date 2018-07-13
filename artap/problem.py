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
           
    def __init__(self, name):                        
        self.name = name    
        self.parameters = dict()
        self.costs = []
        self.datastore = DataStore()
        self.id = self.datastore.add_problem(name)

        
    def create_table_individual(self):
        self.datastore.create_table_individual(self.name + "_" + str(self.id), self.parameters, self.costs)    

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def set_function(self, function):
        self.function = function.eval
    
    def evaluate(self, x):
        individ = Individual()
        individ.set_eval(self.function) # TODO: Move to settings? 
        individ.evaluate(x)
        return individ.cost
 

    def read_from_database(self):        
        connection = sqlite3.connect(self.database_name) # TODO: Generalize, time stamp?
        cursor = connection.cursor()
        exec_cmd = """ SELECT * FROM structures """            
        cursor.execute(exec_cmd)
        self.data = cursor.fetchall()                
        connection.commit()
        cursor.close()
        connection.close()
        
        

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
        self.cost = 0                
        self.number = 0
        self.function = problem.function        

    def toString(self):
        string = "["
        for number in self.vector:
            string += str(number) + ", "
        string = string[:len(string)-1]
        string += "]\n"
        return string

    
    def toDatabase(self): 
        connection = sqlite3.connect("problem.db") # ToDo: Move to datastore
        cursor = connection.cursor()       
        id = self.number
        name = self.problem.name
        
        cmd_exec = "INSERT INTO structures (id,name,"
        
        for i in range(len(self.vector)):
            cmd_exec += "x" + str(i) + ","
        cmd_exec += "cost) VALUES (?, ?,"
        for i in range(len(self.vector)):
            cmd_exec += "?, "
        cmd_exec += "?);"           
        
        params = [id , name]
        for i in range(len(self.vector)):
            params.append(self.vector[i])
        params.append(self.cost)

        cursor.execute(cmd_exec, params)
        connection.commit()
        cursor.close()
        connection.close()
        
    def evaluate(self, vector):        
        self.vector = vector        
        self.length = len(vector)        
        self.cost = self.function(vector)
        self.number = Individual.number
        Individual.number += 1        
        self.toDatabase()


class MyProblem(Problem):
        # Simple example for testing purposes
        def __init__(self, name):
            
            super().__init__(name)
            print(self.id)    
            self.max_population_number = 1
            self.max_population_size = 1
            self.parameters = {'x_1': 10,'x_2': 10}
            self.costs = ['F1']
            self.create_table_individual()


if __name__ == "__main__":    
    from function import Function
    from datastore import DataStore
    problem = MyProblem("Problem")
    
else:
    from .function import Function
    from .datastore import DataStore