from unittest import TestCase, main
from context import ComsolFunction
from context import Problem   
from scipy.optimize import minimize


class TestProblem(Problem):

    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1':10, 'x_2':10}
        self.costs = ['F_1']
        super().__init__(name, self.parameters, self.costs)

class TestSimpleComsolOptimization(TestCase):

    def test_upper(self):        
        import os
        curr_dir = os.path.abspath(os.curdir)
        input_file =curr_dir + "/tests/parameters.txt"
        output_file =curr_dir + "/tests/max.txt"
        model_file =  curr_dir + "/tests/elstat.java"
        problem = TestProblem("Comsol_Problem")
        function = ComsolFunction(2, 1, input_file, output_file, model_file)
        problem.set_function(function)        
        problem.evaluate([10, 10])
        problem.read_from_database()                
        optimum = problem.data[-1][-1]        
        self.assertAlmostEqual(optimum, 112.94090668383139)

if __name__ == '__main__':
    main()