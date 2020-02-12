import sqlite3
import os
import time
import logging
from abc import abstractmethod
from sqlitedict import SqliteDict

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
        # self.worker_loop = asyncio.new_event_loop()
        # worker = Thread(target=self._start_worker, args=(self.worker_loop,))
        # worker.daemon = True
        # # Start the thread
        # worker.start()

        # populations
        self.populations = []

    def __del__(self):
        # print("DataStore:def __del__(self):")
        pass

    # def _start_worker(self, loop):
    #     asyncio.set_event_loop(loop)
    #     loop.run_forever()

    @abstractmethod
    def create_structure(self):
        pass

    @abstractmethod
    def write_individual(self, individual):
        # TODO: check this hack
        if len(self.populations) == 0:
            self.populations.append(Population())

        # add individual
        self.populations[-1].individuals.append(individual)

    @abstractmethod
    def write_population(self, population):
        self.populations.append(population)

    def get_id(self):
        return 0


class FileDataStore(DataStore):

    def __init__(self, problem, database_name=None, remove_existing=True, mode="write", backend="sqlitedict"):
        super().__init__(problem)

        self.database_name = database_name
        self.mode = mode

        if remove_existing and mode == "write":
            if os.path.exists(self.database_name):
                os.remove(self.database_name)

        if backend == "sqlitedict":
            self.db = SqliteDict(self.database_name, autocommit=True)
            if self.mode == "write":
                # remove database and create structure
                if remove_existing and os.path.exists(self.database_name):
                    self.create_structure()
            else:
                self.read_from_datastore()
        elif backend == "shelve":
            import shelve

            if self.mode == "write":
                self.db = shelve.open(self.database_name, flag='c', writeback=True)
                # remove database and create structure
                if remove_existing and os.path.exists(self.database_name):
                    self.create_structure()
            else:
                self.db = shelve.open(self.database_name, flag='r')
                self.read_from_datastore()
        else:
            assert 1

        # set datastore to problem
        self.problem.data_store = self

    def __del__(self):
        super().__del__()

    def create_structure(self):
        self.db["name"] = self.problem.name
        self.db["description"] = self.problem.description
        self.db["parameters"] = self.problem.parameters
        self.db["costs"] = self.problem.costs

        self.db["populations"] = []

    def write_individual(self, individual):
        # add individual
        super().write_individual(individual)

        if self.mode == "write":
            # TODO: check this hack
            populations = self.db["populations"]
            if len(populations) == 0:
                populations.append(Population())

            # add individual
            populations[-1].individuals.append(individual)
            self.db["populations"] = populations

    def write_population(self, population):
        super().write_population(population)

        if self.mode == "write":
            # write to database
            populations = self.db["populations"]
            populations.append(Population())
            self.db["populations"] = populations

    def read_from_datastore(self):
        self.problem.name = self.db["name"]
        self.problem.description = self.db["description"]
        self.problem.parameters = self.db["parameters"]
        self.problem.costs = self.db["costs"]

        self.populations = self.db["populations"]


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

    def write_population(self, population):
        super().write_population(population)