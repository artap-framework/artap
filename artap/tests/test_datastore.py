import unittest 
from artap.enviroment import Enviroment
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore


class TestDataStore(unittest.TestCase):
    def test_local_problem_datastore(self):
        datastore = SqliteDataStore(new_database=False, problem_id=0)
        problem = ProblemDataStore(datastore)
        optimum = problem.populations[0].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, 0)
        
if __name__ == '__main__':
    unittest.main()
    