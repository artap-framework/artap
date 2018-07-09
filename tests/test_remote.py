from unittest import TestCase, main
from context import RemoteFunction
from context import Problem   
from scipy.optimize import minimize
import os

class TestRemoteOptimization(TestCase):

    def test_upper(self):        
    
        problem = Problem(1, 2, 2)
        function = RemoteFunction()       
        problem.set_function(function)        
        problem.create_database() # TODO: NotNecessary move into consructor    
        es = minimize(problem.evaluate, [10, 10], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
        problem.read_from_database()
        optimum = problem.data[-1][-1]                
        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()