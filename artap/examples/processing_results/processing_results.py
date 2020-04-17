from artap.problem import Problem
from artap.algorithm_genetic import NSGAII
from artap.results import Results


class BiObjectiveTestProblem(Problem):
    """

    """
    def set(self):
        # Not mandatory to give a name for the test problem
        self.name = 'Biobjective Test Problem'
        self.working_dir = '.'
        # Defines x_1 and x_2, which are the optimized parameters
        # and the bounds 'defines' the constraints of the optimization problem
        # nsga -- ii algorithm doesn't need an initial value for the definition
        self.parameters = [{'name': 'x_1', 'bounds': [-1.0, 1.]},
                           {'name': 'x_2', 'bounds': [-1.0, 5.0]}]

        # The two, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'},
                      {'name': 'F_2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        # The individual.vector function contains the problem parameters in the appropriate (previously defined) order
        x1 = individual.vector[0]
        x2 = individual.vector[1]
        f1 = 4 * pow(x1, 2) + 4 * pow(x2, 2)
        f2 = pow(x1 - 5, 2) + pow(x2 - 5, 2)
        return [f1, f2]


# Initialization of the problem
problem = BiObjectiveTestProblem()

# Perform the optimization iterating over 100 times on 100 individuals.
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 100
algorithm.run()

# Post - processing the results
# reads in the result values into the b, results class
results = Results(problem)

slice = results.pareto_front()
import pylab as plt
plt.plot(slice[0], slice[1], 'x')
plt.show()
