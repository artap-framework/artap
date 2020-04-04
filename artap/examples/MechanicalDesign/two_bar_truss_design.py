from artap.problem import Problem
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.results import Results, GraphicalResults

from math import inf
import matplotlib.pyplot as plt


class TwoBarTrussDesignProblem(Problem):
    """
    Example from K.DEb Multi-objective evolutionary optimization problems, Wiley, 2001.
    pp 432 - 433

    The truss has to carry a certain load without elastic failure. Thus, in addition to the objective of
    designing the truss for minimum volume, there are additional objectives of minimizing the stress in
    each of the two members AC and BC.


    The following two objactive optimization problem should be solved for the three variables:

    x1, x2 are horizontal varibales
    and y is the vertical

    Minimize
    --------

    f1 = x1*sqrt(16+y^2) + x2*sqrt(1+y**2)
    f2 = max(sigmaAC, sigmaBC)

    subject to
    ----------

    max(sigmaAC, sigmaBC) <= 1e5
    1<= x3 <= 3
    x1, x2 >= 0

    """
    def set(self):
        self.parameters = [{'name': 'x_1', 'bounds': [0.0, 0.01]},
                           {'name': 'x_2', 'bounds': [0.0, 0.1]},
                           {'name': 'y', 'bounds': [1.0, 3.0]}]
        self.costs = [{'name': 'F_1'},
                      {'name': 'F_2'}]

    def evaluate(self, individual):
        x = individual.vector

        f1 = x[0]*(16+x[2]**2.)**0.5 + x[1]*(1+x[2]**2.)**0.5

        sigmaAC = 20*(16+x[2]**2.)**0.5/(x[2]*x[0])
        sigmaBC = 80 * (1 + x[2] ** 2.) ** 0.5 / (x[2] * x[1])

        f2 = max(sigmaAC, sigmaBC)

        if f2 > 1e5:
            f2 = inf

        return [f1, f2]


problem = TwoBarTrussDesignProblem()
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 100
algorithm.options['max_population_size'] = 100
algorithm.run()

b = Results(problem)
solution = b.pareto_values()

print(solution)

# plot solution
plt.scatter([s[0] for s in solution],
            [s[1]*1e-3 for s in solution])
plt.xlim([0, 0.1])
plt.ylim([0, 100.])
plt.xlabel("Volume [m3]")
plt.ylabel("Maximum stress [MPa]")

# The values from the original solution
# Original solution of the task with the eps-contraint method
# original Palli et al, 1999
plt.scatter(0.004445, 89.983, c='red')
plt.annotate('   Red points are the original solutions from eps-constraint method', (0.004445, 89.983))
#plt.annotate('Original solution with eps-constraint method',(0.004833, 83.268))
plt.scatter(0.004833, 83.268, c='red')

plt.show()