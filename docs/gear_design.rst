.. index::
   single: Multi-objective mechanical optimization problem with NSGA-II

Gear Design - Multi-objective mechanical design problem
=========================================================

This example shows, that how you can use Artap to solve a simple multi-objective optimization problem. The optimization
problem is inspired by a mechanical engineering problem and it is a general test problem for multi-objective optimization
solvers [DEB]_. The objective of the task is to find the optimal turn numbers of a gearbox gear's.
The gearbox contains for gears, the required gear ratio is 1/6.931, the number of the teeth have to be integer numbers,
therefor all of these four optimized variables must to be integers.

The optimized variables are represented by the following variable vector:

    x = (x1, x2, x3, x4) = (Td, Tb, Ta, Tf)

The problem can be formulated as a two variable optimization function. The first goal function's role is to minimize
the  error between the obtained and the realized gear ratio:

.. math::

    f_1 = (\frac{1.}{6.931} - \frac{x1 x2}{x3 x4} )^2.

where *x* is the solution vector, contains the number of the teeths, these numbers are strictly integers.
The second function has to be minimized:

.. math::
    f_2 = max(x1, x2, x3, x4)


subject to

    - x1 e [12, 60] strictly integer
    - x2 e [12, 60] strictly integer
    - x3 e [12, 60] strictly integer
    - x4 e [12, 60] strictly integer

The two extremal solutions from [DEB]_ to check the solution:

    - solution E : x = (12, 12, 27, 37); Calculation Error f1 = 1.83e-8; Max teeth number = 37
    - solution D : x = (12, 12, 13, 13); Calculation Error f1 = 5.01e-1; Max teeth number = 13


.. image:: figures/gear_design.png
   :width: 400px
   :align: center


The following code block defines the above described mathematical problem for Artap:

.. code-block:: python

    def set(self):

        # Not mandatory to give a name for the test problem
        self.name = 'Gear Design'

        # Defines x_1 and x_2, which are the optimized parameters
        # and the bounds 'defines' the constraints of the optimization problem
        # nsga -- ii algorithm doesn't need an initial value for the definition
        self.parameters = [{'name':'x1', 'bounds': [12, 60], 'parameter_type':'integer'},
                           {'name':'x2', 'bounds': [12, 60], 'parameter_type':'integer'},
                           {'name':'x3', 'bounds': [12, 60], 'parameter_type':'integer'},
                           {'name':'x4', 'bounds': [12, 60], 'parameter_type':'integer'}]

        # The two, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

    def evaluate(self, x):
        f1 = (1./6.931 - (x.vector[0]*x.vector[1])/(x.vector[2]*x.vector[3]))**2.
        f2 = max(x.vector)
        return [f1, f2]


The problem is solved by the NSGA-II algorithm of the *Algorithm* class on the maximum of 100 populations, which contains
100 individuals.

.. code-block:: python


    # Initialization of the problem
    problem = GearDesignProblem()

    # Perform the optimization iterating over 100 times on 100 individuals.
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()


Post - processing the results with the simple *Results* class and a simple plot with matpolib from the given Pareto-front.

.. code-block:: python

    b = Results(problem)
    # finding the pareto values
    solution = b.pareto_values()

    print(solution)

    # Plotting out the resulting hyperbola with matplotlib
    plt.scatter([s[0] for s in solution],
            [s[1] for s in solution])

    plt.xlabel("$f_1(x)$ - Error")
    plt.ylabel("$f_2(x)$ - Maximum size")

    plt.show()


References:

.. [DEB] Deb, K. (2001). Multi-objective optimization using evolutionary algorithms (Vol. 16). John Wiley & Sons.
