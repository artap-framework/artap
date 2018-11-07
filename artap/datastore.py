import sqlite3
import tempfile
import os
from datetime import datetime
from string import Template
from abc import abstractmethod

from .individual import Individual
from .population import Population
from .utils import flatten


class DataStore:
    """ Class  ensures saving data from optimization problems. """

    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def create_structure(self, problem):
        pass

    def create_structure_individual(self, parameters, costs):
        pass

    def write_individual(self, params):
        pass

    def read_problem(self, problem):
        pass

    def get_id(self):
        pass


class SqliteDataStore(DataStore):

    def __init__(self, problem=None, database_file=None, working_dir=None, create_database=False):
        super().__init__()

        if working_dir is None:
            self.working_dir = ""
        else:
            self.working_dir = working_dir

        if problem is not None:
            problem.data_store = self

        time_stamp = str(datetime.now())
        if create_database:
            self.database_name = self.working_dir + os.sep + "data" + ".sqlite"
        else:
            if database_file is not None:
                    self.database_name = database_file
            else:
                parameters_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sqlite")
                parameters_file.close()

        self.connection = sqlite3.connect(self.database_name)

    def __del__(self):
        pass
        # remove database
        # self.connection_problem.close()
        # self.connection.close()
        # os.remove(self.database_name)
        super().__del__()

    def save_problem(self, problem):
        pass

    def create_structure_task(self, problem):
        cursor = self.connection.cursor()
        exec_cmd = 'CREATE TABLE IF NOT EXISTS problem (INTEGER PRIMARY KEY, ' \
                   'name TEXT, ' \
                   'description TEXT,' \
                   'algorithm TEXT,' \
                   'calculation_time NUMBER,' \
                   'state TEXT)'

        cursor.execute(exec_cmd)
        exec_cmd = "INSERT INTO problem(name, description, state) " \
                   "values('%s', '%s', '%s');" % (problem.name, problem.description, "running")
        cursor.execute(exec_cmd)
        self.connection.commit()
        cursor.close()

    def create_structure_individual(self, parameters, costs):
        cursor = self.connection.cursor()
        exec_cmd = 'CREATE TABLE IF NOT EXISTS data (id INTEGER, population_id INTEGER, '

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
            length = len(parameter)
            parameter_arg[0:length] = parameter
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
        cmd_exec = Template("INSERT INTO data VALUES ($params)")
        params_substitute = ""

        flat_params = flatten(params)
        for i in range(len(flat_params) - 1):
            params_substitute += " ?,"
        params_substitute += " ?"

        cmd_exec = cmd_exec.substitute(params=params_substitute)
        cursor.execute(cmd_exec, flat_params)
        self.connection.commit()
        cursor.close()

    def read_problem(self, problem):
        cursor = self.connection.cursor()

        exec_cmd_problem = "SELECT * FROM problem"
        problem_table = cursor.execute(exec_cmd_problem).fetchall()
        problem.name = problem_table[0][1]

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

        current_population = 0

        is_all = False

        data = cursor.execute(exec_cmd_data)
        while not is_all:
            population = Population(problem)
            is_all = True
            for row in data:
                if row[1] == current_population:
                    individual = Individual(row[2:2 + len(problem.parameters)], problem, row[1])
                    individual.costs = row[2 + len(problem.parameters): 2 + len(problem.parameters) + len(problem.costs)]
                    population.individuals.append(individual)
                    del row
                else:
                    is_all = False
            problem.populations.append(population)
            current_population +=1

        problem.populations.append(population)
        cursor.close()

    def close_connection(self):
        self.connection.close()
