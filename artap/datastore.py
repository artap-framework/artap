import sqlite3
import tempfile
import os
import json
import time
from threading import Thread
import asyncio
import logging

from abc import abstractmethod

from .individual import Individual
from .population import Population


class SqliteHandler(logging.Handler):
    """
    Thread-safe logging handler for SQLite.
    """

    def __init__(self, data_store):
        logging.Handler.__init__(self)

        self.data_store = data_store
        self.data_store.create_structure_log()

    def emit(self, record: logging.LogRecord):
        """

        self.format(record)
        # format record
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        if record.exc_info:  # for exceptions
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        """

        # Insert the log record
        try:
            connection = sqlite3.connect(self.data_store.database_name)

            cursor = connection.cursor()
            cursor.execute("INSERT INTO log(timestamp, source, loglevel, loglevelname, message, args, module, funcname, lineno, exception, process, threadname) "
                           "VALUES (:timestamp, :source, :loglevel, :loglevelname, :message, :args, :module, :funcname, :lineno, :exception, :process, :threadname)",
                           { "timestamp": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))),
                             "source": str(record.name),
                             "loglevel": record.levelno,
                             "loglevelname": str(record.levelname),
                             "message": str(record.getMessage()),
                             "args": str(record.args),
                             "module": str(record.module),
                             "funcname": str(record.funcName),
                             "lineno": record.lineno,
                             "exception": str(record.exc_text),
                             "process": record.process,
                             "threadname": str(record.threadName) })
            connection.commit()
            cursor.close()

            connection.close()
        except sqlite3.Error as e:
            print("SqliteHandler: error occurred:", e.args[0])


class DataStore:
    """ Class  ensures saving data from optimization problems. """

    def __init__(self, problem):
        self.problem = problem

        # create the new loop and worker thread
        self.worker_loop = asyncio.new_event_loop()
        worker = Thread(target=self._start_worker, args=(self.worker_loop,))
        worker.daemon = True
        # Start the thread
        worker.start()

        # populations
        self.populations = []
        # individuals ???
        self.individuals = []

    def __del__(self):
        # print("DataStore:def __del__(self):")
        pass

    def _start_worker(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    @abstractmethod
    def create_structure(self):
        pass

    @abstractmethod
    def write_individual(self, individual):
        # print("write_individual: {}".format(individual))
        self.individuals.append(individual)

    @abstractmethod
    def write_population(self, population, index=0):
        self.populations.append(population)
        # print("write_population: {}/{}".format(len(population.individuals), len(self.populations)))

    def get_id(self):
        return 0


class SqliteDataStore(DataStore):
    def __init__(self, problem, database_name=None, remove_existing=True):
        super().__init__(problem)

        self.database_name = database_name

        # remove database and create structure
        if remove_existing and os.path.exists(self.database_name):
            os.remove(self.database_name)
            self.create_structure()

        # set datastore to problem
        self.problem.data_store = self

        # set db log
        if self.problem.options['log_db_handler']:
            # create file handler and set level to debug
            file_handler = SqliteHandler(self)
            file_handler.setLevel(logging.DEBUG)
            # add formatter to SqliteHandler
            file_handler.setFormatter(self.problem.formatter)
            # add SqliteHandler to logger
            self.problem.logger.addHandler(file_handler)

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

    def _create_structure_task(self):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS problem (INTEGER PRIMARY KEY, ' \
                   'name TEXT, ' \
                   'description TEXT,' \
                   'algorithm TEXT,' \
                   'calculation_time NUMBER,' \
                   'state TEXT)'
        self._execute_command(exec_cmd)

        exec_cmd = "INSERT INTO problem(name, description, state) " \
                   "values('%s', '%s', '%s');" % (self.problem.name, self.problem.description, "running")
        self._execute_command(exec_cmd)

    def _create_structure_individual(self):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS data (id INTEGER, population_id INTEGER, '

        for parameter in self.problem.parameters.keys():
            exec_cmd += parameter + " NUMBER, "

        for cost in self.problem.costs:
            exec_cmd += cost + " NUMBER,"

        exec_cmd += 'front_number NUMBER, crowding_distance NUMBER, feasible NUMBER, dominates JSON, gradient JSON'
        exec_cmd += ");"

        self._execute_command(exec_cmd)

    def _create_structure_parameters(self):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS parameters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,' \
                   'initial_value NUMBER, low_boundary NUMBER, high_boundary NUMBER, precision NUMBER);'
        self._execute_command(exec_cmd)

        for parameter in self.problem.parameters.items():
            exec_cmd = "INSERT INTO parameters(name, initial_value, low_boundary, high_boundary, precision) " \
                       "VALUES( '{}', {}, {}, {}, {});".format(parameter[0], parameter[1]['initial_value'],
                                                               parameter[1]['bounds'][0], parameter[1]['bounds'][1],
                                                               parameter[1]['precision'] if 'precision' in parameter[1] else 0)
            self._execute_command(exec_cmd)

    def _create_structure_costs(self):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS costs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);'
        self._execute_command(exec_cmd)

        for cost in self.problem.costs:
            exec_cmd = "INSERT INTO costs(name) values('%s');" % cost
            self._execute_command(exec_cmd)

    def create_structure(self):
        self._create_structure_task()
        self._create_structure_individual()
        self._create_structure_parameters()
        self._create_structure_costs()

    def create_structure_log(self):
        exec_cmd = 'CREATE TABLE IF NOT EXISTS log(' \
                    'timestamp TEXT,' \
                    'source TEXT,' \
                    'loglevel INT,' \
                    'loglevelname TEXT,' \
                    'message TEXT,' \
                    'args TEXT,' \
                    'module TEXT,' \
                    'funcname TEXT,' \
                    'lineno INT,' \
                    'exception TEXT,' \
                    'process INT,' \
                    'threadname TEXT)'

        self._execute_command(exec_cmd)

    def write_individual(self, individual):
        # add individual
        super().write_individual(individual)

        # add to database
        if self.problem.options['save_level'] == "individual":
            params = individual.to_list()
            # individual index
            params.insert(0, self.individuals.index(individual) + 1)
            # population index
            params.insert(1, len(self.populations) + 1)

            exec_cmd = "INSERT INTO data VALUES ("

            for i in range(len(params) - 1):
                if params[i] == float('inf'):
                    params[i] = -1
                if type(params[i]) == list:
                    par = "'" + str(params[i]) + "'"
                else:
                    par = str(params[i])
                exec_cmd += " " + par + ","

            if type(params[i]) == list:
                par = "'" + str(params[i]) + "'"
            else:
                par = str(params[i])
            exec_cmd += " " + par + ")"

            self._execute_command(exec_cmd)

    def write_population(self, population, index):
        super().write_population(population, index)
        connection = sqlite3.connect(self.database_name)
        table = population.to_list(index)
        cursor = connection.cursor()
        for params in table:
            exec_cmd = "INSERT INTO data VALUES ("
            for i in range(len(params) - 1):
                if params[i] == float('inf'):
                    params[i] = -1
                if type(params[i]) == list:
                    par = "'" + str(params[i]) + "'"
                else:
                    par = str(params[i])
                exec_cmd += " " + par + ","

            if type(params[i]) == list:
                par = "'" + str(params[i]) + "'"
            else:
                par = str(params[i])
            exec_cmd += " " + par + ")"

            cursor.execute(exec_cmd)
        cursor.close()
        connection.commit()
        connection.close()

    def read_from_datastore(self):
        connection = sqlite3.connect(self.database_name)
        # connection.execute('pragma journal_mode=wal')

        cursor = connection.cursor()

        exec_cmd_problem = "SELECT * FROM problem"
        problem_table = cursor.execute(exec_cmd_problem).fetchall()
        self.problem.name = problem_table[0][1]

        # parameters
        exec_cmd_params = "SELECT * FROM parameters"
        columns = []
        for row in cursor.execute(exec_cmd_params):
            columns.append(row)

        self.problem.parameters = {}
        for parameter in columns:
            self.problem.parameters[parameter[1]] = {'initial_value': parameter[2],
                                                'bounds': [parameter[3], parameter[4]], 'precision': parameter[5]}
        exec_cmd_costs = "SELECT * FROM costs"

        # costs
        costs = []
        for cost in cursor.execute(exec_cmd_costs):
            costs.append(cost[1])
        self.problem.costs = {cost: 0.0 for cost in costs}

        exec_cmd_data = "SELECT * FROM data"
        data = cursor.execute(exec_cmd_data)

        # clear populations and individuals
        self.individuals = []
        self.populations = []
        # new population
        population = Population()
        self.populations.append(population)

        table = list()
        for row in data:
            table.append(row)

        cursor.close()
        connection.close()

        table.sort(key=lambda x: x[1])  # Sorting according to population number

        current_population = table[0][1]
        for row in table:
            if row[1] == current_population:
                individual = Individual(list(row[2:2 + len(self.problem.parameters)]))
                l = 2 + len(self.problem.parameters) + len(self.problem.costs)
                individual.costs = row[2 + len(self.problem.parameters): 2 + len(self.problem.parameters) + len(self.problem.costs)]
                individual.front_number = row[l]
                individual.crowding_distance = row[l+1]
                individual.feasible = row[l+2]
                individual.dominate = json.loads(row[l+3])
                individual.gradient = json.loads(row[l+4])

                # add individual
                self.individuals.append(individual)
                # add to population
                population.individuals.append(individual)
            else:
                # increase population
                self.populations.append(population)
                population = Population()
                current_population = row[1]


class DummyDataStore(DataStore):

    def __init__(self, problem=None):
        super().__init__(problem)
        self.create_structure()

    def __del__(self):
        super().__del__()

    def create_structure(self):
        pass

    def write_individual(self, individual):
        super().write_individual(individual)

    def write_population(self, population, index=0):
        super().write_population(population, index)
