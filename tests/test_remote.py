from unittest import TestCase, main
from context import RemoteExecutor
from context import Problem   
from context import ScipyNelderMead
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
        self.executor = RemoteExecutor(username="panek50")

        cwd = os.getcwd()
        self.executor.script = cwd + "/tests/eval.py"
        
        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        return self.executor.eval(x)
        
class TestRemoteOptimization(TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is performed on remote machine.
    """
    def test_remote_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("RemotePythonProblem")        
        problem.eval([1, 1])
        # problem.read_from_database()
        # optimum = problem.data[-1][-1]
        # self.assertAlmostEqual(optimum, 0)
    
    # def test_remote_optimization(self):        
    #     """ Tests simple optimization problem. """ 
    #     problem = TestProblem("Optimization_problem")
    #     function = RemoteFunction()       
    #     problem.set_function(function)        
    #     algorithm = ScipyNelderMead()
    #     algorithm.run(problem.evaluate, [10, 10])        
    #     problem.read_from_database()
    #     optimum = problem.data[-1][-1]                
    #     self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()