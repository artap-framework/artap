import threading
from multiprocessing import Process, Event
import os
from enum import Enum
import time
import logging
from abc import abstractmethod
from sqlitedict import SqliteDict

from .population import Population


# class SqliteHandler(logging.Handler):
#     """
#     Thread-safe logging handler for SQLite.
#     """
#
#     def __init__(self, data_store):
#         logging.Handler.__init__(self)
#
#         self.data_store = data_store
#         self.data_store.create_structure_log()
#
#     def emit(self, record: logging.LogRecord):
#         """
#
#         self.format(record)
#         # format record
#         record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
#         if record.exc_info:  # for exceptions
#             record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
#         else:
#             record.exc_text = ""
#         """
#
#         # Insert the log record
#         try:
#             connection = sqlite3.connect(self.data_store.database_name)
#
#             cursor = connection.cursor()
#             cursor.execute("INSERT INTO log(timestamp, source, loglevel, loglevelname, message, args, module, funcname, lineno, exception, process, threadname) "
#                            "VALUES (:timestamp, :source, :loglevel, :loglevelname, :message, :args, :module, :funcname, :lineno, :exception, :process, :threadname)",
#                            { "timestamp": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))),
#                              "source": str(record.name),
#                              "loglevel": record.levelno,
#                              "loglevelname": str(record.levelname),
#                              "message": str(record.getMessage()),
#                              "args": str(record.args),
#                              "module": str(record.module),
#                              "funcname": str(record.funcName),
#                              "lineno": record.lineno,
#                              "exception": str(record.exc_text),
#                              "process": record.process,
#                              "threadname": str(record.threadName) })
#             connection.commit()
#             cursor.close()
#
#             connection.close()
#         except sqlite3.Error as e:
#             print("SqliteHandler: error occurred:", e.args[0])

# class Timer(Process):
#     def __init__(self, interval, function, args=[], kwargs={}):
#         super(Timer, self).__init__()
#         self.interval = interval
#         self.function = function
#         self.args = args
#         self.kwargs = kwargs
#         self.finished = Event()
#
#     def cancel(self):
#         print("cancel")
#         self.finished.set()
#         self.join()
#
#     def run(self):
#         self.finished.wait(self.interval)
#         if not self.finished.is_set():
#             self.function(*self.args, **self.kwargs)
#         self.finished.set()

class FileMode(Enum):
    READ = 0
    WRITE = 1


class FileDataStoreCacheThread:
    def __init__(self, problem, database_name, mode):
        self._should_continue = False
        self.is_running = False
        self.delay = 1.0
        self.timer = None

        self.problem = problem
        self.database_name = database_name
        self.mode = mode

        if not self.database_name:
            return

        self.db = SqliteDict(self.database_name, autocommit=True)
        if self.mode == FileMode.WRITE:
            # remove database and create structure
            if os.path.exists(self.database_name):
                self._create_structure()
        else:
            self._read_from_datastore()

        self.start()

    def _handle_target(self):
        self.is_running = True
        self.sync()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:
            self.timer = threading.Timer(self.delay, self._handle_target)
            self.timer.start()

    def _create_structure(self):
        self.db["name"] = self.problem.name
        self.db["description"] = self.problem.description
        self.db["parameters"] = self.problem.parameters
        self.db["costs"] = self.problem.costs

        self.db["populations"] = []

    def _read_from_datastore(self):
        self.problem.name = self.db["name"]
        self.problem.description = self.db["description"]
        self.problem.parameters = self.db["parameters"]
        self.problem.costs = self.db["costs"]

        self.populations = self.db["populations"]

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def cancel(self):
        if self.timer is not None:
            self._should_continue = False
            self.timer.cancel()

    def sync(self):
        if self.mode == FileMode.WRITE:
            if len(self.problem.populations) > 0:
                self.problem.logger.info("Caching to disk {} individuals.".format(0))

                self.db["populations"] = self.problem.populations


class FileDataStore:
    def __init__(self, problem, database_name=None, remove_existing=True, mode=FileMode.WRITE):
        if remove_existing and mode == "write":
            if os.path.exists(self.database_name):
                os.remove(self.database_name)

        # file cache
        self.file_cache = FileDataStoreCacheThread(problem, database_name, mode)

    def __del__(self):
        self.file_cache.sync()
        self.file_cache.cancel()

        del self.file_cache
        self.file_cache = None
