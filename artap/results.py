# from .problem import Problem

import matplotlib
matplotlib.use('Agg')

import pylab as pl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc



# import sys

class Results:

    def __init__(self, problem):
        self.problem = problem

    def find_minimum(self, name=0):
        """
        Search the optimal value for the given (by name parameter) single objective .

        :param name:
        :return:
        """
        ind = None
        # get the index of the required parameter
        index = int(self.problem.costs.get(name))

        min_l = []
        for population in self.problem.populations:

            if type(population.individuals[index].costs) is not list:
                min_l.append(min(population.individuals, key=lambda x: x.costs))
                opt = min(min_l, key=lambda x: x.costs)
                opt = opt.costs
            else:
                min_l.append(min(population.individuals, key=lambda x: x.costs[index]))
                opt = min(min_l, key=lambda x: x.costs[index])
                opt = opt.costs[index]

        return opt

    def pareto_values(self):
        """
        :return: a list of lists which contains the optimal values of the cost function:
                l_sol[[c11, c12, ... c1n], ... [cm1, cm2, ... cmn]]
        """
        population = self.problem.populations[-1]
        l_sol = []
        if len(population.individuals) > 1:
            for individual in population.individuals:
                l_sol.append(individual.costs)
        return l_sol


class GraphicalResults(Results):

    def __init(self, problem):
        super.__init__(problem)
        self.name = ""
        rc('text', usetex=True)
        rc('font', family='serif')

    def plot_all_individuals(self, filename=None):
        for population in self.problem.populations:
            for individual in population.individuals:
                pl.plot(individual.number, individual.parameters[0], 'x')

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + "all_individuals.pdf")

    def plot_populations(self):
        for population in self.problem.populations:
            figure_name = self.problem.working_dir + "pareto_" + str(population.number) + ".pdf"
            if len(population.individuals) > 1:
                figure = Figure()
                FigureCanvas(figure)
                figure.add_subplot(111)
                ax = figure.axes[0]
                colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']

                for individual in population.individuals:
                    # TODO: Make for more objective values
                    ax.plot(individual.costs[0], individual.costs[1], 'o')
                    if hasattr(individual, 'front_number'):
                        if individual.front_number != 0:
                            scale = 100 / (individual.front_number / 4.)
                            ax.scatter(individual.costs[0], individual.costs[1],
                                       scale, c=colors[(individual.front_number - 1) % 6])
                ax.set_xlabel('$x$')
                ax.set_ylabel('$y$')
                ax.grid()
                figure.savefig(figure_name)
