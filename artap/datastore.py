import sqlite3

import os
import json

from .individual import Individual


class DummyDataStore:
    def __init__(self):
        pass

    def sync_individual(self, individuals):
        pass

    def sync_all(self):
        pass

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

        if self.mode == "write":
            if os.path.exists(self.database_name):
                statinfo = os.stat(self.database_name)
                if statinfo.st_size == 0:
                    self._create_structure()
                else:
                    self.read_from_datastore()
            else:
                self._create_structure()
        elif self.mode == "rewrite":
            if os.path.exists(database_name):
                os.remove(database_name)
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
            self.problem.parameters.append(parameter)

        # costs
        self.problem.costs.clear()
        c.execute(self.sql_costs_select)
        rows = c.fetchall()
        for row in rows:
            cost = json.loads(row[1])
            self.problem.costs.append(cost)

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
                self.sync_individual(individual)

    def sync_all(self):
        if self.mode == "write" or self.mode == "rewrite":
            conn = self.conn()
            c = conn.cursor()

            for individual in self.problem.individuals:
                c.execute(self.sql_individuals_upsert, [individual.id, json.dumps(individual.to_dict())])

            conn.commit()
