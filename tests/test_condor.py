# from unittest import TestCase, main
# from context import RemoteFunction
# from context import Problem   
# from scipy.optimize import minimize
# import os

# class TestProblem(Problem):
#     """ Describe simple one obejctive optimization problem. """
#     def __init__(self, name):
#         self.name = name
#         self.id =  Problem.number
#         Problem.number += 1
        
#         self.max_population_number = 1
#         self.max_population_size = 1
#         self.vector_length = 2

# class TestCondor(TestCase):
#     """ Tests simple optimization problem where calculation of 
#         goal function is submitted as a job on HtCondor. 
#     """
#     def test_condor_run(self):        
#         """ Tests one calculation of goal function."""
#         problem = TestProblem("Condor Problem")
#         function = RemoteFunction()       
#         problem.set_function(function)        
#         problem.create_database() # TODO: NotNecessary move into consructor    
#         problem.evaluate([2, 1])
#         problem.read_from_database()
#         optimum = problem.data[-1][-1]                        
#         print(optimum)

# if __name__ == '__main__':
    # main()