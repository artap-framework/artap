import os
import unittest
import tempfile
import time
from sqlitedict import SqliteDict

from artap.problem import Problem
from artap.datastore import FileDataStore
from artap.algorithm_scipy import ScipyOpt
from artap.algorithm_sweep import SweepAlgorithm

from artap.results import Results
from artap.operators import RandomGeneration

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
        return [x_1**2 + x_2**2]


class TestDataStoreFile(unittest.TestCase):
    def test_read_write_sqlitedict_data_store(self):
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = FileDataStore(problem, database_name=database_name, backend="sqlitedict", mode="write")
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'CG'
        algorithm.options['tol'] = 1e-8
        algorithm.options['verbose_level'] = 0
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum.costs[0], 0, 3)
        problem.data_store.db.close()

        # check db
        db = SqliteDict(database_name, autocommit=True)

        populations = db["populations"]

        self.assertAlmostEqual(populations[-1].individuals[9].costs[0], 0, 3) # result
        db.close()

        # remove file
        # print(database_name)
        os.remove(database_name)

    # @unittest.skipIf(__platform__ == "WINDOWS", "for Linux platform only")
    # def test_read_dbm_data_store(self):
    #     problem = Problem()
    #     results = Results(problem)
    #     database_name = "." + os.sep + "data" + os.sep + "data.db"
    #     problem.data_store = FileDataStore(problem, database_name=database_name, mode="read")
    #     optimum = results.find_minimum('F')
    #     self.assertAlmostEqual(optimum.costs[0], 0, 3)
    #     self.assertEqual(problem.name, 'NLopt_BOBYQA')
    #     self.assertEqual(problem.description, '')
    #     self.assertEqual(problem.parameters[0]['initial_value'], 2.5)
    #     self.assertEqual(problem.parameters[0]['bounds'][0], -10)
    #     self.assertEqual(problem.parameters[0]['bounds'][1], 10)
    #     self.assertEqual(problem.parameters[1]['initial_value'], 1.5)
    #     self.assertEqual(problem.parameters[1]['bounds'][0], -10)
    #     self.assertEqual(problem.parameters[1]['bounds'][1], 10)
    #     individual = problem.data_store.populations[0].individuals[-1]
    #     self.assertAlmostEqual(individual.vector[0], 0, 5)
    #     self.assertAlmostEqual(individual.vector[1], 0, 5)
    #     self.assertAlmostEqual(individual.costs[0], 0, 5)

    # @unittest.skipIf(__platform__ == "WINDOWS", "for Linux platform only")
    # def test_write_dbm_data_store(self):
    #     problem = MyProblem()
    #
    #     # set data store
    #     database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".db").name
    #     problem.data_store = FileDataStore(problem, database_name=database_name,  backend="shelve", mode="write")
    #
    #     algorithm = ScipyOpt(problem)
    #     algorithm.options['algorithm'] = 'CG'
    #     algorithm.options['tol'] = 1e-8
    #     algorithm.options['verbose_level'] = 0
    #     algorithm.options['n_iterations'] = 500
    #     algorithm.run()
    #
    #     results = Results(problem)
    #     optimum = results.find_minimum('F')
    #
    #     self.assertAlmostEqual(optimum.costs[0], 0, 3)
    #
    #     problem.data_store.db.close()
    #
    #     # check db
    #     import shelve
    #
    #     db = shelve.open(problem.data_store.database_name, flag='r')
    #     populations = db["populations"]
    #
    #     self.assertAlmostEqual(populations[-1].individuals[9].costs[0], 0, 3) # result
    #     db.close()
    #
    #     # remove file
    #     # print(database_name)
    #     os.remove(database_name)


class TestDataStoreFileBenchmark(unittest.TestCase):
    def setUp(self):
        self.n = 2000

    def test_benchmark_sqlitedict_data_store(self):
        backend = "sqlitedict"
        [problem, database_name, cost] = self.benchmark(backend)

        # check db
        t_s = time.time()
        db = SqliteDict(database_name, autocommit=True)

        populations = db["populations"]

        self.assertEqual(len(populations[0].individuals), self.n)
        self.assertAlmostEqual(problem.data_store.populations[0].individuals[int(self.n / 2)].costs[0], cost, 3)
        # print(populations[0].individuals[int(self.n / 2)])
        db.close()

        # remove file
        # print(database_name)
        os.remove(database_name)

        t = time.time() - t_s
        problem.logger.info("{}: read elapsed time: {} s".format(backend, t))

    # @unittest.skipIf(__platform__ == "WINDOWS", "for Linux platform only")
    # def test_benchmark_dbm_data_store(self):
    #     backend = "shelve"
    #     [problem, database_name, cost] = self.benchmark(backend)
    #
    #     # check db
    #     t_s = time.time()
    #     # check db
    #     import shelve
    #     db = shelve.open(problem.data_store.database_name, flag='r')
    #     populations = db["populations"]
    #
    #     self.assertEqual(len(populations[0].individuals), self.n)
    #     self.assertAlmostEqual(problem.data_store.populations[0].individuals[int(self.n / 2)].costs[0], cost, 3)
    #     # print(populations[0].individuals[int(self.n / 2)])
    #     db.close()
    #
    #     # remove file
    #     # print(database_name)
    #     os.remove(database_name)
    #
    #     t = time.time() - t_s
    #     problem.logger.info("{}: read elapsed time: {} s".format(backend, t))

    def benchmark(self, backend):
        t_s = time.time()
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".cache").name
        problem.data_store = FileDataStore(problem, database_name=database_name, backend=backend, mode="write")

        gen = RandomGeneration(problem.parameters)
        gen.init(self.n)

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.options['max_processes'] = 1
        algorithm.run()

        # print(problem.data_store.populations[0].individuals[int(self.n / 2)])
        cost = problem.data_store.populations[0].individuals[int(self.n / 2)].costs[0]

        problem.data_store.db.close()

        t = time.time() - t_s

        problem.logger.info("{}: write elapsed time: {} s, size: {} MB, n: {}".format(backend, t, self.get_size(database_name) / 1024 / 1024, self.n))

        return [problem, database_name, cost]

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


if __name__ == '__main__':
    unittest.main()
