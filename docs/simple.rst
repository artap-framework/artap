.. index::
   single: Simple Multi-objective problem


Introducing the Artap's optimization interface on a simple example
------------------------------------------------------------------

The goal of this example to show, how we can use Artap to solve a simple, bi-objective optimization problem.

The problem is defiend by the following two objectives [GDE3]_:

.. math::

    f_1 = x_1

    f_2 = \frac{1+x_2}{x_1}

subject to

.. math::

    x_1 \in [0.1, 1]

    x_2 \in [0, 5]

The Pareto - front of the following problem is known, it is a simple  hyperbola.
This problem is very simple for an Evolutionary algorithm, it finds its solution within 20-30 generations.
In this example, we are using the built in NSGA  algorithm to solve this example.


The used modules contains the *NSGAII* algorithm, which is located in the *algorithm_genetic* class the *Problem* class,
which should be redefined with the description of the task and the *Results* class, which used for post processing.


.. code-block:: python

    from artap.problem import Problem
    from artap.algorithm_genetic import NSGAII,
    from artap.results import Results

    import matplotlib.pyplot as plt


The user only have to define a class for the problem, it is the *BiObjectiveTestProblem* class in our case.
The user has to redefine 4 inherited methods and functions from the *Problem* baseclass:

- the *name* of the problem
- define the optimized *parameters* with their bounds, in some cases (e.g. Nelder-Mead from scipyopt) the initial value, or the type of the parameter (integer) can be defined here.
- the *costs* function, it can be defined as a minimization and a maximization problem, as well.
- finally, the *evaluate()* function has to be redefined. This function realize the optimization task, it can invoke Agros as a Python script or run other commercial FEM solvers, as well to perform the calculatoins.

.. code-block:: python

    class BiObjectiveTestProblem(Problem):

    def set(self):
        # Not mandatory to give a name for the test problem
        self.name = 'Biobjective Test Problem'
        self.working_dir = '.'
        # Defines x_1 and x_2, which are the optimized parameters
        # and the bounds 'defines' the constraints of the optimization problem
        # nsga -- ii algorithm doesn't need an initial value for the definition
        self.parameters = [{'name': 'x1', 'bounds': [0.1, 1.]},
                           {'name': 'x2', 'bounds': [0.0, 5.0]}]

        # The two, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'f1', 'criteria': 'minimize'},
                      {'name': 'f2', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        # The individual.vector function contains the problem parameters in the appropriate (previously defined) order
        f1 = individual.vector[0]
        f2 = (1 + individual.vector[1]) / individual.vector[0]
        # individual.auxvar = [1.]
        return [f1, f2]


Now, our only task is to run() the defined optimization task. We have to tell the solver the *problem* and the *algorithm* variables.
*BiObjectiveTestProblem()* class set as a problem, the algorithm is NSGAII, where its parameters, the number of the maximum population and the population size is set.
Then we can run the calculation.

.. code-block:: python

    problem = BiObjectiveTestProblem()

    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

Every calculation result saved into the problem class during the calculation. It can be simply post-processed by the *Results* class, which contains simple functions for plotting the results
.. code-block:: python

    # Post - processing the results
    # reads in the result values into the b, results class
    b = Results(problem)
    b.pareto_values()

--------------------
Performance analysis
--------------------

There are some built-in performance indicator, which let it possible to compare the results with a reference.
In the following examples, we are calculating the additive unary epsilon indicator and the generational distances.
Firstly, we have to define a the reference solution, which is a list of the [(x, 1/x), ...] tuples in the given range.

Therefore, the reference function can be defined by the following list comprehension:

reference = [(0.1 + x * 4.9 / 1000, 1. / (0.1 + x * 4.9 / 1000)) for x in range(0, 1000)]

The unary epsilon indicator is the default function:
print('additive unary epsilon indicator:', b.performance_measure(reference))

The generational distance can be selected by the 'gd' type keyword.
print('generational distance:', b.performance_measure(reference, type='gd'))

----------
References
----------

.. [GDE3] The third Evolution Step of Generalized Differential Evolution Saku Kukkonen, Jouni Lampinen
