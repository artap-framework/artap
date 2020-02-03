import os
import numpy as np
import pylab as pl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc

import logging
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

import csv

class Results:
    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self, problem):
        self.problem = problem

    def value(self, individual, name):
        # TODO: check speed
        val = 0

        try:
            # try costs
            # get the index of the required parameter
            index = 0  # default - one parameter
            for i in range(len(self.problem.costs)):
                cost = self.problem.costs[i]
                if cost['name'] == name:
                    index = i
                    break

            # ind = list(self.problem.costs.keys()).index(name)
            val = individual.costs[index]
        except ValueError:
            # try parameters
            ind = list(self.problem.parameters.keys()).index(name)
            val = individual.vector[ind]
        except ValueError:
            self.problem.logger.error("Value '{}' not found".format(name))

        return val

    def find_minimum(self, name=None):
        """
        Search the optimal value for the given (by name parameter) single objective .

        :param name:
        :return:
        """
        # get the index of the required parameter
        index = 0  # default - one parameter
        if name:
            for i in range(len(self.problem.costs)):
                cost = self.problem.costs[i]
                if cost['name'] == name:
                    index = i
        #if len(self.problem.data_store.individuals) is not 0:
        #    min_l = [min(self.problem.data_store.individuals, key=lambda x: x.costs[index])]
        #else:
        if len(self.problem.data_store.populations[-1].archives) > 0:
            min_l = [min(self.problem.data_store.populations[-1].archives, key=lambda x: x.costs[index])]
        else:
            if len(self.problem.data_store.populations[-1].individuals) is not 0:
                min_l = [min(self.problem.data_store.populations[-1].individuals, key=lambda x: x.costs[index])]
        # for population in self.problem.data_store.populations:
        opt = min(min_l, key=lambda x: x.costs[index])
        return opt

    def find_pareto(self, name1, name2):
        pareto_front_x = []
        pareto_front_y = []
        for population1 in self.problem.data_store.populations:
            for individual1 in population1.individuals:
                is_pareto = True

                for population2 in self.problem.data_store.populations:
                    for individual2 in population2.individuals:
                        # TODO: MINIMIZE and MAXIMIZE
                        if self.value(individual1, name1) > self.value(individual2, name1) \
                                and self.value(individual1, name2) > self.value(individual2, name2):
                            is_pareto = False

                if is_pareto:
                    pareto_front_x.append(self.value(individual1, name1))
                    pareto_front_y.append(self.value(individual1, name2))

        return pareto_front_x, pareto_front_y

    def pareto_values(self):
        """
        :return: a list of lists which contains the optimal values of the cost function:
                l_sol[[c11, c12, ... c1n], ... [cm1, cm2, ... cmn]]
        """

        population = self.problem.data_store.populations[-1]
        l_sol = []

        if len(self.problem.data_store.populations[-1].archives) < 1:
            if len(population.individuals) > 1:
                for individual in population.individuals:
                    l_sol.append(individual.costs)
        else:
            if len(population.archives) > 1:
                for individual in population.archives:
                    l_sol.append(individual.costs)
        return l_sol

    def table(self):
        out = []
        if len(self.problem.data_store.populations) > 0:
            population = self.problem.data_store.populations[0]
            if len(population.individuals) > 0:
                # init array
                individual = population.individuals[0]
                for v in individual.vector:
                    out.append([])
                for c in individual.costs:
                    out.append([])

                for population in self.problem.data_store.populations:
                        for individual in population.individuals:
                            i = 0
                            for v in individual.vector:
                                out[i].append(v)
                                i += 1
                            for c in individual.costs:
                                out[i].append(c)
                                i += 1

        return out


    def parameters(self):
        out = []
        for population in self.problem.data_store.populations:
            for individual in population.individuals:
                out.append(individual.vector)
        return out

    def costs(self):
        out = []
        for population in self.problem.data_store.populations:
            for individual in population.individuals:
                out.append(individual.costs)
        return out

    def write_out_populations(self):
        """
        Writes out every population into a
        :return:
        """
        for population in self.problem.data_store.populations:
            out_file = self.problem.working_dir + "population_" + \
                          str(self.problem.data_store.populations.index(population)) + "_costs.csv"

            with open(out_file, 'w', newline='') as f:
                writer = csv.writer(f)

                for index, individual in enumerate(population.individuals):
                    out = []
                    for i in individual.costs:
                        out.append(i)
                    for j in individual.vector:
                        out.append(j)

                    #print(index, out)
                    writer.writerows([out])

        return

class GraphicalResults(Results):

    def __init__(self, problem):
        super().__init__(problem)
        self.name = ""
        # rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
        # pl.rcParams['figure.figsize'] = 6, 4
        rc('text', usetex=True)
        self.labels_size = 16
        self.tick_size = 12

    def plot_scatter(self, name1, name2, filename=None, population_number=None):
        figure = Figure()
        figure.clf()

        if population_number is None:
            populations = self.problem.data_store.populations
        else:
            populations = [self.problem.data_store.populations[population_number]]

        for population in populations:
            values1 = []
            values2 = []
            for individual in population.individuals:
                values1.append(self.value(individual, name1))
                values2.append(self.value(individual, name2))
            pl.scatter(values1, values2)

        # pareto front
        values1 = []
        values2 = []
        population = populations[-1]
        for individual in population.individuals:
            if hasattr(individual, 'front_number'):
                if individual.front_number == 1:
                    values1.append(self.value(individual, name1))
                    values2.append(self.value(individual, name2))
                pl.scatter(values1, values2, c='k')

        ax = pl.gca()
        # ax.set_yscale('log')
        # ax.set_xscale('log')
        #ax.set_xlim(-1.5, -0.9)
        #ax.set_ylim(0.3, 0.8)
        #ax.set_xlim(0.00000, 0.0004)
        #ax.set_ylim(50, 200)
        #ax.set_xlim(0.00000, 0.001)
        #ax.set_ylim(60, 300)
        #ax.set_xlim(0.00000, 0.00125)
        #ax.set_ylim(-0.00001, 0.0002)

        # labels
        pl.grid()
        pl.xlabel("${}$".format(name1))
        pl.ylabel("${}$".format(name2))

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + os.sep + "scatter.pdf")
        pl.close()

    def plot_convergence_chart(self, name1, filename=None, population_number=None):

        figure = Figure()
        figure.clf()

        # all individuals
        if population_number is None:
            populations = self.problem.data_store.populations
        else:
            populations = [self.problem.data_store.populations[population_number]]

        results = []
        for population in populations:
            min_l = min(population.individuals, key=lambda x: x.costs[0])
            results.append(min_l.costs)

        pl.grid()
        pl.xlabel("Number of generation")
        pl.ylabel("TOC [eur]".format(name1))

        pl.plot(results)
        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig("convergence.pdf")
        pl.close()

    def plot_scatter_vectors(self, name1, name2, filename=None, population_number=None):
        figure = Figure()
        figure.clf()

        # all individuals
        if population_number is None:
            populations = self.problem.data_store.populations
        else:
            populations = [self.problem.data_store.populations[population_number]]

        for population in populations:
            values1 = []
            values2 = []
            vector_x = []
            vector_y = []
            for individual in population.individuals:
                values1.append(individual.vector[0])
                values2.append(individual.vector[1])
                vector_x.append(individual.velocity_i[0])
                vector_y.append(individual.velocity_i[1])

            pl.scatter(values1, values2)
            pl.quiver(values1, values2, vector_x, vector_y)

        # pareto front
        values1 = []
        values2 = []
        population = populations[-1]
        for individual in population.individuals:
            if individual.front_number == 1:
                values1.append(self.value(individual, name1))
                values2.append(self.value(individual, name2))
        pl.scatter(values1, values2, c='k')

        # labels
        pl.grid()
        pl.xlabel("${}$".format(name1))
        pl.ylabel("${}$".format(name2))

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + os.sep + "scatter.pdf")
        pl.close()

    def plot_individuals(self, name, filename=None):
        # all individuals
        n = 1
        for population in self.problem.data_store.populations:
            ind = []
            values = []
            for individual in population.individuals:
                ind.append(n + len(ind))
                values.append(self.value(individual, name))
            n += len(ind)
            pl.scatter(ind, values)

        # labels
        pl.grid()
        pl.xlabel("$N$")
        pl.ylabel("${}$".format(name))
        # pl.ylim(0, 0.0003)

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + os.sep + "individuals.pdf")
        pl.close()

    def plot_all_individuals(self, filename=None):
        for population in self.problem.data_store.populations:
            for individual in population.individuals:
                pl.plot(individual.vector[0], 'x')

        if filename is not None:
            pl.savefig(filename)
        else:
            pl.savefig(self.problem.working_dir + "all_individuals.pdf")

    def plot_populations(self):
        for population in self.problem.data_store.populations:
            figure_name = self.problem.working_dir + "pareto_" + \
                          str(self.problem.data_store.populations.index(population)) + ".pdf"
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
                            scale = 100 / (individual.front_number / 1.)
                            ax.scatter(individual.costs[0], individual.costs[1],
                                       scale, c=colors[(individual.front_number - 1) % 6])
                labels = []
                for cost in self.problem.costs:
                    labels.append(cost['name'])
                x_label = r'$' + labels[0] + '$'
                y_label = r'$' + labels[1] + '$'
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.grid()

                figure.savefig(figure_name)

    def plot_gradients(self):
        population = self.problem.data_store.populations[-1]  # Last population
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
                                gradient_length += x[i] ** 2

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
