import sqlite3
import os.path
import os
from string import Template
from datetime import datetime


class DataStore:
    """ Class  ensures saving data from optimization problems. """
    
    def __init__(self, name, exact_name = False):                      # TODO: Exception if failed?         
        print(os.getcwd())
        # self.id = uuid.int_(uuid.uuid4())   # Another way for generating unique ID                
        if (exact_name):
            problem_name = name
        else:
            problem_name = name + "_"  + str(datetime.now())
        self.database_name = "database.db"        
        os.makedirs(problem_name)
        os.chdir("./" + problem_name)
        self.create_table_problem()
        self.add_problem('Problem')
        
        # if not os.path.isfile(self.database_name):        
        #    self.create_database()
        

    # Prepared for the case of one big database file
    def create_table_problem(self):        
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()        
        exec_cmd = """
            CREATE TABLE IF NOT EXISTS problem_details (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT)                       
            """
        cursor.execute(exec_cmd)
        connection.commit()
        cursor.close()
        connection.close()

    # Prepared for the case of one big database file
    def add_problem(self, name):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        exec_cmd_tmp = Template("INSERT INTO problem_details(name) VALUES ('$x')")        
        cursor.execute(exec_cmd_tmp.substitute(x = name))
        
        #exec_cmd = "SELECT last_insert_rowid()"
        #cursor.execute(exec_cmd)
        #id = cursor.fetchone()[0]        
        connection.commit()
        cursor.close()
        connection.close()
        return id
    
    def create_table_individual(self, problem_name, parameters, costs):    
                
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        exec_cmd_tmp = Template("""
            CREATE TABLE IF NOT EXISTS $name (
            id INTEGER PRIMARY KEY,
            population_id INTEGER,                        
            """)
        exec_cmd = exec_cmd_tmp.substitute(name = "data")    

        for parameter in parameters.keys():
            exec_cmd += parameter + " NUMBER, \n"

        for cost in costs:
            exec_cmd += cost + " NUMBER" 
            exec_cmd += ");"
                
        cursor.execute(exec_cmd)
        connection.commit()
        cursor.close()
        connection.close()

    def write_individual(self, cmd_exec, params):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()       
        cursor.execute(cmd_exec, params)
        connection.commit()
        cursor.close()
        connection.close()


    def read_all(self, table):       
        connection = sqlite3.connect(self.database_name) 
        cursor = connection.cursor()
        exec_cmd_tmp = Template("SELECT * FROM $table_name")
        exec_cmd = exec_cmd_tmp.substitute(table_name = table)
        cursor.execute(exec_cmd)
        data = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return data
        

if __name__ == "__main__":    
    datastore = DataStore('nova_database')
    