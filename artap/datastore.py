import sqlite3
import tempfile
import os
import datetime

from abc import abstractmethod

from .individual import Individual
from .population import Population
from .utils import flatten
from .enviroment import Enviroment


class DataStore:
    """ Class  ensures saving data from optimization problems. """

    def __init__(self):  # TODO: Exception if failed?
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

    @abstractmethod
    def get_id(self):
        pass


class SqliteDataStore(DataStore):

    def __init__(self, problem=None, problem_id=1, new_database=True, working_dir=None):
        super().__init__()

        self.database_name = None
        self.id = problem_id
        self.connection_problem = sqlite3.connect(Enviroment.artap_root + "/problems.db")
        self.problem = problem

        time_stamp = str(datetime.datetime.now())

        if (new_database):
            self.create_structure(problem)
            if  working_dir != None:
                self.database_name = working_dir + "/" + self.problem.name + time_stamp + ".sqlite"
                if problem != None:
                    self.save_problem(problem)
                    problem.datastore = self
            else:
                parameters_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sqlite")
                parameters_file.close()

                self.database_name = parameters_file.name

        else:
            cursor_problem = self.connection_problem.cursor()

            # problem
            exec_cmd_problem = "SELECT * FROM problem WHERE id = %s" % str(self.id)
            cursor_problem.execute(exec_cmd_problem)
            data_problem = cursor_problem.fetchall()

            self.problem_name = data_problem[0][0]
            self.num_parameters = data_problem[0][3]
            self.num_costs = data_problem[0][4]
            self.database_name = data_problem[0][5]

            cursor_problem.close()

            if not (os.path.exists(self.database_name)):
                raise IOError("Database file not found!")

            # if (working_dir != None):
            #    self.database_name = working_dir + "/" + filename

        self.connection = sqlite3.connect(self.database_name)

    def __del__(self):
        pass
        # remove database
        # os.remove(self.database_name)
        self.connection_problem.close()
        self.connection.close()
        super().__del__()

    def save_problem(self, problem):
        cursor = self.connection_problem.cursor()
        exec_cmd_insert = "INSERT INTO problem(name, database_file, num_parameters, num_costs) VALUES ('%s', '%s', %i, %i)" % (
        problem.name, self.database_name, len(problem.parameters), len(problem.costs))
        cursor.execute(exec_cmd_insert)
        self.connection_problem.commit()
        cursor.close()

    def create_structure(self, problem):

        cursor = self.connection_problem.cursor()
        exec_cmd = """
            CREATE TABLE IF NOT EXISTS problem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,            
            name TEXT,
            description TEXT,            
            database_file TEXT,            
            num_parameters NUMBER,
            num_costs NUMBER)      
            """
        cursor.execute(exec_cmd)

        self.connection_problem.commit()
        cursor.close()

    def create_structure_individual(self, parameters, costs):
        cursor = self.connection.cursor()
        exec_cmd = 'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, population_id INTEGER, '

        for parameter in parameters.keys():
            exec_cmd += parameter + " NUMBER, "

        for cost in costs:
            exec_cmd += cost + " NUMBER,"

        exec_cmd = exec_cmd[:-1]
        exec_cmd += ");"

        cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()

    def create_structure_parameters(self, parameters_list):
        cursor = self.connection.cursor()
        exec_cmd = 'CREATE TABLE IF NOT EXISTS parameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,' \
                   'initial_value NUMBER, low_boundary NUMBER, high_boundary NUMBER, precision NUMBER);'
        cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()
        cursor = self.connection.cursor()
        for parameter in parameters_list:
            parameter_arg = [0] * 5
            l = len(parameter)
            parameter_arg[0:l] = parameter
            exec_cmd = 'INSERT INTO parameters(name, initial_value, low_boundary, high_boundary, precision) ' \
                    "VALUES( '%s', %f, %f, %f, %f);" % tuple(parameter_arg)
            cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()

    def create_structure_costs(self, costs):
        cursor = self.connection.cursor()
        exec_cmd = 'CREATE TABLE IF NOT EXISTS costs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);'
        cursor.execute(exec_cmd)
        for cost in costs:
            exec_cmd = "INSERT INTO costs(name) values('%s');" % cost
        cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()


    def write_individual(self, params):
        cursor = self.connection.cursor()
        cmd_exec = "INSERT INTO data VALUES ("

        flat_params = flatten(params)
        for i in range(len(flat_params) - 1):
            cmd_exec += " ?,"
        cmd_exec += " ?);"

        cursor.execute(cmd_exec, flat_params)
        self.connection.commit()
        cursor.close()

    def read_problem(self, problem):
        cursor = self.connection.cursor()

        # parameters
        exec_cmd_params = "SELECT * FROM parameters"

        columns = []
        for row in cursor.execute(exec_cmd_params):
            columns.append(row)

        problem.parameters = {}
        for parameter in columns:
            problem.parameters[parameter[1]] = {'initial_value': parameter[2],
                                             'bounds': [parameter[3], parameter[4]], 'precision': parameter[5]}

        exec_cmd_costs = "SELECT * FROM costs"

        problem.costs = []
        for cost in cursor.execute(exec_cmd_costs):
            problem.costs.append(cost[1])

        exec_cmd_data = "SELECT * FROM data"
        problem.populations = []
        population = Population(problem)
        current_population = 0
        for row in cursor.execute(exec_cmd_data):
            individ = Individual(row[2:2 + self.num_parameters], problem, row[1])
            individ.costs = row[2 + self.num_parameters: 2 + self.num_parameters + self.num_costs]
            population.individuals.append(individ)
            if (row[1] != current_population):
                problem.populations.append(next_population.copy())
                next_population = []
                current_population = row[1]

        problem.populations.append(population)
        cursor.close()

        def get_id(self):
            return 0
