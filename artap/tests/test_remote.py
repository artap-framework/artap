import unittest
import os
import sys
import getpass

from scipy.optimize import minimize

from artap.executor import RemoteExecutor
from artap.problem import Problem   
from artap.algorithm_scipy import ScipyNelderMead
from artap.enviroment import Enviroment

class TestProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):        
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1': {'initial_value':10}, 
                           'x_2': {'initial_value':10}}
        self.costs = ['F1']
        
        if Enviroment.ssh_login == "":
            user = getpass.getuser()        
        else:
            user = Enviroment.ssh_login
        
        host = Enviroment.available_ssh_servers[0]
        host_working_directory = ""
        local_working_directory = ""

        self.executor = RemoteExecutor(username=user, hostname=host)
        self.executor.script = Enviroment.tests_root + "/remote.py"            
        
        
        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        result = self.executor.eval(x)        
        return result
        
class TestRemoteOptimization(unittest.TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is performed on remote machine.
    """
    def test_remote_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("RemotePythonProblem")        
        result = problem.eval([1, 2])
 
        self.assertAlmostEqual(result, 5.0)
    
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