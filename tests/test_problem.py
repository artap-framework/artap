
from unittest import TestCase, main
from context import Function
from context import Problem
from context import ScipyNelderMead   
from scipy.optimize import minimize


class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.name = name
        self.id =  Problem.number
        Problem.number += 1
        
        self.max_population_number = 1
        self.max_population_size = 1
        self.vector_length = 1


class TestSimpleOptimization(TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_upper(self):
   
        problem = MyProblem("Kavadratic function")
        function = Function(1, 1)
        problem.set_function(function)
        problem.create_database()              #TODO: Move out.                   
        algorithm = ScipyNelderMead()
        algorithm.run(problem.evaluate, [10])        
        problem.read_from_database()
        optimum = problem.data[-1][-1] # Takes last individual
        self.assertAlmostEqual(optimum, 0)

if __name__ == '__main__':
    main()
    

