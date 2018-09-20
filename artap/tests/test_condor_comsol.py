from unittest import TestCase, main
import getpass
import os

from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem   
from artap.enviroment import Enviroment



class TestProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'a': {'initial_value':10},
                           'b': {'initial_value':10}}
        self.costs = ['F1']

        output_file = "max.txt"
        model_file = "elstat.mph"

        # current username
        if Enviroment.condor_host_login == "":
            user = getpass.getuser()        
        else:
            user = Enviroment.condor_host_login
        # host        
        
        host = Enviroment.condor_host_ip

        self.executor = CondorComsolJobExecutor(self.parameters, model_file, output_file,
                                          username=user, hostname=host, working_dir="./workspace/condor_comsol")
    
    def eval(self, x):
        result = self.executor.eval(x)
        return result

    def eval_batch(self, table):
        result = self.executor.eval_batch(table)
        return result

class TestCondor(TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is submitted as a job on HtCondor. 
    """
    def test_condor_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("Condor Comsol Problem")
        result = problem.eval_batch([[5, 4], [2, 1], [3, 2]])
        print(result)

if __name__ == '__main__':
    main()
