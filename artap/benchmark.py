from .quality_indicator import epsilon_add
from .algorithm_genetic import NSGAII
from .benchmark_pareto import DTLZI, DTLZII, DTLZIII, DTLZIV
from .results import Results
from .individual import Individual

"""
Comparison is based on the following paper:

  [1]  Durillo, Juan J., José García-Nieto, Antonio J. Nebro, Carlos A. Coello Coello, Francisco Luna, and Enrique Alba. 
       "Multi-objective particle swarm optimizers: An experimental comparison."
        In International conference on evolutionary multi-criterion optimization, 
        pp. 495-509. Springer, Berlin, Heidelberg, 2009.

Common parameters
-----------------

    Swarm/Generation size: 100 particles
    Iterations: 250

"""

def b_nsga2_dtlzI():
    """
    Benchmarks the performance of the NSGA-II algorithm with the DTLZI test problem.
    The mean value of the unary epsilon indicator should be around [1]: 7.13e-3  +- 1.6e-3

    :return: the unary epsilon indicator for the dtlz-i test problem
    """

    test2d = DTLZI(**{'dimension': 9, 'm': 2})

    # Cross-check with Platypus and JMetalpy implementatinos
    #print(test2d.evaluate(Individual([1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5])))
    #print(test2d.evaluate(Individual([1.0, 0.1, 0.9, 1.0, 0.8, 0.5, 0.5])))
    #print(test2d.evaluate(Individual([0.6, 0.7, 1.0, 1.0, 1.0, 0.5, 0.5])))

    # expected results:
    #
    # [50.5, 0.0]
    # [33.50000000000001, 0.0]
    # [24.0, 16.0]

    algorithm = NSGAII(test2d)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

    results = Results(test2d)
    results.pareto_plot()
    vals = results.pareto_values()



    #reference = []
    #for elem in vals:
    #    reference.append((elem[0], 0.5 - elem[0]))

    print(vals)
    #print(reference)

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # display the results
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.scatter(vals[0], vals[1], vals[2])
    ax.set_xlim([0, 1.1])
    ax.set_ylim([0, 1.1])
    ax.set_zlim([0, 1.1])
    ax.view_init(elev=30.0, azim=15.0)
    #ax.locator_params(nbins=4)

    plt.show()

b_nsga2_dtlzI()
