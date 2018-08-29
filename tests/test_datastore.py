import unittest 
from context import Problem, ProblemDataStore, SqliteDataStore

class TestDataStore(unittest.TestCase):
    def test_local_problem_datastore(self):         
        datastore = SqliteDataStore("db.sqlite", "/home/karban/Projects/rdolab/artap/tests", False)                  
        problem = ProblemDataStore(datastore)

        optimum = problem.populations[-1].individuals[-1].costs[0] # Takes last cost function

        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    unittest.main()
    

