.. index::
   single: Multi-objective mechanical optimization problem with NSGA-II


Two Bar Truss Design - Multi-objective mechanical design problem
================================================================

This example shows, that how you can use Artap to solve a simple multi-objective optimization problem. The optimization
problem is inspired by a mechanical engineering problem and it is a general test problem for multi-objective optimization
solvers [DEB]_.


.. image:: figures/two_bar.png
   :width: 400px
   :align: center


The truss has to carry a certain load without elastic failure. Thus, in addition to the objective of designing the
truss for minimum volume, there are additional objectives of minimizing the stress in each of the two members AC and BC.


The following two objactive optimization problem should be solved for the three variables:

- *x1*, *x2* are horizontal variables
- *y* is the vertical

The objectives:
----------------

.. math::

    f_1 = x_1 \sqrt{16+y^2} + x_2 \sqrt{1+y^2}

    f_2 = max(\sigma_{AC}, \sigma_{BC})

subject to
----------

.. math::

    max(\sigma_{AC}, \sigma_{BC}) <= 1e5

    1<= x3 <= 3

    x_1, x_2 >= 0

The following code block defines the above described mathematical problem for Artap:

.. code-block:: python

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



The problem is solved by the NSGA-II algorithm of the *Algorithm* class on the maximum of 100 populations, which contains
100 individuals.

.. code-block:: python

    problem = TwoBarTrussDesignProblem()
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

Post - processing the results with the simple *Results* class and a simple plot with matpolib from the given Pareto-front.

.. code-block:: python

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
    plt.scatter(0.004833, 83.268, c='red')

    plt.show()

References:

.. [DEB] Deb, K. (2001). Multi-objective optimization using evolutionary algorithms (Vol. 16). John Wiley & Sons. pp 432 - 433
