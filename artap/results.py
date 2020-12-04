import csv
from .quality_indicator import gd, epsilon_add
from matplotlib import pylab, rc, axis


class Results:
    """ Class Results offers tools for interpreting calculated data. """

    def __init__(self, problem):
        self.problem = problem
        self.use_latex = True
        self.label_size = 16
        self.tick_size = 14
        self.title_size = 18
        self.legend = True
        self.width = 8
        self.hight = 5

        if self.use_latex:
            # allows using Latex
            rc('font', **{'family': ' DejaVu Sans', 'sans-serif': ['Helvetica']})
            rc('text', usetex=True)

        # sets the legend font size
        params = {'legend.fontsize': 14,
                  'legend.handlelength': 2}

        pylab.rcParams.update(params)

    def parameter_names(self):
        parameter_names = []
        for parameter in self.problem.parameters:
            parameter_names.append(parameter["name"])
        return parameter_names

    def parameter_number(self):
        return len(self.problem.parameters)

    def goal_number(self):
        return len(self.problem.costs)

    def goal_names(self):
        cost_names = []
        for cost in self.problem.costs:
            cost_names.append(cost["name"])
        return cost_names

    def parameter_index(self, name):
        try:
            return next((index for (index, d) in enumerate(self.problem.parameters) if d["name"] == name), None)
        except ValueError as e:
            raise ValueError('There is not a parameter with given name: {}'.format(name))

    def goal_index(self, name):
        try:
            return next((index for (index, d) in enumerate(self.problem.costs) if d["name"] == name), None)
            # return list(self.problem.costs).index(name)
        except ValueError as e:
            raise ValueError('There is not a cost function with given name: {}'.format(name))

    def parameters(self):
        out = []
        for individuals in self.problem.populations().values():
            for individual in individuals:
                out.append(individual.vector)
        return out

    def costs(self):
        out = []
        for individuals in self.problem.populations().values():
            for individual in individuals:
                out.append(individual.costs)
        return out

    def table(self, transpose=True):
        out = []
        for individuals in self.problem.populations().values():
            for individual in individuals:
                out.append(individual.vector + individual.costs)

        if transpose:
            return list(zip(*out))
        else:
            return out

    def population(self, population_id=-1):
        # Returns population with given index
        #if population_id >= len(self.problem.populations):
        #    raise ValueError('Index of population exceeds the number of populations.')
        if population_id == -1:
            individuals = self.problem.last_population()
        else:
            individuals = self.problem.population(population_id)
        return individuals

    def goal_on_index(self, name=None, population_id=-1):
        """ Returns a list of lists. The first list contains indexes of individuals in population,
            the other lists contains values of the goal function(s).
        """
        individuals = self.population(population_id)
        n = range(len(individuals))

        table = [list(n)]
        if name is None:
            for j in range(len(self.problem.costs)):
                table.append([])
                for i in n:
                    table[j + 1].append(individuals[i].costs[j])
        else:
            table.append([])
            index = self.goal_index(name)
            for i in n:
                table[1].append(individuals[i].costs[index])

        return table

    def parameter_on_index(self, name=None, population_id=-1):
        """
        Returns a list of lists. The first list contains indexes of individuals in population,
            the other lists contains values of the parameters(s).
        :param name: string representing the name of parameter if it is not given, all parameters are included
        :param population_id: index of the selected parameter
        :return:
        """

        individuals = self.population(population_id)
        n = range(len(individuals))
        table = [list(n)]
        if name is None:
            for j in range(len(self.problem.parameters)):
                table.append([])
                for i in n:
                    table[j + 1].append(individuals[i].vector[j])
        else:
            table.append([])
            index = self.parameter_index(name)
            for i in n:
                table[1].append(individuals[i].vector[index])

        return table

    def goal_on_parameter(self, parameter_name, goal_name, population_id=-1, sorted=False):
        """
        The method returns the dependance of selected goal function on particular parameter
        :param parameter_name: string specifying particular parameter
        :param goal_name: string specifying name of required goal function
        :param population_id: index of required population, if it is not given the last population is used
        :return: list of two lists, the first contains sorted parameter values, the second values of selected goal
        function
        """

        if population_id == -1:
            individuals = self.problem.last_population()
        else:
            individuals = self.population(population_id)

        parameter_index = self.parameter_index(parameter_name)
        goal_index = self.goal_index(goal_name)
        parameter_values = []
        goal_values = []

        for individual in individuals:
            parameter_values.append(individual.vector[parameter_index])
            goal_values.append(individual.costs[goal_index])

        if sorted is True:
            goal_values = self.sort_list(parameter_values, goal_values)
            parameter_values.sort()

        return [parameter_values, goal_values]

    def parameter_on_goal(self, goal_name, parameter_name, population_id=-1, sorted=False):
        parameter_values, goal_values = self.goal_on_parameter(parameter_name, goal_name, population_id, sorted=False)
        if sorted:
            parameter_values = self.sort_list(goal_values, parameter_values)
            goal_values.sort()

        return [goal_values, parameter_values]

    def parameter_on_parameter(self, parameter_1, parameter_2, population_id=-1, sorted=False):
        individuals = self.population(population_id)
        index_1 = self.parameter_index(parameter_1)
        index_2 = self.parameter_index(parameter_2)
        values_1 = []
        values_2 = []

        for individual in individuals:
            values_1.append(individual.vector[index_1])
            values_2.append(individual.vector[index_2])

        if sorted:
            values_2 = self.sort_list(values_1, values_2)
            values_1.sort()

        return [values_1, values_2]

    def export_to_csv(self, filename):
        """
        Writes out populations into a csv file, the file contains the costs and the parameters
        :return:
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # names
            out = ["population_id"]
            for parameter in self.problem.parameters:
                out.append(parameter["name"])
            for cost in self.problem.costs:
                out.append(cost["name"])

            writer.writerows([out])

            # values
            population_id = 0
            for individuals in self.problem.populations().values():
                for individual in individuals:
                    out = [population_id]
                    for i in individual.costs:
                        out.append(i)
                    for j in individual.vector:
                        out.append(j)

                    writer.writerows([out])
                population_id += 1

    def pareto_front(self, population_id=None):
        """

        :return: pareto front
        """
        if population_id is not None:
            individuals = self.population(population_id)
        else:
            individuals = self.problem.individuals

        n = self.goal_number()
        pareto_front = []
        for i in range(n):
            pareto_front.append([])
            for individual in individuals:
                if individual.features['front_number'] == 1:
                    pareto_front[i].append(individual.costs[i])

        return pareto_front

    @staticmethod
    def sort_list(list_1, list_2):
        zipped_pairs = zip(list_1, list_2)
        sorted_list = [x for _, x in sorted(zipped_pairs)]
        return sorted_list

    # TODO: Generalize
    # TODO: add test
    def find_optimum(self, name=None):
        """
        Search the optimal value for the given (by name parameter) single objective .

        :param name: string representing name of the goal function
        :return:
        """

        # get the index of the required parameter
        index = 0  # default - one parameter
        if name:
            for i in range(len(self.problem.costs)):
                cost = self.problem.costs[i]
                if cost['name'] == name:
                    index = i
        # if len(self.problem.data_store.individuals) is not 0:
        #    min_l = [min(self.problem.data_store.individuals, key=lambda x: x.costs[index])]
        # else:
        #if self.problem.archive:
        #    min_l = [min(self.problem.archive, key=lambda x: x.costs[index])]
        #else:
        if len(self.problem.individuals) > 0:
            min_l = [min(self.problem.individuals, key=lambda x: x.costs[index])]
        # for population in self.problem.populations:
        opt = min(min_l, key=lambda x: x.costs[index])
        return opt

    # TODO: same function - David, could you check it and write test?
    def pareto_values(self, archive=None):
        """
        :return: a list of lists which contains the optimal values of the cost function:
                l_sol[[c11, c12, ... c1n], ... [cm1, cm2, ... cmn]]
        """

        individuals = self.problem.last_population()
        l_sol = []

        # the pareto values collected in the archive, if the algorithm uses this strategy
        if archive:
            for individual in archive:
                l_sol.append(individual.costs)
        else:
            if len(individuals) > 1:
                for individual in individuals:
                    l_sol.append(individual.costs)

        return l_sol

    # TODO: add test
    def performance_measure(self, reference: list, type='epsilon'):
        """
        This function compares the result with a given, reference pareto-set. By default it offers to make
        an epsilon measure, but other metrics can be selected.

        :param reference: list of tuples, which are similar to the data of the calculated pareto-front
        :param type:
        :return:
        """

        computed = self.pareto_values()  # [[], [], .. ]

        if type == 'epsilon':
            result = epsilon_add(reference, computed)
        if type == 'gd':
            result = gd(reference, computed)

        return result

    def set_figure(self):
        # We change the fontsize of minor ticks label
        fig, ax = pylab.subplots(figsize=(self.width, self.hight))
        ax.tick_params(axis='both', which='major', labelsize=self.tick_size)
        ax.tick_params(axis='both', which='minor', labelsize=self.tick_size)
        ax.grid()
        # ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
        # removing top and right borders
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)  # adds major gridlines
        return [fig, ax]

    def get_objectives_plot(self):

        fig, ax = self.set_figure()
        all_individuals = self.costs()
        for point in all_individuals:
            ax.plot(point[0], point[1], '.')

        pareto = self.pareto_front()
        ax.plot(pareto[0], pareto[1], 'ro', label='Last Pareto front')

        ax.set_xlabel(r'$F_1$', fontsize=self.label_size)
        ax.set_ylabel(r'$F_2$', fontsize=self.label_size)
        ax.legend()
        return [fig, ax]

    def objectives_plot(self):
        fig, ax = self.get_objectives_plot()
        fig.show()

    def get_pareto_plot(self, cost_x=0, cost_y=1):
        """
        A simple 2d - pareto plot from the variable 1 and 2 by default.
        :return:
        """
        fig, ax = self.set_figure()
        pvalues = self.pareto_values()

        x = [i[cost_x] for i in pvalues]
        y = [i[cost_y] for i in pvalues]

        ax.scatter(x, y, alpha=0.80)

        # adds a title and axes labels
        x_name = self.problem.costs[cost_x]['name']
        y_name = self.problem.costs[cost_y]['name']

        ax.set_title('Pareto values', fontsize=self.title_size)
        ax.set_xlabel('$' + x_name + '$', fontsize=self.label_size)
        ax.set_ylabel('$' + y_name + '$', fontsize=self.label_size)
        return [fig, ax]


    def pareto_plot(self, cost_x=0, cost_y=1):
        fig, ax = self.get_pareto_plot(cost_x, cost_y)
        fig.show()

    def get_goal_on_index(self, name, population_id=-1):
        fig, ax = self.set_figure()
        table = self.goal_on_index(name=name, population_id=population_id)
        ax.plot(table[0], table[1])

        ax.set_xlabel(r'$k$', fontsize=self.label_size)
        ax.set_ylabel(r'$' + name + '$', fontsize=self.label_size)
        return [fig, ax]

    def goal_on_index_plot(self, name, population_id=-1):
        fig, ax = self.get_goal_on_index(name, population_id)
        fig.show()

    def get_parameter_on_index(self, name, population_id=-1):
        fig, ax = self.set_figure()
        table = self.parameter_on_index(name=name, population_id=population_id)
        ax.plot(table[0], table[1])

        ax.set_xlabel(r'$k$', fontsize=self.label_size)
        ax.set_ylabel(r'$' + name + '$', fontsize=self.label_size)
        return [fig, ax]

    def parameter_on_index_plot(self, name, population_id=-1):
        fig, ax = self.get_parameter_on_index(name, population_id)
        fig.show()

    def get_goal_on_parameter(self, parameter_name, goal_name, population_id=-1, sorted=False):
        fig, ax = self.set_figure()
        table = self.goal_on_parameter(parameter_name, goal_name, population_id, sorted)
        ax.plot(table[0], table[1], 'o')

        ax.set_xlabel(r'$' + parameter_name + '$', fontsize=self.label_size)
        ax.set_ylabel(r'$' + goal_name + '$', fontsize=self.label_size)
        return [fig, ax]

    def goal_on_parameter_plot(self, parameter_name, goal_name, population_id=-1, sorted=False):
        fig, ax = self.get_goal_on_parameter(parameter_name, goal_name, population_id, sorted)
        fig.show()

    def get_parameter_on_parameter(self, parameter_1, parameter_2, population_id=-1, sorted=False):
        fig, ax = self.set_figure()
        table = self.parameter_on_parameter(parameter_1, parameter_2, population_id, sorted)
        ax.plot(table[0], table[1], 'o')

        ax.set_xlabel(r'$' + parameter_1 + '$', fontsize=self.label_size)
        ax.set_ylabel(r'$' + parameter_2 + '$', fontsize=self.label_size)
        return [fig, ax]

    def parameter_on_parameter_plot(self, parameter_1, parameter_2, population_id=-1, sorted=False):
        fig, ax = self.get_parameter_on_parameter(parameter_1, parameter_2, population_id, sorted)
        fig.show()

    def goal_histogram_plot(self, name, population_id=-1):
        fig, ax = self.set_figure()
        table = self.goal_on_index(name=name, population_id=population_id)
        n, bins, patches = ax.hist(x=table[1], bins='auto', color='#0504aa',
                                    alpha=0.7, rwidth=0.85)
        fig.show()

    def get_mean_confidence_interval(self, name):
        index = self.goal_index(name)
        return 
