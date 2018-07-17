import sqlite3
import os.path
from string import Template

class DataStore:
    """ Class  ensures saving data from optimization problems. """
    
    database_name =  "data.db"

    def __init__(self):
        #if not os.path.isfile(DataStore.database_name):
        # self.create_database()
        pass

    def create_database(self):        
        connection = sqlite3.connect(DataStore.database_name)
        cursor = connection.cursor()        
        exec_cmd = """
            CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY,
            name TEXT)                       
            """
        cursor.execute(exec_cmd)
        connection.commit()
        cursor.close()
        connection.close()

    def add_problem(self, name):
        connection = sqlite3.connect(DataStore.database_name)
        cursor = connection.cursor()
        exec_cmd_tmp = Template("INSERT INTO problems(name) VALUES ('$x')")        
        cursor.execute(exec_cmd_tmp.substitute(x = name))
        exec_cmd = "SELECT last_insert_rowid()"
        cursor.execute(exec_cmd)
        id = cursor.fetchone()[0]        
        connection.commit()
        cursor.close()
        connection.close()
        return id
    
    def create_table_individual(self, problem_name, parameters, costs):    
                
        connection = sqlite3.connect(DataStore.database_name)
        cursor = connection.cursor()

        exec_cmd_tmp = Template("""
            CREATE TABLE IF NOT EXISTS $name (
            id INTEGER PRIMARY KEY,
            problem_id INTEGER, population_id INTEGER,                        
            """)
        exec_cmd = exec_cmd_tmp.substitute(name = problem_name)    

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
        connection = sqlite3.connect("data.db") # TODO: Move to datastore
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
    datastore = DataStore()
    datastore.create_database()
    datastore.add_problem('Problem')