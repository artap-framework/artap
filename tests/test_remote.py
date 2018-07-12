from unittest import TestCase, main
from context import RemoteFunction
from context import Problem   
from context import ScipyNelderMead
from scipy.optimize import minimize
import os

class TestProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.name = name
        self.id =  Problem.number
        Problem.number += 1
        
        self.max_population_number = 1
        self.max_population_size = 1
        self.vector_length = 2

class TestRemoteOptimization(TestCase):
    """ Tests simple optimization problem where calculation of 
        goal function is performed on remote machine.
    """
    def test_remote_run(self):        
        """ Tests one calculation of goal function."""
        problem = TestProblem("Run Problem")        
        function = RemoteFunction()       
        problem.set_function(function)        
        problem.create_database() # TODO: NotNecessary move into consructor    
        problem.evaluate([1, 1])
        problem.read_from_database()
        # optimum = problem.data[-1][-1]
        # self.assertAlmostEqual(optimum, 0)

    def test_remote_optimization(self):        
        """ Tests simple optimization problem. """ 
        problem = TestProblem("Optimization problem")
        function = RemoteFunction()       
        problem.set_function(function)        
        problem.create_database() # TODO: NotNecessary move into consructor    
        algorithm = ScipyNelderMead()
        algorithm.run(problem.evaluate, [10, 10])        
        problem.read_from_database()
        optimum = problem.data[-1][-1]                
        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()