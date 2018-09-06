import unittest 
from artap.enviroment import Enviroment
from artap.problem import Problem, ProblemDataStore 
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults

class TestDataStore(unittest.TestCase):
    def test_local_problem_datastore(self):         
        datastore = SqliteDataStore(new_database=False, problem_id=1)
        problem = ProblemDataStore(datastore)
        results = GraphicalResults(problem)
        results.plot_all_individuals()

if __name__ == '__main__':
    unittest.main()
    