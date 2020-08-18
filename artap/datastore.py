from multiprocessing import Process, Event
import sqlite3
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import os
import json
import shutil

from .individual import Individual


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


class DummyDataStore:
    def __init__(self):
        pass

    def sync_individual(self, individuals):
        pass

    def destroy(self):
        pass


class JsonDataStore(DummyDataStore):
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

    def read(self):
        for filename in os.listdir(self.path):
            if '.json' in filename:
                with open(os.path.join(self.path, filename), 'r') as file:
                    individual = Individual([])
                    individual.__dict__ = json.load(file)
                    population.individuals.append(individual)

    def insert(self, individual):
        file_name = os.path.join(self.path, str(individual.id) + '.json')
        with open(file_name,  'w') as file:
            individual_dict = individual.to_dict()
            data = json.dumps(individual_dict)
            file.write(data)

    def update(self, individual):
        path = ""
        file_name = os.path.join(self.path, str(individual.id) + '.json')
        if os.path.exists(file_name):
            os.remove(file_name)

        if individual.population_id != -1:
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

    def destroy(self):
        pass


class SqliteDataStore(DummyDataStore):
    sql_main_table = "CREATE TABLE IF NOT EXISTS main (name text NOT NULL, description text NOT NULL);"
    sql_parameters_table = "CREATE TABLE IF NOT EXISTS parameters (name text PRIMARY KEY, parameter json not null);"
    sql_costs_table = "CREATE TABLE IF NOT EXISTS costs (name text PRIMARY KEY, cost json not null);"
    sql_individuals_table = "CREATE TABLE IF NOT EXISTS individuals (id int PRIMARY KEY, individual json not null);"

    sql_main_insert = "INSERT INTO main(name, description) VALUES (?,?)"
    sql_parameters_insert = "INSERT INTO parameters(name, parameter) VALUES (?,?)"
    sql_costs_insert = "INSERT INTO costs(name, cost) VALUES (?,?)"

    sql_individuals_upsert = "INSERT INTO individuals (id, individual) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET individual=excluded.individual;"

    sql_main_select = "SELECT * FROM main;"
    sql_parameters_select = "SELECT * FROM parameters;"
    sql_costs_select = "SELECT * FROM costs;"
    sql_individuals_select = "SELECT * FROM individuals;"
    # SELECT json_extract(individual, '$.costs[0]') as cost FROM individuals where cost>10;

    def __init__(self, problem, database_name, mode="write", thread_safe=True):
        self.problem = problem
        self.database_name = database_name
        self.mode = mode
        self.thread_safe = thread_safe
        # cache
        self._conn = None

        if not self.database_name:
            raise RuntimeError("SqliteDataStoreCacheThread: database name is empty.")

        elif self.mode == "write":
            if os.path.exists(database_name):
                os.remove(database_name)

        if self.mode == "write":
            if os.path.exists(self.database_name):
                statinfo = os.stat(self.database_name)
                if statinfo.st_size == 0:
                    self.read_from_datastore()
                else:
                    self._create_structure()
            else:
                self._create_structure()
        elif self.mode == "rewrite":
            self._create_structure()
        elif self.mode == "read":
            self.read_from_datastore()

    def conn(self):
        if self.thread_safe:
            try:
                if self.mode == "write":
                    conn = sqlite3.connect(self.database_name, isolation_level='Exclusive')
                    c = conn.cursor()
                    c.execute('PRAGMA synchronous = 0')
                    c.execute('PRAGMA journal_mode = ON')
                    conn.commit()
                else:
                    conn = sqlite3.connect(self.database_name)
            except sqlite3.Error as e:
                print(e)

            return conn
        else:
            if self._conn is None:
                try:
                    if self.mode == "write":
                        self._conn = sqlite3.connect(self.database_name, isolation_level='Exclusive')
                        c = self._conn.cursor()
                        c.execute('PRAGMA synchronous = 0')
                        c.execute('PRAGMA journal_mode = OFF')
                        self._conn.commit()
                    else:
                        self._conn = sqlite3.connect(self.database_name)
                except sqlite3.Error as e:
                    print(e)

            return self._conn

    def _create_structure(self):
        conn = self.conn()
        c = conn.cursor()

        # structure
        c.execute(self.sql_main_table)
        c.execute(self.sql_costs_table)
        c.execute(self.sql_parameters_table)
        c.execute(self.sql_individuals_table)
        conn.commit()

        # data
        c.execute(self.sql_main_insert, [self.problem.name, self.problem.description])
        for parameter in self.problem.parameters:
            c.execute(self.sql_parameters_insert, [parameter["name"], json.dumps(parameter)])
        for cost in self.problem.costs:
            c.execute(self.sql_costs_insert, [cost["name"], json.dumps(cost)])
        conn.commit()

    def read_from_datastore(self):
        conn = self.conn()
        c = conn.cursor()

        c.execute(self.sql_main_select)
        rows = c.fetchall()

        # main
        self.problem.name = rows[0][0]
        self.problem.description = rows[0][1]

        # parameters
        self.problem.parameters.clear()
        c.execute(self.sql_parameters_select)
        rows = c.fetchall()
        for row in rows:
            parameter = json.loads(row[1])
            self.problem.parameters[parameter["name"]] = parameter

        # costs
        self.problem.costs.clear()
        c.execute(self.sql_costs_select)
        rows = c.fetchall()
        for row in rows:
            cost = json.loads(row[1])
            self.problem.costs[cost["name"]] = cost

        # individuals
        self.problem.individuals.clear()
        c.execute(self.sql_individuals_select)
        rows = c.fetchall()
        for row in rows:
            individual = Individual.from_dict(json.loads(row[1]))
            self.problem.individuals.append(individual)

    def destroy(self):
        if self._conn is not None:
            self._conn.close()

    def sync_individual(self, individual):
        if self.mode == "write" or self.mode == "rewrite":
            conn = self.conn()
            c = conn.cursor()

            # data
            try:
                c.execute(self.sql_individuals_upsert, [individual.id, json.dumps(individual.to_dict())])
                conn.commit()
            except sqlite3.OperationalError as e:
                # try again
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ERROR")
                self.sync_individual(individual)


class TinyDataStore(DummyDataStore):
    def __init__(self, problem, database_name, mode="write"):
        self.problem = problem
        self.database_name = database_name
        self.mode = mode

        if not self.database_name:
            raise RuntimeError("TinyDataStoreCacheThread: database name is empty.")

        elif self.mode == "write":
            if os.path.exists(database_name):
                os.remove(database_name)

        if self.mode == "write":
            # self.db = TinyDB(self.database_name)
            # self.db = TinyDB(storage=MemoryStorage)
            self.db = TinyDB(self.database_name, storage=CachingMiddleware(JSONStorage))
            # sort_keys=True, indent=4

            if os.path.exists(self.database_name):
                statinfo = os.stat(self.database_name)
                if statinfo.st_size == 0:
                    # raise RuntimeError("TinyDataStoreCacheThread: database file already exists.
                    # Mode is WRITE (for automatic rewrite you can use REWRITE mode.")
                    self._create_structure()
                else:
                    self.read_from_datastore()
            else:
                self._create_structure()
        elif self.mode == "rewrite":
            self._create_structure()
        elif self.mode == "read":
            self.db = TinyDB(self.database_name)
            self.read_from_datastore()

    def _create_structure(self):
        main = self.db.table('main')
        main.insert({'name': self.problem.name,
                     'description': self.problem.description})
        main.insert({'parameters': self.problem.parameters})
        main.insert({'costs': self.problem.costs})

        individuals = self.db.table('individuals')

    def read_from_datastore(self):
        main = self.db.table('main')
        main_all = main.all()
        self.problem.name = main_all[0]["name"]
        self.problem.description = main_all[0]["description"]
        self.problem.parameters = main_all[1]["parameters"]
        self.problem.costs = main_all[2]["costs"]

        individuals = self.db.table('individuals')
        individuals_all = individuals.all()
        for data in individuals_all:
            individual = Individual()
            self.problem.individuals.append(Individual.from_dict(data))

    def sync_individual(self, individual):
        individuals = self.db.table('individuals')
        individual_query = Query()
        individuals.upsert(individual.to_dict(), individual_query.id == individual.id)

    def destroy(self):
        self.db.close()
