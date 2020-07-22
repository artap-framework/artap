from artap.benchmark_robust import Synthetic2D
from artap.algorithm_genetic import EpsMOEA
from artap.algorithm import EvaluatorType
from artap.results import Results
import pylab as plt
import artap.colormaps as cmaps


if __name__ == '__main__':
    problem = Synthetic2D()
    algorithm = EpsMOEA(problem, evaluator_type=EvaluatorType.WORST_CASE)
    algorithm.options['max_population_size'] = 200
    algorithm.options['max_population_number'] = 100
    algorithm.run()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    [x, y, z] = problem.get_data_2d()
    ax.plot_surface(x, y, z, cmap=cmaps.viridis,
                    linewidth=0, antialiased=True)

    for individual in problem.last_population():
        x_1 = individual.vector[0]
        x_2 = individual.vector[1]
        y = individual.costs[0]
        ax.scatter(x_1, x_2, y, color='red', marker='o')

        for child in individual.children:
            x_1 = child.vector[0]
            x_2 = child.vector[1]
            y = child.costs[0]
            ax.scatter(x_1, x_2, y, color='black', marker='o')
    plt.show()

    results = Results(problem)
