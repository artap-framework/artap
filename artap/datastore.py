import sqlite3
import os.path
import os
import tempfile
from string import Template
from datetime import datetime

from abc import ABCMeta,abstractmethod
from .individual import Individual
from .population import Population

class DataStore:
    """ Class  ensures saving data from optimization problems. """
    
    def __init__(self): # TODO: Exception if failed?         
        pass        

    def __del__(self):
        pass

    @abstractmethod
    def create_structure(self):        
        pass
    
    @abstractmethod
    def create_structure_individual(self, parameters, costs):    
        pass                

    @abstractmethod
    def write_individual(self, cmd_exec, params):
        pass

    @abstractmethod
    def read_problem(self, problem):       
        pass
        
class SqliteDataStore(DataStore):
    def __init__(self, problem = None, working_dir = None, structure = True, filename = "db.sqlite"): 
        super().__init__()
        
        # self.id = uuid.int_(uuid.uuid4())   # Another way for generating unique ID                
        if (working_dir != None):
            self.database_name = working_dir + "/" + filename
        else:
            parameters_file = tempfile.NamedTemporaryFile(mode = "w", delete=False, suffix=".sqlite")
            parameters_file.close()

            self.database_name = parameters_file.name

        #if os.path.isfile(self.database_name):
        #    os.remove(self.database_name)

        self.connection = sqlite3.connect(self.database_name)
        
        if (structure):
            self.create_structure(problem)
        
        # print(self.database_name)      

    def __del__(self):
        self.connection.close()

        # remove database
        # os.remove(self.database_name)

        super().__del__()

    def create_structure(self, problem):                
        cursor = self.connection.cursor()        
        exec_cmd = """
            CREATE TABLE IF NOT EXISTS problem (            
            name TEXT,
            description TEXT,
            num_parameters NUMBER,
            num_costs NUMBER)      
            """
        cursor.execute(exec_cmd)

        exec_cmd_insert = "INSERT INTO problem(name, num_parameters, num_costs) VALUES ('%s', %i, %i)" % (problem.name, len(problem.parameters), len(problem.costs))
        cursor.execute(exec_cmd_insert)
                
        self.connection.commit()
        cursor.close()

    def create_structure_individual(self, parameters, costs):            
        cursor = self.connection.cursor()

        exec_cmd = "CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, population_id INTEGER, "

        for parameter in parameters.keys():
            exec_cmd += parameter + " NUMBER, "

        for cost in costs:
            exec_cmd += cost + " NUMBER," 
        
        exec_cmd = exec_cmd[:-1]
        exec_cmd += ");"
                
        cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()

    def write_individual(self, params):
        cursor = self.connection.cursor()       

        cmd_exec = "INSERT INTO data VALUES ("

        for i in range(len(params) - 1):
            cmd_exec += " ?,"
        cmd_exec += " ?);"          

        cursor.execute(cmd_exec, params)
        self.connection.commit()
        cursor.close()

    def read_problem(self, problem):       
        cursor = self.connection.cursor()

        # problem
        exec_cmd_problem = "SELECT * FROM problem"
        cursor.execute(exec_cmd_problem)
        data_problem = cursor.fetchall()
        
        problem.name = data_problem[0][0]
        num_parameters = data_problem[0][2]
        num_costs = data_problem[0][3]

        # parameters
        exec_cmd_struct = "pragma table_info('data')"
        columns = []
        for row in cursor.execute(exec_cmd_struct):
            columns.append(row[1])

        problem.parameters = {}        
        for parameter in columns[2:2 + num_parameters]:
            problem.parameters[parameter] =  { 'initial_value': 0.0, 'bounds': [0, 1], 'precision': 1e-1 }

        problem.costs = []
        for cost in columns[2 + num_parameters:2 + num_parameters + num_costs]:
            problem.costs.append(cost)

        exec_cmd_data = "SELECT * FROM data"
        problem.populations = []
        population = Population(problem)
        current_population = 0
        for row in cursor.execute(exec_cmd_data):
            individ = Individual(row[2:2 + num_parameters], problem, row[1])
            individ.costs = row[2 + num_parameters: 2 + num_parameters + num_costs]
            population.individuals.append(individ)
            if (row[1] != current_population):
                problem.populations.append(population.copy())
                population = []
                current_population = row[1]                
        
        problem.populations.append(population)
        cursor.close()
        