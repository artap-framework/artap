from multiprocessing import Process, Event
from sqlitedict import SqliteDict
import os
import json
from .individual import Individual
from .population import Population
import shutil


class Timer(Process):
    def __init__(self, interval, function, args=None, kwargs=None):
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
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


class JsonDataStore:

    def __init__(self, problem, database_name, mode="write"):
        self.path = os.path.join(os.getcwd(), database_name)
        self.mode = mode
        self.problem = problem

        if mode == "write":
            if not os.path.exists(self.path):
                pass
            else:
                shutil.rmtree(self.path)
            os.makedirs(self.path)

        file_name = os.path.join(self.path, 'problem.json')
        data = json.dumps(problem.to_dict())
        with open(file_name, 'w') as file:
            file.write(data)

    def write(self, individual):
        file_name = os.path.join(self.path, str(individual.id) + '.json')
        with open(file_name,  'w') as file:
            individual_dict = individual.to_dict()
            data = json.dumps(individual_dict)
            file.write(data)

    def sync(self, individual):
        path = ""
        file_name = os.path.join(self.path, str(individual.id) + '.json')
        if os.path.exists(file_name):
            os.remove(file_name)

        if individual.population_id is not None:
            path = os.path.join(self.path, "population_{}".format(individual.population_id))
            if not os.path.exists(path):
                os.mkdir(path)
        else:
            path = self.path
        file_name = os.path.join(path, str(individual.id) + '.json')
        with open(file_name, 'w') as file:
            individual_dict = individual.to_dict()
            data = json.dumps(individual_dict)
            file.write(data)

    def read(self):
        self.problem.populations = []
        population = Population()

        for filename in os.listdir(self.path):
            if '.json' in filename:
                with open(os.path.join(self.path, filename), 'r') as file:
                    individual = Individual([])
                    individual.__dict__ = json.load(file)
                    population.individuals.append(individual)

    def destroy(self):
        pass


class FileDataStore:
    def __init__(self, problem, database_name, mode="write"):
        self._should_continue = False
        self.is_running = False

        self.problem = problem
        self.database_name = database_name
        self.mode = mode

        if not self.database_name:
            raise RuntimeError("FileDataStoreCacheThread: database name is empty.")

        elif self.mode == "write":
            if os.path.exists(database_name):
                os.remove(database_name)

        if self.mode == "write":
            self.db = SqliteDict(self.database_name, autocommit=True, flag='w')
            if os.path.exists(self.database_name):
                statinfo = os.stat(self.database_name)
                if statinfo.st_size == 0:
                    # raise RuntimeError("FileDataStoreCacheThread: database file already exists.
                    # Mode is WRITE (for automatic rewrite you can use REWRITE mode.")
                    self.read_from_datastore()
                else:
                    self._create_structure()
            else:
                self._create_structure()
        elif self.mode == "rewrite":
            self._create_structure()
        elif self.mode == "read":
            self.db = SqliteDict(self.database_name, flag='r')
            self.read_from_datastore()

        self.delay = 2.0
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
        if self.mode == "write" or self.mode == "rewrite":
            # print("sync: {} - {}".format(self.problem, len(self.problem.populations)))
            if len(self.problem.populations) > 0 and self.db.conn is not None:
                # print("SYNC - 3")
                self.problem.logger.info("Caching to disk {} populations.".format(len(self.problem.populations)))

                self.db["populations"] = self.problem.populations

    def write(self, individual):
        pass


class DummyDataStore:

    def __init__(self):
        pass

    def write(self, individuals):
        pass

    def sync(self, individuals):
        pass

    def destroy(self):
        pass
