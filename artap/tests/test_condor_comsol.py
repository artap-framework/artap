from unittest import TestCase, main
import getpass


from artap.executor import CondorJobExecutor
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

        suplementary_files = ["compile_and_run.sh"]

        # current username
        if Enviroment.condor_host_login == "":
            user = getpass.getuser()        
        else:
            user = Enviroment.condor_host_login
        # host        
        
        host = Enviroment.condor_host_ip

        self.executor = CondorJobExecutor(username=user, hostname=host, working_dir="./workspace/condor_comsol",
                                          suplementary_files = suplementary_files)
    
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
        result = problem.eval_batch([[5, 5], [2, 2], [3, 3]])
        print(result)

if __name__ == '__main__':
    main()
