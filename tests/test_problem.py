
from unittest import TestCase, main
from context import Function
from context import Problem
from context import ScipyNelderMead   
from scipy.optimize import minimize


class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        super().__init__(name)
        
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1', 10}
        self.costs = ['F_1']


class TestSimpleOptimization(TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_upper(self):
   
        problem = MyProblem("Kavadratic function")
        function = Function(1, 1)
        problem.set_function(function)        
        algorithm = ScipyNelderMead()
        algorithm.run(problem.evaluate, [10])        
        problem.read_from_database()
        optimum = problem.data[-1][-1] # Takes last individual
        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()
    

