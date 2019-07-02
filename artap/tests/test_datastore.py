import os
import unittest
from artap.problem import Problem, ProblemFileDataStore
from artap.datastore import FileDataStore
from artap.algorithm_nlopt import NLopt
from artap.algorithm_nlopt import LN_BOBYQA

from artap.results import Results
from artap.benchmark_functions import Booth

import tempfile


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10]},
                      'x_2': {'initial_value': 1.5, 'bounds': [-10, 10]}}
        costs = ['F']

        super().__init__(name, parameters, costs, working_dir=tempfile.mkdtemp())

    def evaluate(self, x):
        return [Booth.eval(x)]


# class TestDataStoreSqlite(unittest.TestCase):
#     def test_read_data_store(self):
#         database_name = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite"
#         problem = ProblemSqliteDataStore(database_name=database_name)
#
#         results = Results(problem)
#         optimum = results.find_minimum('F_1')
#         self.assertLessEqual(abs(optimum.costs[0]), 5)
#
#     def test_write_data_store(self):
#         problem = MyProblem("NLopt_BOBYQA")
#
#         # set datastore
#         database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".sqlite").name
#         problem.data_store = SqliteDataStore(problem, database_name=database_name)
#
#         algorithm = NLopt(problem)
#         algorithm.options['verbose_level'] = 0
#         algorithm.options['algorithm'] = LN_BOBYQA
#         algorithm.options['n_iterations'] = 10
#         algorithm.run()
#
#         results = Results(problem)
#         optimum = results.find_minimum('F')
#         self.assertAlmostEqual(optimum.costs[0], 1.854, 3)
#
#         # check db
#         connection = sqlite3.connect(database_name)
#         # connection.execute('pragma journal_mode=wal')
#
#         cursor = connection.cursor()
#         exec_cmd_data = "SELECT * FROM data"
#         data = cursor.execute(exec_cmd_data)
#
#         table = list()
#         for row in data:
#             table.append(row)
#
#         self.assertAlmostEqual(row[0], 10) # individual id
#         self.assertAlmostEqual(row[1], 1) # population id
#         self.assertAlmostEqual(row[4], 1.854, 3) # result
#
#         cursor.close()
#         connection.close()
#
#         # remove file
#         os.remove(database_name)


class TestDataStoreFile(unittest.TestCase):
    def test_read_data_store(self):
        database_name = "." + os.sep + "data" + os.sep + "data.db"
        problem = ProblemFileDataStore(database_name=database_name)

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum.costs[0], 1.854, 3)
        self.assertEqual(problem.name, 'NLopt_BOBYQA')
        self.assertEqual(problem.description, '')
        self.assertEqual(problem.parameters['x_1']['initial_value'], 2.5)
        self.assertEqual(problem.parameters['x_1']['bounds'][0], -10)
        self.assertEqual(problem.parameters['x_1']['bounds'][1], 10)
        self.assertEqual(problem.parameters['x_2']['initial_value'], 1.5)
        self.assertEqual(problem.parameters['x_2']['bounds'][0], -10)
        self.assertEqual(problem.parameters['x_2']['bounds'][1], 10)
        individual = problem.data_store.populations[0].individuals[6]
        self.assertAlmostEqual(individual.vector[0], 2.6989845414318134, 5)
        self.assertAlmostEqual(individual.vector[1], 1.83185007711266, 5)
        self.assertAlmostEqual(individual.costs[0], 5.378264283347013, 5)

    def test_write_data_store(self):
        problem = MyProblem("NLopt_BOBYQA")

        # set datastore
        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".db").name
        problem.data_store = FileDataStore(problem, database_name=database_name, mode="write")

        algorithm = NLopt(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['algorithm'] = LN_BOBYQA
        algorithm.options['n_iterations'] = 10
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum.costs[0], 1.854, 3)

        problem.data_store.db.close()

        # check db
        import shelve

        db = shelve.open(problem.data_store.database_name, flag='r')
        populations = db["populations"]

        self.assertAlmostEqual(populations[-1].individuals[9].costs[0], 1.854, 3) # result
        db.close()

        # remove file
        print(database_name)
        os.remove(database_name)


if __name__ == '__main__':
    unittest.main()
