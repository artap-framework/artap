import os
import unittest
import getpass

from artap.executor import RemoteExecutor
from artap.problem import Problem   
from artap.enviroment import Enviroment
from artap.datastore import DummyDataStore


class TestProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):        
        self.max_population_number = 1
        self.max_population_size = 1
        parameters = {'x_1': {'initial_value': 10},
                      'x_2': {'initial_value': 10}}
        costs = ['F1']

        super().__init__(name, parameters, costs, data_store=DummyDataStore(self))

        if Enviroment.ssh_login == "":
            user = getpass.getuser()
        else:
            user = Enviroment.ssh_login

        host = Enviroment.available_ssh_servers[0]
        self.executor = RemoteExecutor(username=user, hostname=host,
                                       working_dir="." + os.sep + "workspace" + os.sep + "remote",
                                       supplementary_files=["remote.py"])
        self.executor.script = Enviroment.tests_root + os.sep + "remote.py"

    def evaluate(self, x):
        result = self.executor.eval(x)        
        return [result]
        

class TestRemoteOptimization(unittest.TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is performed on remote machine.
    """
    def test_remote_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("RemotePythonProblem")        
        result = problem.evaluate([1, 2])
 
        self.assertAlmostEqual(result[0], 5.0)
    
    # def test_remote_optimization(self):        
    #     """ Tests simple optimization problem. """ 
    #     problem = TestProblem("RemotePythonProblem")
    #     algorithm = ScipyNelderMead(problem)
    #     algorithm.run()  
    #     problem.read_from_database()
    #     optimum = problem.data[-1][-1] # Takes last individual

    #     self.assertAlmostEqual(optimum, 0)


if __name__ == '__main__':
    unittest.main()
