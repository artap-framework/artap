from unittest import TestCase, main
from context import ComsolFunction
from context import Problem   
from scipy.optimize import minimize

class TestSimpleComsolOptimization(TestCase):

    def test_upper(self):        
        import os
        curr_dir = os.path.abspath(os.curdir)
        input_file =curr_dir + "/tests/parameters.txt"
        output_file =curr_dir + "/tests/max.txt"
        model_file =  curr_dir + "/tests/elstat.java"
        problem = Problem(1, 2, 2)
        function = ComsolFunction(2, 1, input_file, output_file, model_file)
        problem.set_function(function)
        problem.create_database() # ToDo: NotNecessary move into consructor
        problem.evaluate([10, 10])
        problem.read_from_database()                
        optimum = problem.data[-1][-1]        
        self.assertAlmostEqual(optimum, 112.94090668383139)

if __name__ == '__main__':
    main()