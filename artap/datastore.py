from multiprocessing import Process, Event
import os
import time
from enum import Enum
from sqlitedict import SqliteDict


class Timer(Process):
    def __init__(self, interval, function, args=[], kwargs={}):
        super(Timer, self).__init__(*args, **kwargs)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

        self.daemon = True

    def cancel(self):
        self.finished.set()

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
        self.finished.set()


class FileMode(Enum):
    READ = 0
    WRITE = 1
    REWRITE = 2


class FileDataStore:
    def __init__(self, problem, database_name, mode=FileMode.WRITE):
        self._should_continue = False
        self.is_running = False

        self.problem = problem
        self.database_name = database_name
        self.mode = mode

        if not self.database_name:
            raise RuntimeError("FileDataStoreCacheThread: database name is empty.")

        elif self.mode == FileMode.REWRITE:
            if os.path.exists(database_name):
                os.remove(database_name)

        self.db = SqliteDict(self.database_name, autocommit=True)
        if self.mode == FileMode.WRITE:
            if os.path.exists(self.database_name):
                statinfo = os.stat(self.database_name)
                if statinfo.st_size == 0:
                    # raise RuntimeError("FileDataStoreCacheThread: database file already exists. Mode is WRITE (for automatic rewrite you can use REWRITE mode.")
                    self.read_from_datastore()
                else:
                    self._create_structure()
            else:
                self._create_structure()
        elif self.mode == FileMode.REWRITE:
            self._create_structure()
        elif self.mode == FileMode.READ:
            self.read_from_datastore()

        self.delay = 5.0
        self.start()

    def _handle_target(self):
        self.is_running = True
        self.sync()
        self.is_running = False

    def _start_timer(self):
        if self._should_continue:
            # if self.timer is not None:
            #     self.timer.cancel()
            #     del self.timer
            #     self.timer = None
            timer = Timer(self.delay, self._handle_target)
            timer.start()

    def _create_structure(self):
        self.db["name"] = self.problem.name
        self.db["description"] = self.problem.description
        self.db["parameters"] = self.problem.parameters
        self.db["costs"] = self.problem.costs

        self.db["populations"] = []

    def read_from_datastore(self):
        self.problem.name = self.db["name"]
        self.problem.description = self.db["description"]
        self.problem.parameters = self.db["parameters"]
        self.problem.costs = self.db["costs"]

        self.problem.populations = self.db["populations"]

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def destroy(self):
        self._should_continue = False

        self.sync()
        self.db.close()

    def sync(self):
        if self.mode == FileMode.WRITE or self.mode == FileMode.REWRITE:
            if len(self.problem.populations) > 0 and self.db.conn is not None:
                self.problem.logger.info("Caching to disk {} populations.".format(len(self.problem.populations)))

                self.db["populations"] = self.problem.populations
