.. _chap_algorithms:

************
Algorithms
************

Non dominated sorting genetic algorithm (NSGA-II)
==========
NSGA-II is a well-known, elite, and fast sorting multi-objective genetic algorithm. It is introduced by [Deb2002].
NSGA-II generates offspring utilizing a specific form of crossover and mutation, then chooses the next generation
based on nondominated sorting and crowding distance comparison.

The non-dominated sorting is done first. Then, optimization starts by computing and updating pareto dominance, and
crowding distance.

EXAMPLE:
----------

    .. code-block::
        import pylab as plt
        import numpy as np
        from artap.problem import Problem
        from artap.results import Results
        from artap.algorithm_genetic import NSGAII
        from artap.benchmark_functions import Sphere

        # Initialization of the problem
        problem = Sphere(**{'dimension': 1})

        # Perform the optimization iterating over 100 times on 100 individuals.
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        # Post - processing the results
        # reads in the result values into the b, results class
        results = Results(problem)
        pareto = results.pareto_values()



CMA_ES
==========
The Covariance Matrix Adaptation Evolution Strategy (CMA-ES) [Hansen2001] is one of the most effective approaches
for black-box optimization, in which objective functions cannot be specified explicitly in general.
CMA-ES outperformed over 100 black-box optimization approaches for a variety of benchmark problems [Hansen2006].

The CMA-ES algorithm selects solutions from a multivariate gaussian distribution. Following the evaluation of
all solutions, the solutions are sorted by evaluation values, and the distribution parameters
(i.e., the mean vector and the covariance matrix) are updated depending on the ranking of evaluation values.


EXAMPLE:
----------
1) Importing the necessary packages:

    .. code-block::
        import pylab as plt
        import numpy as np
        from artap.problem import Problem
        from artap.results import Results
        from artap.algorithm_cmaes import CMA_ES

2) Define the problem and it's parameters. Also, specify the goal function.
The problem class, has two methods: a) set, and b) evaluate.


a) set: the main goal of this method is to define the number of parameters and costs.

b) evaluate: this method should be written to define the optimization task.
the evaluate method should give back a list of the calculated objective values.

    .. code-block::
        class Schwefel(Problem):

            def set(self, **kwargs):
                self.name = "Schwefel function"
                self.parameters = [{'name': 'x_1', 'initial_value': 0.1, 'bounds': [0.0, 1.0]}]
                self.costs = [{'name': 'f_1'}]
                self.dimension = kwargs['dimension']
                self.global_optimum = 0.
                self.global_optimum_coords = [0.0 for x in range(self.dimension)]

            def evaluate(self, individual):
                x = individual.vector
                # the goal function
                F1 = 418.9829 - np.sum(x[0] * np.sin(np.sqrt(np.abs(x[0]))))

                return [F1]

3) Initialize the problem and the algorithm, then run the optimization.

    .. code-block::
        # Initialization of the problem
        problem = Schwefel(**{'dimension': 1})

        # Perform the optimization iterating over 100 times on 100 individuals.
        algorithm = CMA_ES(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        # Post - processing the results
        # reads in the result values into the b, results class
        results = Results(problem)
        pareto = results.pareto_values()

        # Convergence plot on a selected goal function and parameter
        slice = results.goal_on_parameter('x_1', 'f_1')
