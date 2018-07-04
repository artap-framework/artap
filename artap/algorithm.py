import sqlite3

class Individual:   
    number = 0    
    def __init__(self,  vector = []):
        self.length = len(vector)
        self.vector = vector
        self.cost = 0        
        self.population_number = 0
        self.number = 0
        

    def toString(self):
        string = "["
        for number in self.vector:
            string += str(number) + ", "
        string = string[:len(string)-1]
        string += "]\n"
        return string

    
    def toDatabase(self):
        connection = sqlite3.connect("problem.db") # ToDo: Generalize, time stamp?
        cursor = connection.cursor()       
        id = self.number
        name = "problem_1"   # ToDo: Generalize
        
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
        

    def set_eval(self, eval):
        self.eval = eval

    def evaluate(self, vector):        
        self.vector = vector
        
        self.length = len(vector)        
        self.cost = self.eval(vector)
        self.number = Individual.number
        Individual.number += 1        
        self.toDatabase()


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
    number = 0
    max_population_number = 0
    max_population_size = 0
    vector_length = 0
    boundaries = []
    database_name = "problem.db"

    def __init__(self, population_number = 0, population_size = 0, vector_length = 0):
        self.max_population_number = population_number
        self.max_population_size = population_size
        self.vector_length = vector_length

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def set_eval(self, eval):
        self.eval = eval
    
    def evaluate(self, x):
        individ = Individual()
        individ.set_eval(self.eval) # ToDo: Move to settings? 
        individ.evaluate(x)
        return individ.cost
 
    def create_database(self):        
        connection = sqlite3.connect(self.database_name) # ToDo: Generalize, time stamp?
        cursor = connection.cursor()
        cursor.execute(""" DROP TABLE IF EXISTS structures;""")
        exec_cmd = """
            CREATE TABLE structures (
            id INTEGER PRIMARY KEY,
            name TEXT,                        
            """
        for i in range(self.vector_length):
            exec_cmd += "x"+ str(i) + " NUMBER, \n"
        
        exec_cmd += "cost NUMBER" 
        exec_cmd += ");"
        
        cursor.execute(exec_cmd)
        connection.commit()
        cursor.close()
        connection.close()

    def read_from_database(self):
        connection = sqlite3.connect(self.database_name) # ToDo: Generalize, time stamp?
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
        
        for i in range(len(self.data)):
            vector.append(self.data[i][2:2 + self.vector_length])
            cost.append(self.data[i][2 + self.vector_length])

        import pylab as pl
        
        for j in range(self.vector_length):
            y = []
            for i in range(len(vector)):
                y.append(vector[i][j])
            pl.figure(j)        
            pl.plot(y)
            pl.grid() 
        
        pl.figure('Cost function')
        pl.plot(cost)
        
        pl.show()

def function(x):
    result = 0
    for i in x:
        result += i*i
    return result


#x = Individual([1.0, 1.0, 1.0])
#print(x.toString())

problem = Problem(1, 100, 1)
problem.set_eval(function)
problem.create_database()

from scipy.optimize import minimize
es = minimize(problem.evaluate, [10], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
problem.read_from_database()
problem.plot_data()