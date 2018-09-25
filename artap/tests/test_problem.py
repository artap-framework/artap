import unittest 
from artap.problem import Problem
from artap.algorithm_scipy import ScipyNelderMead   


class MyProblem(Problem):
    """ Describe simple one obejctive optimization problem. """
    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1
        self.parameters = {'x_1': {'initial_value': 10}}
        self.costs = ['F_1']

        super().__init__(name, self.parameters, self.costs)

    def eval(self, x):
        result = 0
        for i in x:
            result += i*i   

        return result


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""
    
    def test_local_problem(self):           
        problem = MyProblem("LocalPythonProblem")
        algorithm = ScipyNelderMead(problem)
        algorithm.run()                
        optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function
        self.assertAlmostEqual(optimum, 0)


if __name__ == '__main__':
    unittest.main()
