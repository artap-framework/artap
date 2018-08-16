from unittest import TestCase, main
from context import CondorJobExecutor
from context import Problem   
from scipy.optimize import minimize
import os

class TestProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):

        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1': {'initial_value':10}, 
                           'x_2': {'initial_value':10}}
        self.costs = ['F1']

        # current username
        user = getpass.getuser()        
        # host        
        host = "localhost"
        self.executor = CondorJobExecutor(username=user, hostname=host)
    
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
        print(result)

if __name__ == '__main__':
    main()