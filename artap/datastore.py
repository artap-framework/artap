import sqlite3
import tempfile
import os
import json
# from datetime import datetime
from abc import abstractmethod

from .individual import Individual
from .population import Population
# from .utils import flatten

from threading import Thread
# from threading import Lock
import asyncio


class DataStore:
    """ Class  ensures saving data from optimization problems. """

    def __init__(self):
        # create the new loop and worker thread
        self.worker_loop = asyncio.new_event_loop()
        worker = Thread(target=self._start_worker, args=(self.worker_loop,))
        worker.daemon = True
        # Start the thread
        worker.start()

    def __del__(self):
        # print("DataStore:def __del__(self):")
        pass

    def _start_worker(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

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

        if create_database:
            self.database_name = self.working_dir + os.sep + "data" + ".sqlite"
            if os.path.exists(self.database_name):
                os.remove(self.database_name)
        else:
            if database_file is not None:
                self.database_name = database_file
            else:
                parameters_file = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite")
                parameters_file.close()
                self.database_name = parameters_file.name()

    def __del__(self):
        super().__del__()

    def _execute_command(self, command):
        """  """
        self._execute_command_async(self.database_name, command)
        # self.worker_loop.call_soon_threadsafe(self._execute_command_async, self.database_name, command)

    @staticmethod
    def _execute_command_async(database_name, command):
        # print(database_name)
        # print(command)

        try:
            connection = sqlite3.connect(database_name)
            # connection.execute('pragma journal_mode=wal')

            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            cursor.close()

            connection.close()
        except sqlite3.Error as e:
            print("SqliteDataStore: execute: error occurred:", e.args[0])

    def save_problem(self, problem):
        pass

    def create_structure_task(self, problem):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS problem (INTEGER PRIMARY KEY, ' \
                   'name TEXT, ' \
                   'description TEXT,' \
                   'algorithm TEXT,' \
                   'calculation_time NUMBER,' \
                   'state TEXT)'
        self._execute_command(exec_cmd)

        exec_cmd = "INSERT INTO problem(name, description, state) " \
                   "values('%s', '%s', '%s');" % (problem.name, problem.description, "running")
        self._execute_command(exec_cmd)

    def create_structure_individual(self, parameters, costs):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS data (id INTEGER, population_id INTEGER, '

        for parameter in parameters.keys():
            exec_cmd += parameter + " NUMBER, "

        for cost in costs:
            exec_cmd += cost + " NUMBER,"

        exec_cmd += 'front_number NUMBER ,crowding_distance NUMBER, feasible NUMBER, dominates JSON, gradient JSON'
        exec_cmd += ");"

        self._execute_command(exec_cmd)

    def create_structure_parameters(self, parameters_list):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS parameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,' \
                   'initial_value NUMBER, low_boundary NUMBER, high_boundary NUMBER, precision NUMBER);'
        self._execute_command(exec_cmd)

        for parameter in parameters_list:
            parameter_arg = [0] * 5
            length = len(parameter)
            parameter_arg[0:length] = parameter
            exec_cmd = 'INSERT INTO parameters(name, initial_value, low_boundary, high_boundary, precision) ' \
                       "VALUES( '%s', %f, %f, %f, %f);" % tuple(parameter_arg)
            self._execute_command(exec_cmd)

    def create_structure_costs(self, costs):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS costs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);'
        self._execute_command(exec_cmd)

        for cost in costs:
            exec_cmd = "INSERT INTO costs(name) values('%s');" % cost
            self._execute_command(exec_cmd)

    def write_individual(self, params):
        exec_cmd = "INSERT INTO data VALUES ("
        for i in range(len(params) - 1):
            exec_cmd += " " + str(params[i]) + ","
        exec_cmd += " " + str(params[i]) + ")"

        self._execute_command(exec_cmd)

    def write_population(self, table):
        connection = sqlite3.connect(self.database_name)

        for params in table:
            exec_cmd = "INSERT INTO data VALUES ("
            for i in range(len(params) - 2):
                exec_cmd += " " + str(params[i]) + ","
<<<<<<< HEAD
            exec_cmd += " " + json.dumps(params[i + 1]) + ","
            exec_cmd += " " + json.dumps(params[i+2]) + ")"
=======
            exec_cmd += " '" + json.dumps(params[i+1]) + "', '"
            exec_cmd += json.dumps(params[i+2]) + " ')"
>>>>>>> 90fd69bff6445bf07b0d19b7c9c6f48939a0ba4c
            cursor = connection.cursor()
            cursor.execute(exec_cmd)
            cursor.close()
        connection.commit()
        connection.close()

    def read_problem(self, problem):
        connection = sqlite3.connect(self.database_name)
        # connection.execute('pragma journal_mode=wal')

        cursor = connection.cursor()

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

        costs = []
        for cost in cursor.execute(exec_cmd_costs):
            costs.append(cost[1])
        problem.costs = {cost: 0.0 for cost in costs}

        exec_cmd_data = "SELECT * FROM data"
        problem.populations = []

<<<<<<< HEAD
        current_population = 0

        is_all = False

        # TODO: Specify structure of data somewhere

        data = cursor.execute(exec_cmd_data)
        while not is_all:
            population = Population(problem)
            is_all = True
            for row in data:
                if row[1] == current_population+1:
                    individual = Individual(row[2:2 + len(problem.parameters)], problem, row[1])
                    l = 2 + len(problem.parameters) + len(problem.costs)
                    individual.costs = row[2 + len(problem.parameters): 2 + len(problem.parameters) + len(problem.costs)]
                    individual.front_number = row[l]
                    individual.crowding_distance = row[l+1]
                    individual.feasible = row[l+2]
                    individual.dominate = row[l+3]
                    individual.gradient = row[l+4]
                    population.individuals.append(individual)
                    row
                else:
                    is_all = False
            problem.populations.append(population)
            current_population += 1
=======
        data = cursor.execute(exec_cmd_data)

        population = Population(problem)
        table = list()
        for row in data:
            table.append(row)
>>>>>>> 90fd69bff6445bf07b0d19b7c9c6f48939a0ba4c

        cursor.close()
        connection.close()

        table.sort(key=lambda x: x[1])  # Sorting according to population number

        current_population = table[0][1]
        for row in table:
            if row[1] == current_population:
                population.number = current_population
                individual = Individual(row[2:2 + len(problem.parameters)], problem, row[1])
                l = 2 + len(problem.parameters) + len(problem.costs)
                individual.costs = row[2 + len(problem.parameters): 2 + len(problem.parameters) + len(problem.costs)]
                individual.front_number = row[l]
                individual.crowding_distance = row[l+1]
                individual.feasible = row[l+2]
                individual.dominate = row[l+3]
                individual.gradient = row[l+4]
                population.individuals.append(individual)
            else:
                problem.populations.append(population)
                population = Population(problem)
                current_population = row[1]

        problem.populations.append(population)
