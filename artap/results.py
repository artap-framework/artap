import csv
from .quality_indicator import gd, epsilon_add


class Results:
    """ Class Results offers tools for interpreting calculated data. """

    def __init__(self, problem):
        self.problem = problem

    def parameter_names(self):
        parameter_names = []
        for parameter in self.problem.parameters:
            parameter_names.append(parameter['name'])
        return parameter_names

    def parameter_number(self):
        return len(self.problem.parameters)

    def goal_function_number(self):
        return len(self.problem.costs)

    def goal_function_names(self):
        cost_names = []
        for cost in self.problem.costs:
            cost_names.append(cost['name'])
        return cost_names

    def parameter_index(self, name):
        index = -1
        for i in range(len(self.problem.parameters)):
            parameter = self.problem.parameters[i]
            if parameter['name'] == name:
                index = i
        if index == -1:
            raise ValueError('There is not a parameter with given name: {}'.format(name))
        return index

    def goal_index(self, name):
        index = -1
        for i in range(len(self.problem.costs)):
            cost = self.problem.costs[i]
            if cost['name'] == name:
                index = i
        if index == -1:
            raise ValueError('There is not a cost function with given name: {}'.format(name))
        return index

    def population(self, population_id):
        # Returns population with given index
        #if population_id >= len(self.problem.populations):
        #    raise ValueError('Index of population exceeds the number of populations.')

        population = self.problem.population(population_id)
        return population

    def goal_on_index(self, name=None, population_id=-1):
        """ Returns a list of lists. The first list contains indexes of individuals in population,
            the other lists contains values of the goal function(s).
        """
        population = self.population(population_id)
        n = range(len(population.individuals))

        table = [list(n)]
        if name is None:
            for j in range(len(self.problem.costs)):
                table.append([])
                for i in n:
                    table[j + 1].append(population.individuals[i].costs[j])
        else:
            table.append([])
            index = self.goal_index(name)
            for i in n:
                table[1].append(population.individuals[i].costs[index])

        return table

    def parameter_on_index(self, name=None, population_id=-1):
        """
        Returns a list of lists. The first list contains indexes of individuals in population,
            the other lists contains values of the parameters(s).
        :param name: string representing the name of parameter if it is not given, all parameters are included
        :param population_id: index of the selected parameter
        :return:
        """

        population = self.population(population_id)
        n = range(len(population.individuals))
        table = [list(n)]
        if name is None:
            for j in range(len(self.problem.parameters)):
                table.append([])
                for i in n:
                    table[j + 1].append(population.individuals[i].vector[j])
        else:
            table.append([])
            index = self.parameter_index(name)
            for i in n:
                table[1].append(population.individuals[i].vector[index])

        return table

    @staticmethod
    def sort_list(list_1, list_2):
        zipped_pairs = zip(list_1, list_2)
        sorted_list = [x for _, x in sorted(zipped_pairs)]
        return sorted_list

    def goal_on_parameter(self, parameter_name, goal_name, population_id=-1):
        """
        The method returns the dependance of selected goal function on particular parameter
        :param parameter_name: string specifying particular parameter
        :param goal_name: string specifying name of required goal function
        :param population_id: index of required population, if it is not given the last population is used
        :return: list of two lists, the first contains sorted parameter values, the second values of selected goal
        function
        """
        individuals = self.population(population_id)
        parameter_index = self.parameter_index(parameter_name)
        goal_index = self.goal_index(goal_name)
        parameter_values = []
        goal_values = []

        for individual in individuals:
            parameter_values.append(individual.vector[parameter_index])
            goal_values.append(individual.costs[goal_index])

        goal_values = self.sort_list(parameter_values, goal_values)
        parameter_values.sort()
        return [parameter_values, goal_values]

    def parameter_on_parameter(self, parameter_1, parameter_2, population_id=-1):
        individuals = self.population(population_id)
        index_1 = self.parameter_index(parameter_1)
        index_2 = self.parameter_index(parameter_2)
        values_1 = []
        values_2 = []

        for individual in individuals:
            values_1.append(individual.vector[index_1])
            values_2.append(individual.costs[index_2])

        dependent_values = self.sort_list(values_1, values_2)
        values_1.sort()
        return [values_1, dependent_values]

    # TODO: Generalize
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

    def pareto_front(self, population_id=-1):
        """

        :return:
        """
        individuals = self.population(population_id)
        n = self.goal_function_number()
        pareto_front = []
        for i in range(n):
            pareto_front.append([])
            for individual in individuals:
                if individual.features['front_number'] == 1:
                    pareto_front[i].append(individual.costs[i])

        return pareto_front

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

    def pareto_plot(self, cost_x=0, cost_y=1):
        """
        A simple 2d - pareto plot from the variable 1 and 2 by default.
        :return:
        """

        pvalues = self.pareto_values()

        x = [i[cost_x] for i in pvalues]
        y = [i[cost_y] for i in pvalues]

        import pylab as plt

        fig, ax = plt.subplots(figsize=(10, 5))  # customizes alpha for each dot in the scatter plot
        ax.scatter(x, y, alpha=0.80)

        # adds a title and axes labels
        x_name = self.problem.costs[cost_x]['name']
        y_name = self.problem.costs[cost_y]['name']

        ax.set_title('Pareto values')
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

        # removing top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)  # adds major gridlines
        ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

        plt.show()
        return

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

    def parameters(self):
        out = []
        for individuals in self.problem.populations():
            for individual in individuals:
                out.append(individual.vector)
        return out

    def costs(self):
        out = []
        for individuals in self.problem.populations():
            for individual in individuals:
                out.append(individual.costs)
        return out

    def write_out_populations(self):
        """
        Writes out every population into a a csv file, the file contains the costs and the parameters and the
        auxiliary variables if they are exist.
        :return:
        """
        for population in self.problem.populations:
            out_file = self.problem.working_dir + "population_" + \
                       str(self.problem.populations.index(population)) + "_costs.csv"

            with open(out_file, 'w', newline='') as f:
                writer = csv.writer(f)

                for index, individual in enumerate(population.individuals):
                    out = []
                    for i in individual.costs:
                        out.append(i)
                    for j in individual.vector:
                        out.append(j)

                    if hasattr(individual, 'auxvar'):
                        for k in individual.auxvar:
                            out.append(k)
                    writer.writerows([out])
