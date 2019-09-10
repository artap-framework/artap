"""
This example shows how to use Artap to solve a simple mathematical, single objective optimization problem.
The understanding of this problem doesn't need any physical knowledge.

Problem:
--------

A spyder, S, sits in one corner of a cuboid room, measuring 'H' by 'W' by 'L', and a fly, F, sits in the opposite
corner. By travelling on the surfaces of the room the, what is the shortest “straight line” distance from S to F?

The problem formulated as a single optimization problem, free optimization problem (without constraints)

Problem parameters are the edges of the cuboid: H, W, L
"""

from artap.problem import Problem
from artap.results import Results
from artap.algorithm_scipy import ScipyOpt

# wall lengths defined as global parameters
H = 1.
W = 1.
L = 1.

class ArtapProblem(Problem):
    """
    The solution of this problem needs to find the minimum of a one parametered (x_1) goal function.
    The problem solved, by the Nelder-Mead method, therefore an initial value has to be defined, anyway it is set to 0.
    """

    def set(self):

        self.name = "spyder on the wall"
        self.parameters = [{'name': 'x_1', 'initial_value':0.1, 'bounds': [0.0, 0.9]}]
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        # this function should be rewritten to define the optimization task
        # every individual contains a vector of parameters, which contains the previously defined problem parameters
        # in the given order
        x = individual.vector

        # the goal function
        F1 = (x[0] ** 2. + H ** 2.) ** 0.5 + ((W - x[0]) ** 2. + L ** 2.) ** 0.5

        # the evaluate function should give back a list of the calculated objective values, following the defined
        # order in set(Problem) in this case --> ['F1']
        return [F1]

### Optimization with Nelder-Mead
problem_nlm = ArtapProblem()

# set the optimization method
algorithm_nlm = ScipyOpt(problem_nlm)
algorithm_nlm.options['algorithm'] = 'Nelder-Mead'
algorithm_nlm.options['tol'] = 1e-3
algorithm_nlm.options['calculate_gradients'] = False

# perform the optimization
algorithm_nlm.run()

results_nlm = Results(problem_nlm)
opt = results_nlm.find_minimum('F_1')

print('The exact value of the optimization is at x_1 = 0.5')
print('Optimal solution (Nelder-Mead):', opt)
