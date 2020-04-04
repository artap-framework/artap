.. index::
   single: Single objective unconstrained problem


Spyder - A Simple - single - objective optimization with Artap:
---------------------------------------------------------------

The role of this problem is to show the solution of a simple, well-known optimization problem in Artap.

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

---------------------------
Optimization with ScipyOpt
---------------------------

At first, we should import ScipyOpt through the wrapper functions into the optimization:

.. code-block:: python

    from artap.algorithm_scipy import ScipyOpt


Then instantiate ArtapProblem class, and select scipy-opt (an implementation of the Nelder-Mead algorithm) from the
wrapper class:

.. code-block:: python

    ### Optimization with Nelder-Mead
    problem_nlm = ArtapProblem()

    # set the optimization method
    algorithm_nlm = ScipyOpt(problem_nlm)
    algorithm_nlm.options['algorithm'] = 'Nelder-Mead'
    algorithm_nlm.options['tol'] = 1e-3
    algorithm_nlm.options['calculate_gradients'] = False

    # perform the optimization
    algorithm_nlm.run()


Every result of the optimization stored in Population class. We can export it or we can use the result class for
simple post processing of the results.

Here, we show, how can we use the Results class:

.. code-block:: python

    from artap.results import Results

Simply, we just instantiate a new class from the problem, and we can use the *find_minimum* method in the following way:

.. code-block:: python

    results_nlm = Results(problem_nlm)
    opt = results_nlm.find_minimum('F_1')

    print('The exact value of the optimization is at x_1 = 0.5')
    print('Optimal solution (Nelder-Mead):', opt)

    This function gives back (prints out), an individual type, which contains the optimal value of the parameter type (**0.5** is the theoretical optimum for **x** if **H=W=L=1**), the calculated value(s) of the goal function.

.. code-block:: python

    Optimal solution: vector: [0.500010763656608]; costs:[2.2360679775826897], front number: None crowding distance: 0


.. [CIT1] Gardner, M. "Mathematical Games: About Henry Ernest Dudeney, A Brilliant Creator of Puzzles." Sci. Amer. 198, 108-112, Jun. 1958.


------------------------------------------------------------
Automatically generated docummentation from the example file
------------------------------------------------------------

.. automodule:: artap.examples.single_objective_problem
    :members: