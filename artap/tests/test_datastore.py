import sqlite3
import os
import unittest
import shutil
from artap.problem import Problem, ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.algorithm_nlopt import NLopt
from artap.algorithm_nlopt import LN_BOBYQA

from artap.results import Results
from artap.benchmark_functions import Booth

import tempfile


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [-10, 10], 'precision': 1e-1}}
        costs = ['F']

        super().__init__(name, parameters, costs, working_dir=tempfile.mkdtemp())
        self.options['max_processes'] = 1

    def evaluate(self, x):
        return [Booth.eval(x)]


class TestDataStore(unittest.TestCase):
    def test_read_data_store(self):
        database_file = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite"
        data_store = SqliteDataStore(database_file=database_file)
        problem = ProblemDataStore(data_store)

        results = Results(problem)
        optimum = results.find_minimum('F_1')
        self.assertLessEqual(abs(optimum), 5)

    def xtest_write_data_store(self):
        # database_file = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite"
        problem = MyProblem("NLopt_BOBYQA")
        algorithm = NLopt(problem)
        algorithm.options['verbose_level'] = 0
        algorithm.options['algorithm'] = LN_BOBYQA
        algorithm.options['n_iterations'] = 10
        algorithm.run()

        results = Results(problem)
        optimum = results.find_minimum('F')
        self.assertAlmostEqual(optimum, 1.854, 3)

        # check db
        database_name = problem.working_dir + os.sep + "data" + ".sqlite"
        connection = sqlite3.connect(database_name)
        # connection.execute('pragma journal_mode=wal')

        cursor = connection.cursor()
        exec_cmd_data = "SELECT * FROM data"
        data = cursor.execute(exec_cmd_data)

        table = list()
        for row in data:
            table.append(row)

        self.assertAlmostEqual(row[0], 10) # individual id
        self.assertAlmostEqual(row[1], 1) # population id
        self.assertAlmostEqual(row[4], 1.854, 3) # result

        cursor.close()
        connection.close()

        # remove working_dir
        shutil.rmtree(problem.working_dir)

if __name__ == '__main__':
    unittest.main()
