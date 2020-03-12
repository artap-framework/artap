import os
import unittest
import tempfile
import time
from sqlitedict import SqliteDict

from artap.problem import Problem, ProblemViewDataStore
from artap.datastore import FileMode, FileDataStore
from artap.algorithm_scipy import ScipyOpt
from artap.algorithm_sweep import SweepAlgorithm

from artap.results import Results
from artap.operators import RandomGeneration, CustomGeneration

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


class TestDataStoreFile(unittest.TestCase):
    def test_read_write_database(self):
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = FileDataStore(problem, database_name=database_name)

        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'CG'
        algorithm.options['tol'] = 1e-8
        algorithm.options['verbose_level'] = 0
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum.costs[0], 0, 3)

        # remove datastore
        problem.data_store.destroy()

        # check db
        db = SqliteDict(database_name, autocommit=True)

        populations = db["populations"]

        individual = populations[-1].individuals[9]
        self.assertAlmostEqual(individual.costs[0], 0, 3) # result
        self.assertAlmostEqual(individual.custom["functions"][0], individual.vector[0]**2)
        db.close()

        # remove file
        # print(database_name)
        os.remove(database_name)

    def xtest_read_datastore(self):
        problem = MyProblem()

        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = FileDataStore(problem, database_name=database_name, mode=FileMode.REWRITE)

        gen = CustomGeneration(problem.parameters)
        gen.init([[1, 2], [3, 3]])

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.run()

        problem.data_store.destroy()

    def test_read_datastore(self):
        database_name = "data" + os.sep + "data.sqlite"
        problem = ProblemViewDataStore(database_name=database_name)

        self.assertEqual(problem.name, 'NLopt_BOBYQA')

        individuals = problem.populations[-1].individuals
        self.assertEqual(individuals[0].vector[0], 1)
        self.assertEqual(individuals[1].vector[1], 3)
        self.assertEqual(individuals[0].costs, [5])
        self.assertEqual(individuals[1].costs, [18])


class TestDataStoreFileBenchmark(unittest.TestCase):
    def setUp(self):
        self.n = 20000

    def test_benchmark_data_store(self):
        t_s = time.time()
        problem = MyProblem()

        # set data store
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
        problem.data_store = FileDataStore(problem, database_name=database_name)

        gen = RandomGeneration(problem.parameters)
        gen.init(self.n)

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.options['max_processes'] = 1
        algorithm.run()

        cost = problem.populations[0].individuals[int(self.n / 2)].costs[0]

        # sync
        problem.data_store.destroy()

        t = time.time() - t_s
        problem.logger.info("write elapsed time: {} s, size: {} MB, n: {}".format(t, self.get_size(database_name) / 1024 / 1024, self.n))

        # check db
        t_s = time.time()
        db = SqliteDict(database_name, autocommit=True)

        populations = db["populations"]

        self.assertEqual(len(populations[0].individuals), self.n)
        self.assertAlmostEqual(populations[0].individuals[int(self.n / 2)].costs[0], cost, 3)
        db.close()

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


if __name__ == '__main__':
    unittest.main()
