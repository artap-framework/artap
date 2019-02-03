import os
import unittest
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults
# from artap.benchmark_functions import Rosenbrock


class TestDataStore(unittest.TestCase):

    def test_local_problem_data_store(self):
        working_dir = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep
        database_file = working_dir + "data.sqlite"
        data_store = SqliteDataStore(database_file=database_file)
        problem = ProblemDataStore(data_store, working_dir=working_dir)

        results = GraphicalResults(problem)
        results.plot_scatter('F_1', 'F_2')
        results.plot_individuals('F_1')


if __name__ == '__main__':
    unittest.main()
