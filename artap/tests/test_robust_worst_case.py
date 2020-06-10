import unittest

from artap.benchmark_robust import Synthetic1D, Synthetic2D, Synthetic5D, Synthetic10D
from artap.algorithm_genetic import EpsMOEA
from artap.algorithm import EvaluatorType
from artap.results import Results
from artap.archive import Archive
import pylab as plt
import artap.colormaps as cmaps


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_worst_case(self):
        # problem = Synthetic1D()
        problem = Synthetic2D()
        algorithm = EpsMOEA(problem, evaluator_type=EvaluatorType.WORST_CASE)
        algorithm.options['max_population_size'] = 200
        algorithm.options['max_population_number'] = 100
        algorithm.run()
        # an archive to collect the eps-dominated solutions
        # archive = Archive(dominance=EpsilonDominance(epsilons=[0.0001, 0.00001]))
        archive = Archive()
        # archive.extend(problem.populations[-1].individuals)
        # archive += problem.populations[-1].individuals
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        [x, y, z] = problem.get_data_2d()
        ax.plot_surface(x, y, z, cmap=cmaps.viridis,
                               linewidth=0, antialiased=True)

        for individual in problem.populations[-1].individuals:
            archive += individual
            x_1 = individual.vector[0]
            x_2 = individual.vector[1]
            y = individual.costs[0]
            print(individual)
            ax.scatter(x_1, x_2, y, color='red', marker='o')

            for child in individual.children:
                x_1 = child.vector[0]
                x_2 = child.vector[1]
                y = child.costs[0]
                ax.scatter(x_1, x_2, y, color='black', marker='o')
        plt.show()

        results = Results(problem)




if __name__ == '__main__':
    unittest.main()
