import unittest 
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore


class TestDataStore(unittest.TestCase):
    def test_local_problem_data_store(self):
        database_file = "./workspace/common_data/data.sqlite"
        data_store = SqliteDataStore(database_file=database_file)
        problem = ProblemDataStore(data_store)
        optimum = problem.populations[0].individuals[-1].costs[0]  # Takes last value of cost function
        self.assertLess(abs(optimum), 1e-4)
        

if __name__ == '__main__':
    unittest.main()
