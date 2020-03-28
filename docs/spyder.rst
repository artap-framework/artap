.. index::
   single: Single objective unconstrained problem


Spyder - Simple unconstrained problem:
-----------------------------------------

A spider (*S*) sits in one corner of a cuboid room, measuring **H** by **W** by **L**, and a fly, (*F*), sits in the opposite
corner. By travelling on the surfaces of the room the, what is the shortest “straight line” distance from (*S*) to (*F*)?
The puzzle was originally posed in an English newspaper [CIT1]_.

.. image:: figures/spyder_fly.png
   :width: 400px
   :height: 200px
   :align: center

As it can be seen from the image, in this simple case, the problem can be formulated as a single objective, free optimization problem, where the task is to find the minimal value of *x*.

The following expression should be minimized:

.. math::

   \sqrt{x ^ 2 + H ^ 2} + \sqrt{(W - x)^2 + L^2}

It can be seen, this problem is convex, we can get the minima of this equation if :math:`x = W/2`.

-----------------------------
Problem definition in Artap
-----------------------------

To define an optimization task in artap, we should use the artaps' special **problem**  class.
Here the **evaluate** method have to be redefined by our objective function.
(In case of a constrained optimization task, also the evaluate_constraint function should be redefined)
This function calculates the value of your optimization function (invokes FEM solvers, if it's needed for the calculation).
It gets the the problem parameters from the **parameters** list (denoted by **x** in the code sample), where the bounds,
initial value of the parameters can be defined.
The **costs** list defines the list of the objective functions for artap. In this simple case we have a single objective (**F_1**)

Example code snippet:

.. code-block:: python

    class ArtapProblem(Problem):
        """ Defines the optimization problem """
        def __init__(self, name):

            # wall lengths
            self.H = 1.
            self.W = 1.
            self.L = 1.

            parameters = {'x': {'initial_value': 0.8,
                                'bounds': [0., self.W]}}
            costs = ['F_1']

            super().__init__(name, parameters, costs)

        def evaluate(self, x):
            function = (x[0] ** 2. + self.H ** 2.) ** 0.5 + ((self.W - x[0]) ** 2. + self.L ** 2.) ** 0.5
            return [function]


----------------------------------------------
Using Artaps' NSGA-II module for optimization
----------------------------------------------

We should import the following functions for the optimization:

.. code-block:: python

    from artap.algorithm_genetic import NSGAII
    from artap.results import Results


Then instantiate ArtapProblem class, and the NSGA-II algorithm, define the population number and the number population
size, before running the algorithm.

.. code-block:: python

    problem = ArtapProblem("Spyder on the wall")
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 50
    algorithm.run()


Every result of the optimization stored in a database. To find the optimal one of them, we have several possibilities.
Here, we show, how can we use the Results class:

.. code-block:: python

    from artap.results import Results

Simply, we just instantiate a new class from the problem, and we can use the *find_minimum* method in the following way:

.. code-block:: python

    results = Results(problem)
    optimum = results.find_minimum('F_1')

    print('Optimal solution (NSGA-II):', optimum)

This function gives back (prints out), an individual type, which contains the optimal value of the parameter type (**0.5** is the theoretical optimum for **x** if **H=W=L=1**), the calculated value(s) of the goal function.

.. code-block:: python

    Optimal solution (NSGA-II): vector: [0.500010763656608]; costs:[2.2360679775826897], front number: None crowding distance: 0


---------------------------------------------
Using Nealder-Mead algorithm for optimization
---------------------------------------------

You can use the built-in scipy based non-linear optimization tools, as well. For this, you have to import the following module from scipy:

.. code-block:: python

    from artap.algorithm_scipy import ScipyOpt

Then you can setup the optimization task on the following way:

.. code-block:: python

    problem_nlm = ArtapProblem("Spyder on the wall")
    algorithm_nlm = ScipyOpt(problem_nlm)
    algorithm_nlm.options['algorithm'] = 'Nelder-Mead'
    algorithm_nlm.options['tol'] = 1e-2
    algorithm_nlm.options['calculate_gradients'] = True
    algorithm_nlm.run()

    results_nlm = Results(problem_nlm)
    opt = results_nlm.find_minimum('F_1')

.. [CIT1] Gardner, M. "Mathematical Games: About Henry Ernest Dudeney, A Brilliant Creator of Puzzles." Sci. Amer. 198, 108-112, Jun. 1958.


------------------------------------------------------------
Automatically generated docummentation from the example file
------------------------------------------------------------

.. automodule:: artap.examples.single_objective_problem
    :members: