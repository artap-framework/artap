import unittest 
from artap.enviroment import Enviroment
from artap.problem import Problem, ProblemDataStore 
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults

class TestDataStore(unittest.TestCase):
    def test_local_problem_datastore(self):         
        datastore = SqliteDataStore(working_dir = Enviroment.tests_root, structure = False, filename="datastore.sqlite")                  
        problem = ProblemDataStore(datastore)
        results = GraphicalResults(problem)
        results.plot_all_individuals()

if __name__ == '__main__':
    unittest.main()
    