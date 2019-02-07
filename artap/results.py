# from .problem import Problem

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pylab as pl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc

import os

class Results:
    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self, problem):
        self.problem = problem

    def find_minimum(self, name=None):
        """
        Search the optimal value for the given (by name parameter) single objective .

        :param name:
        :return:
        """
        # get the index of the required parameter
        index = 0  # default - one parameter
        if name:
            index = int(self.problem.costs.get(name))

        min_l = []
        for population in self.problem.populations:
            min_l.append(min(population.individuals, key=lambda x: x.costs[index]))
            opt = min(min_l, key=lambda x: x.costs[index])
            opt = opt.costs[index]

        return opt

    def find_pareto(self, costs=[]):

        keys = list(costs.keys())
        index1 = 0 # int(self.problem.costs.get(keys[0]))
        index2 = 1 # int(self.problem.costs.get(keys[1]))

        pareto_front_x = []
        pareto_front_y = []
        for population1 in self.problem.populations:
            for individual1 in population1.individuals:
                is_pareto = True

                for population2 in self.problem.populations:
                    for individual2 in population2.individuals:
                        # TODO: MINIMIZE and MAXIMIZE
                        if individual1.costs[index1] > individual2.costs[index1] \
                                and individual1.costs[index2] > individual2.costs[index2]:
                            is_pareto = False

                if is_pareto:
                    pareto_front_x.append(individual1.costs[index1])
                    pareto_front_y.append(individual1.costs[index2])

        return pareto_front_x, pareto_front_y

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

    def __init__(self, problem):
        super().__init__(problem)
        self.name = ""
        rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
        # pl.rcParams['figure.figsize'] = 6, 4
        rc('text', usetex=True)
        self.labels_size = 16
        self.tick_size = 12


    def plot_all_individuals(self, filename=None):
        for population in self.problem.populations:
            for individual in population.individuals:
                pl.plot(individual.number, individual.parameters[0], 'x')

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + os.sep + "all_individuals.pdf")

    def plot_populations(self):
        for population in self.problem.populations:
            figure_name = self.problem.working_dir + "pareto_" + str(population.number) + ".pdf"
            if len(population.individuals) > 1:
                figure = Figure()
                FigureCanvas(figure)
                plot = figure.add_subplot(111)
                plot.tick_params(axis='both', which='major', labelsize=self.tick_size)
                plot.tick_params(axis='both', which='minor', labelsize=self.tick_size - 2)
                ax = figure.axes[0]
                colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']

                for individual in population.individuals:
                    # TODO: Make for more objective values
                    #
                    if hasattr(individual, 'front_number'):
                        if individual.front_number != 0:
                            scale = 100 / (individual.front_number / 4.)
                            ax.scatter(individual.costs[0], individual.costs[1],
                                           scale, c=colors[(individual.front_number - 1) % 6])
                            ax.plot(individual.costs[0], individual.costs[1], 'o')
                labels = list(self.problem.costs.keys())
                x_label = r'$' + labels[0] + '$'
                y_label = r'$' + labels[1] + '$'
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.grid()
                figure.savefig(figure_name)

    def plot_gradients(self):
            population = self.problem.populations[-1]  # Last population
            figure_name = self.problem.working_dir + "gradients_" + str(population.number) + ".pdf"
            if len(population.individuals) > 1:
                figure = Figure()
                FigureCanvas(figure)
                plot = figure.add_subplot(111)
                plot.tick_params(axis='both', which='major', labelsize=self.tick_size)
                plot.tick_params(axis='both', which='minor', labelsize=self.tick_size - 2)
                ax = figure.axes[0]
                colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']

                grad = [[], []]

                sorted(population.individuals, key=lambda item: item.costs[0])

                for individual in population.individuals:
                    # TODO: Make for more objective values

                    if hasattr(individual, 'front_number'):
                        if individual.front_number == 1:
                            gradient_length = 0

                            for i in range(2):
                                for x in individual.gradient:
                                    gradient_length += x[i]**2

                                gradient_length = np.sqrt(gradient_length)
                                grad[i].append(gradient_length)

                x_axis = range(1, len(grad[0]) + 1)
                ax.bar(x_axis, grad[0], align='edge', width=0.45)
                ax.bar(x_axis, grad[1], align='center', width=0.45)
                ax.set_xlabel(r'$i$ [-]', size=self.labels_size)
                ax.set_ylabel(r'$\| \nabla F_1 \|, \| \nabla F_2 \|$', size=self.labels_size)
                ax.grid()
                pl.show()
                pl.tight_layout()
                figure.savefig(figure_name)
