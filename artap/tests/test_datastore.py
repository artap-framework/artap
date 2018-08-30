import unittest 
from artap.enviroment import Enviroment
from artap.problem import Problem, ProblemDataStore 
from artap.datastore import SqliteDataStore

class TestDataStore(unittest.TestCase):
    def test_local_problem_datastore(self):         
        datastore = SqliteDataStore(working_dir = Enviroment.tests_root, structure = False, filename="datastore.sqlite")                  
        problem = ProblemDataStore(datastore)
        optimum = problem.populations[0].individuals[-1].costs[0] # Takes last cost function
        self.assertAlmostEqual(optimum, 0)
        print(Enviroment.condor_host_ip)

if __name__ == '__main__':
    unittest.main()
    