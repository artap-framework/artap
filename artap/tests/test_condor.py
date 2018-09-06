from unittest import TestCase, main
import os
import getpass

from scipy.optimize import minimize

from artap.executor import CondorJobExecutor
from artap.problem import Problem   
from artap.enviroment import Enviroment

class TestProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):

        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1': {'initial_value':10}, 
                           'x_2': {'initial_value':10}}
        self.costs = ['F1']

        suplementary_files = ["remote.job", "remote.py"]

        # current username
        if Enviroment.condor_host_login == "":
            user = getpass.getuser()        
        else:
            user = Enviroment.condor_host_login
        # host        
        
        host = Enviroment.condor_host_ip

        self.executor = CondorJobExecutor(username=user, hostname=host, working_dir="./workspace/condor",
                                          suplementary_files = suplementary_files)
    
    def eval(self, x):
        result = self.executor.eval(x)
        return result

class TestCondor(TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is submitted as a job on HtCondor. 
    """
    def test_condor_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("Condor Problem")                     
        result = problem.eval([3, 2])                        
        

if __name__ == '__main__':
    main()