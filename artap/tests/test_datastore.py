import os
import unittest
from artap.problem import Problem
from artap.datastore import FileDataStore
from artap.algorithm_scipy import ScipyOpt

from artap.results import Results
from artap.config import artap_root

import tempfile


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

    def test_read_dbm_data_store(self):
        problem = Problem()
        results = Results(problem)
        database_name = "." + os.sep + "data" + os.sep + "data.db"
        problem.data_store = FileDataStore(problem, database_name=database_name, mode="read")
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum.costs[0], 0, 3)
        self.assertEqual(problem.name, 'NLopt_BOBYQA')
        self.assertEqual(problem.description, '')
        self.assertEqual(problem.parameters[0]['initial_value'], 2.5)
        self.assertEqual(problem.parameters[0]['bounds'][0], -10)
        self.assertEqual(problem.parameters[0]['bounds'][1], 10)
        self.assertEqual(problem.parameters[1]['initial_value'], 1.5)
        self.assertEqual(problem.parameters[1]['bounds'][0], -10)
        self.assertEqual(problem.parameters[1]['bounds'][1], 10)
        individual = problem.data_store.populations[0].individuals[-1]
        self.assertAlmostEqual(individual.vector[0], 0, 5)
        self.assertAlmostEqual(individual.vector[1], 0, 5)
        self.assertAlmostEqual(individual.costs[0], 0, 5)

    def test_write_dbm_data_store(self):
        problem = MyProblem()

        # set data store

        database_name = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=None, suffix=".db").name
        problem.data_store = FileDataStore(problem, database_name=database_name,  backend="shelve", mode="write")
        algorithm = ScipyOpt(problem)
        algorithm.options['algorithm'] = 'CG'
        algorithm.options['tol'] = 1e-8
        algorithm.options['verbose_level'] = 0
        algorithm.options['n_iterations'] = 500
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')

        self.assertAlmostEqual(optimum.costs[0], 0, 3)

        problem.data_store.db.close()

        # check db
        import shelve

        db = shelve.open(problem.data_store.database_name, flag='r')
        populations = db["populations"]

        self.assertAlmostEqual(populations[-1].individuals[9].costs[0], 0, 3) # result
        db.close()

        # remove file
        # print(database_name)
        os.remove(database_name)

    def test_write_sqlitedict_data_store(self):
        problem = MyProblem()
        print(artap_root)
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
        import sys
        sys.path.append(artap_root + os.sep + "3rdparty" + os.sep + "sqlitedict")

        from sqlitedict import SqliteDict

        db = SqliteDict(database_name, autocommit=True)

        populations = db["populations"]

        self.assertAlmostEqual(populations[-1].individuals[9].costs[0], 0, 3) # result
        db.close()

        # remove file
        # print(database_name)
        os.remove(database_name)


if __name__ == '__main__':
    unittest.main()
