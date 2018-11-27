from .problem import Problem
from .algorithm import Algorithm
from .population import Population, Population_Genetic
from .individual import Individual_NSGA_II, Individual
from copy import copy
from abc import ABCMeta, abstractmethod
import random, time


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.problem = problem

    def gen_initial_population(self):
        pass

    def select(self):
        pass

    def form_new_population(self):
        pass

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.parameters_length = len(self.problem.parameters)
        self.current_population = 0

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=10, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='max_population_size')

    def gen_initial_population(self):
        population = Population(self.problem)
        population.gen_random_population(self.population_size, self.parameters_length, self.problem.parameters)
        population.evaluate()

        self.problem.add_population(population)

        self.current_population += 1
        return population

    def select(self):
        pass

    def form_new_population(self):
        pass

    def run(self):
        pass


class NSGA_II(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.9, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.05, lower=0,
                             desc='prob_mutation')

    def gen_initial_population(self):
        population = Population_Genetic(self.problem)
        population.gen_random_population(self.options['max_population_size'],
                                         self.parameters_length,
                                         self.problem.parameters)
        self.problem.populations.append(population)

    def is_dominate(self, p, q):
        """
        :param p: current solution
        :param q: candidate
        :return: True if the candidate is better than the current solution
        """
        dominate = False

        # First check the constraints
        # general evolutionary algorithms
        #if p.feasible != 0.0:
        #    if q.feasible != 0:
        #        if p.feasible < q.feasible:
        #            return False
        #        else:
        #            return True
        #    else:
        #        return True # the candicate is feasible
        #else:
        #    if q.feasible < 0:
        #        return False

        # The cost function can be a float or a list of floats
        for i in range(0, len(self.problem.costs)):
            if p.costs[i] > q.costs[i]:
                return False
            if p.costs[i] < q.costs[i]:
                dominate = True
        return dominate

    def crossover(self):
        pass

    def mutate(self):
        pass

    def fast_non_dominated_sort(self, population):
        pareto_front = []
        front_number = 1

        for p in population:
            for q in population:
                if p is q:
                    continue
                if self.is_dominate(p, q):
                    p.dominate.add(q)
                elif self.is_dominate(q, p):
                    p.domination_counter = p.domination_counter + 1

            if p.domination_counter == 0:
                p.front_number = front_number
                pareto_front.append(p)

        while not len(pareto_front) == 0:
            front_number += 1
            temp_set = []
            for p in pareto_front:
                for q in p.dominate:
                    q.domination_counter -= 1
                    if q.domination_counter == 0 and q.front_number == 0:
                        q.front_number = front_number
                        temp_set.append(q)
            pareto_front = temp_set

    @staticmethod
    def sort_by_coordinate(population, dim):

        population.sort(key = lambda x: x.parameters[dim])
        return population

    def calculate_crowd_dis(self, population):
        infinite = float("inf")

        for dim in range(0, len(self.problem.parameters)):
            new_list = self.sort_by_coordinate(population, dim)

            new_list[0].crowding_distance += infinite
            new_list[-1].crowding_distance += infinite
            max_distance = new_list[0].parameters[dim] - new_list[-1].parameters[dim]
            for i in range(1, len(new_list) - 1):
                distance = new_list[i - 1].parameters[dim] - new_list[i + 1].parameters[dim]
                if max_distance == 0:
                    new_list[i].crowding_distance = 0
                else:
                    new_list[i].crowding_distance += distance / max_distance

        for p in population:
            p.crowding_distance = p.crowding_distance / len(self.problem.parameters)

    @staticmethod
    def tournament_select(parents, part_num=2):
        """
        Binary tournament selection:
        An individual is selected in the rank is lesser than the other or if crowding distance is greater than the other
        """

        participants = random.sample(parents, part_num)
        return min(participants, key= lambda x: (x.front_number, -x.crowding_distance))


    def generate(self, parents):
        """ generate two children from two different parents """
        children = []
        while len(children) < self.options['max_population_size']:

            parent1 = self.tournament_select(parents)
            parent2 = self.tournament_select(parents)

            while parent1 == parent2:
                parent2 = self.tournament_select(parents)

            child1, child2 = self.cross(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            children.append(child1)
            children.append(child2)

        return children.copy()

    def cross(self, p1, p2):
        """ the random linear operator """
        if random.uniform(0, 1) >= self.options['prob_cross']:
            return p1, p2

        parameter1, parameter2 = [], []
        linear_range = 2

        alpha = random.uniform(0, linear_range)

        for i, param in enumerate(self.problem.parameters.items()):

            l_b = param[1]['bounds'][0]
            u_b = param[1]['bounds'][1]

            parameter1.append(self.clip(alpha*p1.parameters[i]+(1-alpha)*p2.parameters[i], l_b, u_b))
            parameter2.append(self.clip((1 - alpha)*p1.parameters[i]+alpha*p2.parameters[i], l_b, u_b))

        c1 = Individual_NSGA_II(parameter1, self.problem)
        c2 = Individual_NSGA_II(parameter2, self.problem)
        return c1, c2

    @staticmethod
    def clip(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    def mutation(self, p):
        """ uniform random mutation """
        mutation_space = 0.1
        parameters = []

        for i, parameter in enumerate(self.problem.parameters.items()):
            if random.uniform(0, 1) < self.options['prob_mutation']:

                l_b = parameter[1]['bounds'][0]
                u_b = parameter[1]['bounds'][1]

                para_range = mutation_space * (u_b - l_b)
                mutation = random.uniform(-para_range, para_range)
                parameters.append(self.clip(p.parameters[i] + mutation, l_b, u_b))
            else:
                parameters.append(p.parameters[i])

        p_new = Individual_NSGA_II(parameters, self.problem)
        return p_new

    def select(self):
        pass

    def form_new_population(self):
        pass

    def run(self):
        self.gen_initial_population()
        offsprings = self.problem.populations[0].individuals

        t_s = time.time()
        for it in range(self.options['max_population_number']):
            population = Population_Genetic(self.problem, offsprings)

            population.evaluate() # evaluate the offsprings

            # non-dominated truncate on the guys
            self.fast_non_dominated_sort(population.individuals)
            self.calculate_crowd_dis(offsprings)

            offsprings.extend(self.problem.populations[it].individuals)  # add the parents to the offsprings
            parents = sorted(offsprings, key=lambda x: x.front_number)

            # truncate
            self.problem.populations[it].individuals = parents[:self.options['max_population_size']]
            self.problem.add_population(population)

            offsprings = self.generate(self.problem.populations[it].individuals)

        t = time.time() - t_s
        print('Elapsed time:', t)

class EpsMOEA(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="EpsMOEA"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.9, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.05, lower=0,
                             desc='prob_mutation')

    def gen_initial_population(self):
        population = Population_Genetic(self.problem)
        population.gen_random_population(self.options['max_population_size'],
                                         self.parameters_length,
                                         self.problem.parameters)
        self.problem.populations.append(population)

    def pop_select(self, p, q):
        """
        Randomly mates two individuals from the population (p,q) and selects the dominating subject.
        If no dominance exist, select the second one (this is arbitrary).

        :param p: assumes that p is the optimal
        :param q: is the candidate
        :return: the subject which is selected for breeding
        """

        # returns back p if this is the dominating
        if self.is_dominate(p,q):
            return p

        if self.is_dominate(q, p):
            return q

        # if there is no dominating solution exist, returns back the second
        return q

    def random_selector(self, parents):
        """
        Selects an individual from the parents for breeding. Currently selects randomly.
        :param parents:
        :return: returns the selected individual
        """
        return random.sample(parents)

    def is_dominate(self, p, q):
        """
        :param p: candidate
        :param q: current solution
        :return: True if the candidate is better than the current solution
        """

        # The cost function can be a float or a list of floats
        for i in range(0, len(self.problem.costs)):
            if p.costs[i] > q.costs[i]:
                return False
            if p.costs[i] < q.costs[i]:
                dominate = True
        return dominate

    def pareto_dominance(self, p, q):
        """
        Pareto dominance comparison with constraint check.

        If either solution violates constraints, then the solution with a smaller
        constraint violation is preferred.  If both solutions are feasible, then
        Pareto dominance is used to select the preferred solution.

        :param p, q: individuals
        :return: 0 - no dominance, 1 - p is dominating, 2 - q is dominating
        """

        # First check the constraint violations
        if p.feasible != 0.0:
            if q.feasible != 0.0:
                if abs(p.feasible) < abs(q.feasible):
                    return 1
                else:
                    return 2
            else:
                return 2
        else:
            if q.feasible != 0.0:
                return 1

        # Then the pareto dominance

        dominate_p = False
        dominate_q = False

        # The cost function can be a float or a list of floats
        for i in range(0, len(self.problem.costs)):
            if p.costs[i] > q.costs[i]:
                dominate_q = True

                if dominate_p:
                    return 0
            if p.costs[i] < q.costs[i]:
                dominate_p = True

                if dominate_q:
                    return 0

        if dominate_q == dominate_p:
            return 0
        elif dominate_p:
            return 1
        else:
            return 2

    def crossover(self):
        pass

    def mutate(self):
        pass

    def run(self):

        # initialize the first population
        self.gen_initial_population()
        population = self.problem.populations[0].individuals
        population.evaluate()   # initial fitness

        for it in range(self.options['max_population_number']):



            #
            # population = Population_Genetic(self.problem, offsprings)
            #
            # population.evaluate() # evaluate the offsprings
            #
            # # non-dominated truncate on the guys
            # #self.fast_non_dominated_sort(population.individuals)
            # #self.calculate_crowd_dis(offsprings)
            #
            # offsprings.extend(self.problem.populations[it].individuals)  # add the parents to the offsprings
            # parents = sorted(offsprings, key=lambda x: x.front_number)
            # random.shuffle(parents)
            # # truncate
            # self.problem.populations[it].individuals = parents[:self.options['max_population_size']]
            # self.problem.add_population(population)
            #
            # offsprings = self.generate(self.problem.populations[it].individuals)