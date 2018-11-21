import os
import unittest
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults


class TestDataStore(unittest.TestCase):

    def test_local_problem_data_store(self):
        database_file = "." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite"
        data_store = SqliteDataStore(database_file=database_file)
        problem = ProblemDataStore(data_store)
        results = GraphicalResults(problem)
        results.plot_all_individuals()


if __name__ == '__main__':
    unittest.main()
