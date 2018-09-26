import unittest 
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults


class TestDataStore(unittest.TestCase):

    def test_local_problem_data_store(self):
        data_store = SqliteDataStore(new_database=False, problem_id=1)
        problem = ProblemDataStore(data_store)
        results = GraphicalResults(problem)
        results.plot_all_individuals()


if __name__ == '__main__':
    unittest.main()
