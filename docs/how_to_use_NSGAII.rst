. index::
   NSGAII: Non-dominated Sorting Genetic Algorithm

Example of how to use NSGAII
----------------------------------------------------------------------
The algorithm is implemented based on [PDB]_. The method is based on the overall structure of a genetic algorithm,
but with modified mating and survival selection. Individuals are chosen frontward in NSGA-II. As a result, a front will
need to be formed since not all persons will be permitted to live. The crowding distance is used to select solutions in
this dividing front.

In the objective space, the crowding distance is the Manhattan Distance. However, the extreme spots are intended to be
retained every generation and, as a result, are allocated an infinite crowding distance.

In addition, to boost selection pressure, NSGA-II utilizes a binary tournament mating selection.
Each individual is compared first by rank, then by crowding distance.

Example :
----------------------------------------------------------------------
Here, we can use NSGAII for solving problems, for example, Ackley.

.. code-block:: python

    from artap.algorithm_genetic import NSGAII
    from artap.benchmark_functions import Ackley
    from artap.results import Results

    problem = Ackley(**{'dimension': 1})
    algorithm = NSGAII(problem)
    algorithm.options['max_population_size'] = 10
    algorithm.options['max_population_number'] = 10

    algorithm.run()

    solution = Results(problem)
    optimum = solution.find_optimum()
    print(f'Optimum found: \nX = {optimum.vector}\nF = {optimum.costs}')


----------------------------------------------------------------------
Results :
----------------------------------------------------------------------

.. code-block::

    2021-10-29 11:34:14,567 (INFO): Ackley-546022 - run (148) - NSGA_II: 10/100
    2021-10-29 11:34:14,711 (INFO): Ackley-546022 - run (173) - NSGA_II: elapsed time: 0.1447887420654297 s
    Optimum found:
    X = [0.12470327216726784]
    F = [1.180137980797721]


.:[PDB] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan. A fast and elitist multiobjective genetic algorithm: nsga-II.
Trans. Evol. Comp, 6(2):182–197, April 2002. URL: http://dx.doi.org/10.1109/4235.996017, doi:10.1109/4235.996017.
