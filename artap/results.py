import csv
import numpy as np
from .quality_indicator import gd, epsilon_add
from .operators import derivative, std_linear
from .individual import Individual


class Results:
    """ Class Results offers tools for interpreting calculated data. """

    def __init__(self, problem):
        self.problem = problem

    def parameter_names(self):
        """ Returns a list of parameter names for the given problem. """
        parameter_names = []
        for parameter in self.problem.parameters:
            parameter_names.append(parameter["name"])
        return parameter_names

    def parameter_number(self):
        """ Returns the number of parameters."""
        return len(self.problem.parameters)

    def goal_number(self):
        """ Returns the number of goal functions. """
        return len(self.problem.costs)

    def goal_names(self):
        """ Returns a list of goal names for the given problem. """
        cost_names = []
        for cost in self.problem.costs:
            cost_names.append(cost["name"])
        return cost_names

    def parameter_index(self, name):
        try:
            return next((index for (index, d) in enumerate(self.problem.parameters) if d["name"] == name), None)
        except ValueError as e:
            raise ValueError('There is not a parameter with given name: {}'.format(name))

    # ToDo: Replace exception raise by warning?
    def goal_index(self, name):
        index = next((index for (index, d) in enumerate(self.problem.costs) if d["name"] == name), None)
        if index is not None:
            return index
        else:
            raise ValueError('There is not a cost function with given name: {}'.format(name))

    def parameters(self):
        out = []
        for individuals in self.problem.populations().values():
            for individual in individuals:
                out.append(individual.vector)
        return out

    def costs(self):
        """ Returns the list containing cost values for all individuals.
            Example of usage:
                costs = results.costs()
                plt.plot(costs, '.')
        """
        out = []
        n = len(self.problem.individuals[0].costs)
        for i in range(n):
            out.append([])

        for individual in self.problem.individuals:
            for i in range(n):
                out[i].append(individual.costs[i])
        return out

    def table(self, transpose=True):
        """ Returns the table where rows consist of values of parameters and values of goal functions. """
        out = []
        for individuals in self.problem.populations().values():
            for individual in individuals:
                out.append(individual.vector + individual.costs)

        if transpose:
            return list(zip(*out))
        else:
            return out

    # TODO : This method returns all the populations instead of the population in the given index
    def population(self, population_id=-1):
        # Returns population with given index
        #   if population_id >= len(self.problem.populations):
        #    raise ValueError('Index of population exceeds the number of populations.')
        if population_id == -1:
            # TODO : last_population returns all the populations instead of last index population
            individuals = self.problem.last_population()
        else:
            # TODO : population() must be modified to return the given index population
            individuals = self.problem.population(population_id)
        return individuals

    # I assume this method must return the goal on the given index not to return all the population or the name must
    # change
    def goal_on_index(self, name=None, population_id=-1):
        """
        Returns a list of lists. The first list contains indexes of individuals in population,
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

    # I assume this method must return the goal on the given index not to return all the population or the name must
    # change
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
                    # population_id += 1
                    # increasing population_id does not work properly here, it must be written as below
                    population_id += 1

    def pareto_individuals(self, population_id=None):
        """

        :return: pareto front
        """
        if population_id is not None:
            individuals = self.population(population_id)
        else:
            individuals = self.population(-1)

        pareto_individuals = []
        for individual in individuals:
            if individual.features['front_number'] == 1:
                pareto_individuals.append(individual)

        return pareto_individuals

    def pareto_front(self, population_id=None):
        """

        :return: pareto front
        """
        if population_id is not None:
            individuals = self.population(population_id)
        else:
            individuals = self.population(-1)

        n = self.goal_number()
        pareto_front = []
        for i in range(n):
            pareto_front.append([])

        for individual in individuals:
            if individual.features['front_number'] == 1:
                for i in range(n):
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
        min_l = []
        if name:
            index = self.goal_index(name)

        criteria = None
        if 'criteria' in self.problem.costs[index]:
            criteria = self.problem.costs[index]['criteria']

        if criteria == 'minimize' or criteria is None:
            if len(self.problem.individuals) > 0:
                min_l = [min(self.problem.individuals, key=lambda x: x.costs[index])]
        else:
            if len(self.problem.individuals) > 0:
                min_l = [max(self.problem.individuals, key=lambda x: x.costs[index])]

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

        result = 0
        computed = self.pareto_values()  # [[], [], .. ]

        if type == 'epsilon':
            result = epsilon_add(reference, computed)
        if type == 'gd':
            result = gd(reference, computed)

        return result

    def get_population_ids(self):
        ids = set()
        for individual in self.problem.individuals:
            ids.add(individual.population_id)
        return ids

    def integration_measure(self):
        Integration = 0
        opt = self.find_optimum('f_1')
        for individual in self.problem.individuals:
            Integration += individual.costs[0]
        ub = self.problem.u_b
        lb = self.problem.l_b
        sampling_size = self.problem.sampling_size
        result = ((ub - lb) / len(self.problem.individuals)) * Integration

        return result

    def form_reliability(self, problem, individual):
        """
            Performs the FORM-HLRF algorithm
                The goal is to find the reliability index for a nonlinear function g(Xi).

                HL_RF algorithm steps:
                1) Define the limit state function (𝑔) and the convergence criterion (tol = 1e-3), statistical characteristics
                 of basic random variables (mean, standard deviation, and distribution function for each random variable).
                2) Transfer the random variables from 𝑋-space to 𝑈-space according to
                    .. math::
                        U = (X - \mu_X^{e}) / \sigma_X^{e}
                3) Compute the gradient vector and limit state function at point U𝑘.
                4) Compute the cost function using
                    .. math::
                        U^{k+1} = [(G(U^{k}) - \grad G(U^{k})U^{k}) / \norm{\grad G(U^{k})}] \alpha^{k}

                    where \alpha^{k} is sensivity factor that can be calculated by:
                    ..math::
                        \alpha^{k} = -(\grad G(U^{k})) / \norm{\grad G(U^{k})}

                5) Transfer the basic random variables from 𝑈-space to 𝑋-space.
                6) Control the convergence conditions as below; if true then the method is converged, stop and go to step (7);
                else, 𝑘 = 𝑘+1 and go to step (2).
                7) Estimate the failure probability by
                    ..math::
                        P_f ~~ \phi(-\beta)
                    where \phi is the CDF of the standard normal distribution and \beta = \norm{U^{*}} is the reliability index.

                ..Reference::

                [1] A Novel Algorithm for Structural Reliability Analysis Based on Finite Step Length and Armijo Line Search
                    https://www.mdpi.com/2076-3417/9/12/2546
                [2] A Comparative Study of First-Order Reliability Method-Based Steepest Descent Search Directions for
                 Reliability Analysis of Steel Structures, https://www.hindawi.com/journals/ace/2017/8643801/
                [3] Reliability analysis and optimal design under uncertainty - Focus on adaptive surrogate-based approaches
                    https://tel.archives-ouvertes.fr/tel-01737299/document

            Args:
                problem
                individual which is optimal
            Return:
                vector: converged design point
                reliability_index
        """
        convergence = False
        tol = 1e-3
        mean = np.random.uniform(0, 10, len(problem.parameters))
        std = np.random.uniform(0, 10, len(problem.parameters))

        mu_g = problem.evaluate(individual)
        grad_g_x = np.array(derivative(problem, mean))
        sig_g = std_linear(grad_g_x, std)
        # reliability_index
        reliability_index = mu_g / sig_g
        alpha = - grad_g_x * std / sig_g

        # Initialize design points
        vector = mean + reliability_index * std * alpha

        while not convergence:
            transform_individuals = (vector - mean) / std

            # compute gradient of g with respect to z
            grad_g_x = derivative(problem, vector)
            grad_g_z = grad_g_x * std

            beta_previous = reliability_index
            reliability_index = (problem.evaluate(Individual(vector)) - grad_g_z @ transform_individuals) \
                                / np.linalg.norm(grad_g_z)
            alpha = - grad_g_z / np.linalg.norm(grad_g_z)

            # update design points in standard space
            transform_individuals = alpha * reliability_index
            # transform to physical space
            physical_transform = mean + transform_individuals * std

            condition1 = np.linalg.norm(physical_transform - vector) \
                         / np.linalg.norm(physical_transform) < tol
            condition2 = abs(np.round(reliability_index, 3) - np.round(beta_previous, 3)) < tol
            if condition2 or condition1:
                convergence = True
            if not convergence:
                vector = physical_transform

        return vector, reliability_index
