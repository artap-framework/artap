import os
import unittest
import tempfile
import time
import json
import sqlite3
import pathlib

from ..problem import Problem, ProblemViewDataStore
from ..individual import Individual
from ..datastore import TinyDataStore, SqliteDataStore
from ..algorithm_scipy import ScipyOpt
from ..algorithm_sweep import SweepAlgorithm
from ..algorithm_genetic import NSGAII

from ..operators import RandomGenerator

from sys import platform
if platform == "win32":
    __platform__ = 'WINDOWS'
else:
    __platform__ = 'Linux'


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "NLopt_BOBYQA"
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-10, 10]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [-10, 10]}]
        self.costs = [{'name': 'F', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        x_1 = individual.vector[0]
        x_2 = individual.vector[1]

        # set custom properties
        individual.custom["functions"] = [x_1**2, x_2**2]

        return [x_1**2 + x_2**2]


class TestDataStoreSqlite(unittest.TestCase):
    def test_read_write_database(self):
        problem = MyProblem()
        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = SqliteDataStore(problem, database_name=database_name)

        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 3
        algorithm.options['max_population_size'] = 4
        algorithm.options['max_processes'] = 4
        algorithm.run()

        # cache individuals
        individuals = {}
        for individual in problem.individuals:
            individuals[individual.id] = individual

        # remove datastore
        problem.data_store.destroy()

        # check json
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("SELECT * FROM individuals WHERE ID = ?", [list(individuals.keys())[6]])
        row = c.fetchall()
        individual = Individual.from_dict(json.loads(row[0][1]))

        # result
        self.assertAlmostEqual(individual.costs[0], individuals[individual.id].costs[0], 3)

        # remove file
        os.remove(database_name)

    def test_read_datastore(self):
        # Path to this script file location
        file_path = str(pathlib.Path(__file__).parent.absolute())
        database_name = os.path.join(file_path, "data/data.sqlite")
        problem = ProblemViewDataStore(database_name=database_name, class_datastore=SqliteDataStore)

        self.assertEqual(problem.name, 'NLopt_BOBYQA')

        individuals = problem.last_population()
        self.assertAlmostEqual(problem.parameters['x_1']['bounds'][0], -10)
        self.assertAlmostEqual(individuals[0].vector[1], 6.58962945, 4)
        self.assertAlmostEqual(individuals[1].vector[0], 1.8944488, 4)
        self.assertAlmostEqual(individuals[0].costs[0], 49.0245242, 4)


class TestDataStoreBenchmark(unittest.TestCase):
    def setUp(self):
        self.n = 300
        self.max_processes = 10

    def test_benchmark_sqlite_data_store(self):
        t_s = time.time()
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = SqliteDataStore(problem, database_name=database_name, thread_safe=(self.max_processes > 1))

        gen = RandomGenerator(problem.parameters)
        gen.init(self.n)

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.options['max_processes'] = self.max_processes
        algorithm.run()

        # cache individuals
        individuals = {}
        for individual in problem.individuals:
            individuals[individual.id] = individual

        # sync
        problem.data_store.destroy()

        t = time.time() - t_s
        problem.logger.info("write elapsed time: {} s, size: {} MB, n: {}".format(t, self.get_size(database_name) / 1024 / 1024, self.n))

        # check db
        t_s = time.time()
        # check

        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # c.execute("SELECT * FROM individuals WHERE ID = ?", [id])
        # row = c.fetchall()
        # individual = Individual.from_dict(json.loads(row[0][1]))
        c.execute("SELECT * FROM individuals;")
        rows = c.fetchall()
        for row in rows:
            individual = Individual.from_dict(json.loads(row[1]))
            self.assertAlmostEqual(individual.costs[0], individuals[individual.id].costs[0], 3)

        # remove file
        # print(database_name)
        os.remove(database_name)

        t = time.time() - t_s
        problem.logger.info("read elapsed time: {} s".format(t))

    def test_benchmark_tiny_data_store(self):
        t_s = time.time()
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".json").name
        problem.data_store = TinyDataStore(problem, database_name=database_name)

        gen = RandomGenerator(problem.parameters)
        gen.init(self.n)

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.options['max_processes'] = self.max_processes
        algorithm.run()

        # cache individuals
        individuals = {}
        for individual in problem.individuals:
            individuals[individual.id] = individual

        # sync
        problem.data_store.destroy()

        t = time.time() - t_s
        problem.logger.info("write elapsed time: {} s, size: {} MB, n: {}".format(t, self.get_size(database_name) / 1024 / 1024, self.n))

        # check db
        t_s = time.time()
        # check json
        with open(database_name) as json_file:
            data = json.load(json_file)
            for row in list(data['individuals'].values()):
                individual = Individual.from_dict(row)
                self.assertAlmostEqual(individual.costs[0], individuals[individual.id].costs[0], 3)

        # remove file
        # print(database_name)
        os.remove(database_name)

        t = time.time() - t_s
        problem.logger.info("read elapsed time: {} s".format(t))

    def get_size(self, start_path):
        if os.path.isfile(start_path):
            return os.path.getsize(start_path)
        else:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)

            return total_size


class TestDataStoreTiny(unittest.TestCase):
    def test_read_write_database(self):
        problem = MyProblem()
        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".json").name
        # database_name = 'data.json'
        problem.data_store = TinyDataStore(problem, database_name=database_name)

        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'CG'
        algorithm.options['tol'] = 1e-8
        algorithm.options['verbose_level'] = 0
        algorithm.run()

        # remove datastore
        problem.data_store.destroy()

        # check json
        with open(database_name) as json_file:
            data = json.load(json_file)
            individual = Individual.from_dict(list(data['individuals'].values())[-1])

            # result
            self.assertAlmostEqual(individual.costs[0], 0, 3)
            self.assertAlmostEqual(individual.custom["functions"][0], individual.vector[0]**2)

        # remove file
        os.remove(database_name)

    def test_read_datastore(self):
        # Path to this script file location
        file_path = str(pathlib.Path(__file__).parent.absolute())
        database_name = os.path.join(file_path, "data/data.json")
        problem = ProblemViewDataStore(database_name=database_name, class_datastore=TinyDataStore)

        self.assertEqual(problem.name, 'NLopt_BOBYQA')

        individuals = problem.last_population()
        self.assertAlmostEqual(individuals[0].vector[1], 1.5, 4)
        self.assertAlmostEqual(individuals[1].vector[0], 2.5, 4)
        self.assertAlmostEqual(individuals[0].costs[0], 8.5, 4)
        self.assertAlmostEqual(individuals[5].costs[0], 3.6308, 4)


if __name__ == '__main__':
    unittest.main()
