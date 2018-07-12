from unittest import TestCase, main
from context import RemoteFunction
from context import Problem   
from scipy.optimize import minimize
import os

class TestRemoteOptimization(TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is performed on remote machine.
    """
    def test_remote_run(self):        
        """ Tests one calculation of goal function."""
        problem = Problem(1, 2, 2)
        function = RemoteFunction()       
        problem.set_function(function)        
        problem.create_database() # TODO: NotNecessary move into consructor    
        problem.evaluate([1, 1])
        problem.read_from_database()
        optimum = problem.data[-1][-1]                        

    def test_remote_optimization(self):        
        """ Tests simple optimization problem. """ 
        problem = Problem(1, 2, 2)
        function = RemoteFunction()       
        problem.set_function(function)        
        problem.create_database() # TODO: NotNecessary move into consructor    
        es = minimize(problem.evaluate, [10, 10], method='nelder-mead', options={'xatol': 1e-8, 'disp': True})        
        problem.read_from_database()
        optimum = problem.data[-1][-1]                
        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()