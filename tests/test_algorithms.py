
from unittest import TestCase, main
from context import Function
from context import Problem   
from scipy.optimize import minimize

class TestSimpleOptimization(TestCase):

    def test_upper(self):
        problem = Problem(1, 100, 1)
        function = Function(1, 1)
        problem.set_function(function)
        problem.create_database()
        es = minimize(problem.evaluate, [10], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
        problem.read_from_database()
        optimum = problem.data[-1][-1]
        self.assertAlmostEqual(optimum, 1)

if __name__ == '__main__':
    main()
    

