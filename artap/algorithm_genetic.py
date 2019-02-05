from .problem import Problem
from .algorithm import Algorithm
from .population import Population
# from .individual import Individual
from .operators import RandomGeneration, SimpleCrossover, SimulatedBinaryCrossover, SimpleMutation, PmMutation, TournamentSelection, Selection
# from copy import copy, deepcopy
# from abc import ABCMeta
# import random
import time
# import itertools
# from numpy.random import random_integers
import sys
# import math

EPSILON = sys.float_info.epsilon


class GeneralEvolutionaryAlgorithm(Algorithm):
    """ Basis Class for evolutionary algorithms """

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.problem = problem

        self.generator = RandomGeneration(self.problem.parameters)
        self.selector = None
        self.mutator = None
        self.crossover = None

    def gen_initial_population(self):
        pass

    def run(self):
        pass


class GeneticAlgorithm(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="General Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.parameters_length = len(self.problem.parameters)

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='max_population_number', default=10, lower=1,
                             desc='max_population_number')
        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='max_population_size')

    def gen_initial_population(self):
        individuals = self.generator.generate(self.options['max_population_size'])
        self.evaluate(individuals)

        population = Population(individuals)
        return population

    def run(self):
        pass


class NSGAII(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

        self.options.declare(name='prob_cross', default=0.9, lower=0,
                             desc='prob_cross')
        self.options.declare(name='prob_mutation', default=0.05, lower=0,
                             desc='prob_mutation')

    def generate(self, parents):
        """ generate two children from two different parents """

        children = []
        while len(children) < self.options['max_population_size']:
            parent1 = self.selector.select(parents)
            parent2 = self.selector.select(parents)

            while parent1 == parent2:
                parent2 = self.selector.select(parents)

            # crossover
            child1, child2 = self.crossover.cross(parent1, parent2)

            # mutation
            child1 = self.mutator.mutate(child1)
            child2 = self.mutator.mutate(child2)

            children.append(child1)
            children.append(child2)

        return children.copy()

    def run(self):
        # set class
        # self.crossover = SimpleCrossover(self.problem.parameters, self.options['prob_cross'])
        self.crossover = SimulatedBinaryCrossover(self.problem.parameters, self.options['prob_cross'])
        # self.mutator = SimpleMutation(self.problem.parameters, self.options['prob_mutation'])
        self.mutator = PmMutation(self.problem.parameters, self.options['prob_mutation'])
        self.selector = TournamentSelection(self.problem.parameters)

        self.population = self.gen_initial_population()
        self.problem.data_store.write_population(self.population)

        offsprings = self.population.individuals

        t_s = time.time()
        self.problem.logger.info("NSGA_II: {}/{}".format(self.options['max_population_number'],
                                                         self.options['max_population_size']))

        # optimization
        for it in range(self.options['max_population_number']):
            self.population = Population(offsprings)
            self.population.individuals = self.evaluate(self.population.individuals)

            # non-dominated sort of individuals
            self.selector.non_dominated_sort(self.population.individuals)
            self.selector.crowding_distance(offsprings)

            self.problem.data_store.write_population(self.population)
            offsprings.extend(self.problem.data_store.populations[it].individuals)  # add the parents to the offsprings
            parents = sorted(offsprings, key=lambda x: x.front_number)

            # truncate
            self.problem.data_store.populations[it].individuals = parents[:self.options['max_population_size']]

            offsprings = self.generate(self.problem.data_store.populations[it].individuals)

            time.sleep(1)

        t = time.time() - t_s
        self.problem.logger.info("NSGA_II: elapsed time: {} s".format(t))

# class Archive(object):
#     """An archive only containing non-dominated solutions."""
#
#     def __init__(self, dominance=ParetoDominance()):
#         super(Archive, self).__init__()
#         self._dominance = dominance
#         self._contents = []
#
#     def add(self, solution):
#         flags = [self._dominance.compare(solution, s) for s in self._contents]
#         dominates = [x > 0 for x in flags]
#         nondominated = [x == 0 for x in flags]
#
#         if any(dominates):
#             return False
#         else:
#             self._contents = list(itertools.compress(self._contents, nondominated)) + [solution]
#             return True
#
#     def append(self, solution):
#         self.add(solution)
#
#     def extend(self, solutions):
#         for solution in solutions:
#             self.append(solution)
#
#     def remove(self, solution):
#         try:
#             self._contents.remove(solution)
#             return True
#         except ValueError:
#             return False
#
#     def __len__(self):
#         return len(self._contents)
#
#     def __getitem__(self, key):
#         return self._contents[key]
#
#     def __iadd__(self, other):
#         if hasattr(other, "__iter__"):
#             for o in other:
#                 self.add(o)
#         else:
#             self.add(other)
#
#         return self
#
#     def __iter__(self):
#         return iter(self._contents)


# class EpsMOEA(GeneticAlgorithm):
#
#     def __init__(self, problem: Problem, name="EpsMOEA"):
#         super().__init__(problem, name)
#
#         self.options.declare(name='p_recomb', default=1.0, lower=0, desc='recombination_probability')
#         self.options.declare(name='dist_ind_sbx', default=15.0, lower=0, desc='distribution_index')
#         self.options.declare(name='p_mutation', default=1.0, lower=0, desc='mutation_probability')
#         self.options.declare(name='dist_ind_pm', default=20.0, lower=0, desc='mutation_distribution_index')
#
#         # self.archive =
#
#     def gen_initial_population(self):
#         population = Population()
#         population.gen_random_population(self.options['max_population_size'],
#                                          self.parameters_length,
#                                          self.problem.parameters)
#         self.populations.append(population)
#
#     def pop_select(self, population):
#         """
#         Randomly mates two individuals from the population (p,q) and selects the dominating subject.
#         If no dominance exist, select the second one (this is arbitrary).
#
#         :param population: the actual population
#         :return: the subject which is selected for breeding
#         """
#         compete = random_integers(0, len(population)-1, size=2)
#
#         p = population[compete[0]]
#         q = population[compete[1]]
#
#         # returns back p if this is the dominating
#         if self.is_dominate(p,q):
#             return p
#
#         if self.is_dominate(q,p):
#             return q
#
#         # if there is no dominating solution exist, returns back the second
#         return q
#
#     def random_selector(self, parents):
#         """
#         Selects an individual from the parents for breeding. Currently selects randomly.
#         It's a tournament selector
#         :param parents:
#         :return: returns the selected individual
#         """
#         return random.sample(parents)
#
#     def is_dominate(self, p, q):
#         """
#         :param p: candidate
#         :param q: current solution
#         :return: True if the candidate is better than the current solution
#         """
#
#         # The cost function can be a float or a list of floats
#         for i in range(0, len(self.problem.costs)):
#             if p.costs[i] > q.costs[i]:
#                 return False
#             if p.costs[i] < q.costs[i]:
#                 dominate = True
#         return dominate
#
#     def pareto_dominance_compare(self, p, q):
#         """
#         Pareto dominance comparison with constraint check.
#
#         If either solution violates constraints, then the solution with a smaller
#         constraint violation is preferred.  If both solutions are feasible, then
#         Pareto dominance is used to select the preferred solution.
#
#         :param p, q: individuals
#         :return: 0 - no dominance, 1 - p is dominating, 2 - q is dominating
#         """
#
#         # First check the constraint violations
#         if p.feasible != 0.0:
#             if q.feasible != 0.0:
#                 if abs(p.feasible) < abs(q.feasible):
#                     return 1
#                 else:
#                     return 2
#             else:
#                 return 2
#         else:
#             if q.feasible != 0.0:
#                 return 1
#
#         # Then the pareto dominance
#
#         dominate_p = False
#         dominate_q = False
#
#         # The cost function can be a float or a list of floats
#         for i in range(0, len(self.problem.costs)):
#             if p.costs[i] > q.costs[i]:
#                 dominate_q = True
#
#                 if dominate_p:
#                     return 0
#             if p.costs[i] < q.costs[i]:
#                 dominate_p = True
#
#                 if dominate_q:
#                     return 0
#
#         if dominate_q == dominate_p:
#             return 0
#         elif dominate_p:
#             return 1
#         else:
#             return 2
#
#     def pareto_front(self, population):
#         """
#         Given multiple fitness values of a population, find which individuals are in
#         the pareto-front(i.e. the non-dominated subset of the population.
#
#         :param population: list of the solutions
#         :return: an array which contains the information that which individual is in the pareto front
#         """
#
#         #archive = [False]*len(population)
#         archive = population
#
#         for i in range(len(population)):
#             for j in range(len(population)):
#                 if i != j:
#                     result = self.pareto_dominance(population[i], population[j])
#
#                     if result == 1:
#                        archive[i].isPareto = True
#                        if archive[j]:
#                            archive[j].isPareto = False
#
#                     if result == 2:
#                         archive[j].isPareto = True
#                         if archive[i]:
#                             archive[i].isPareto = False
#
#         return copy(archive)
#
#     def crossover(self):
#         # it uses the sbx
#         pass
#
#     def mutate(self, parent):
#         # polynomial mutation
#
#         child_param = copy.deepcopy(parent.parameters)
#         probability = self.options['p_mutation']
#
#         if isinstance(probability, int):
#             probability /= float(len(parent.parameters))
#
#         for i, param in enumerate(self.problem.parameters.items()):
#
#             lb = param[1]['bounds'][0]
#             ub = param[1]['bounds'][1]
#
#             if random.uniform(0.0, 1.0) <= probability:
#                 child_param[i] = self.pm_mutation(float(child_param[i]), lb, ub)
#
#         return Individual(child_param, self.problem)
#
#     def pm_mutation(self, x, lb, ub):
#         u = random.uniform(0, 1)
#         dx = ub - lb
#
#         if u < 0.5:
#             bl = (x - lb) / dx
#             b = 2.0 * u + (1.0 - 2.0 * u) * pow(1.0 - bl,  self.options['dist_ind_pm'] + 1.0)
#             delta = pow(b, 1.0 / (self.options['dist_ind_pm'] + 1.0)) - 1.0
#         else:
#             bu = (ub - x) / dx
#             b = 2.0 * (1.0 - u) + 2.0 * (u - 0.5) * pow(1.0 - bu, self.options['dist_ind_pm'] + 1.0)
#             delta = 1.0 - pow(b, 1.0 / (self.options['dist_ind_pm'] + 1.0))
#
#         x = x + delta * dx
#         x = self.clip(x, lb, ub)
#
#         return x
#
#     def sbx_crossover(self, x1, x2, lb, ub):
#         dx = x2 - x1
#
#         if dx > EPSILON:
#             if x2 > x1:
#                 y2 = x2
#                 y1 = x1
#             else:
#                 y2 = x1
#                 y1 = x2
#
#             beta = 1.0 / (1.0 + (2.0 * (y1 - lb) / (y2 - y1)))
#             alpha = 2.0 - pow(beta, self.options['dist_ind_sbx'] + 1.0)
#             rand = random.uniform(0.0, 1.0)
#
#             if rand <= 1.0 / alpha:
#                 alpha = alpha * rand
#                 betaq = pow(alpha, 1.0 / (self.options['dist_ind_sbx'] + 1.0))
#             else:
#                 alpha = alpha * rand
#                 alpha = 1.0 / (2.0 - alpha)
#                 betaq = pow(alpha, 1.0 / (self.options['dist_ind_sbx'] + 1.0))
#
#             x1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
#             beta = 1.0 / (1.0 + (2.0 * (ub - y2) / (y2 - y1)))
#             alpha = 2.0 - pow(beta, self.options['dist_ind_sbx'] + 1.0)
#
#             if rand <= 1.0 / alpha:
#                 alpha = alpha * rand
#                 betaq = pow(alpha, 1.0 / (self.options['dist_ind_sbx'] + 1.0))
#             else:
#                 alpha = alpha * rand
#                 alpha = 1.0 / (2.0 - alpha)
#                 betaq = pow(alpha, 1.0 / (self.options['dist_ind_sbx'] + 1.0))
#
#             x2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))
#
#             # randomly swap the values
#             if bool(random.getrandbits(1)):
#                 x1, x2 = x2, x1
#
#             x1 = self.clip(x1, lb, ub)
#             x2 = self.clip(x2, lb, ub)
#
#         return x1, x2
#
#     def sbx(self, mama, papa):
#         """Create an offspring using simulated binary crossover.
#
#         :parameter mama, papa: - two breeders from the population, each a vector of genes.
#         :return:  a list with 2 offsprings each with the genotype of an  offspring after recombination and mutation.
#         """
#
#         cparam_a = deepcopy(mama.parameters)
#         cparam_b = deepcopy(papa.parameters)
#
#         if random.uniform(0.0, 1.0) <= self.options['p_recomb']:
#             for i, param in enumerate(self.problem.parameters.items()):
#
#                 x1 = cparam_a[i]
#                 x2 = cparam_b[i]
#
#                 lb = param[1]['bounds'][0]
#                 ub = param[1]['bounds'][1]
#
#                 x1, x2 = self.sbx_crossover(x1, x2, lb, ub)
#
#                 cparam_a.variables[i] = x1
#                 cparam_b.variables[i] = x2
#
#         offspring_a = Individual(cparam_a, self.problem)
#         offspring_b = Individual(cparam_b, self.problem)
#
#         return [offspring_a, offspring_b]
#
#     def breed(self, mama, papa):
#         """
#         >> Variator (crossover -> mutate)
#         Creates a new genome for a subject by recombination of parent genes, and possibly mutation of the result,
#         depending on the individuals's mutation resistance.
#
#         :parameter mama, papa: - two breeders from the population, each a vector of genes.
#         :return offspring: - a length-g array with the genotype of the offspring after recombination and mutation.
#         """
#
#         # Recombination place, using one-point crossover:
#         offsprings = self.sbx(mama, papa)
#         childs = []
#         # Possibly mutate:
#         for child in offsprings:
#
#             childs.append(self.mutate(child))
#
#         return deepcopy(childs)
#
#
#     @staticmethod
#     def clip(value, min_value, max_value):
#         return max(min_value, min(value, max_value))
#
#     def _add_to_population(self, solution, curr_population):
#         dominates = []
#         dominated = False
#
#         for i in range(len(curr_population)):
#             flag = self.pareto_dominance_compare(solution, curr_population[i])
#
#             if flag == 1:
#                 dominates.append(i) # 1 if the new solution is the dominant
#             elif flag == 2:
#                 dominated = True # 2 if the other solution is the dominant one
#
#         if len(dominates) > 0:
#             del curr_population[random.choice(dominates)]
#             curr_population.append(solution)
#         elif not dominated:
#             curr_population.remove(random.choice(self.population))
#             curr_population.append(solution)
#
#             return curr_population
#
#     def run(self):
#         # initialize the first population
#         self.gen_initial_population()
#         self.populations[0].evaluate()
#         curr_population = self.populations[0].individuals
#
#         # pareto values after the first iteration
#         archive = self.pareto_front(curr_population)
#
#         for it in range(self.options['max_population_number']):
#             mama = self.pop_select(curr_population)
#             papa = self.random_selector(archive)
#
#             offsprings = self.breed(mama,papa)
#
#             # evaluate all new childs
#
#             ch_population = Population(self.problem, offsprings)
#             ch_population.evaluate() # evaluate the offsprings
#
#             for child in ch_population.individuals:
#                 self._add_to_population(child)
#                 self.archive.add(child)
#
#             # # non-dominated truncate on the guys
#             # #self.fast_non_dominated_sort(population.individuals)
#             # #self.calculate_crowd_dis(offsprings)
#             #
#             # offsprings.extend(self.populations[it].individuals)  # add the parents to the offsprings
#             # parents = sorted(offsprings, key=lambda x: x.front_number)
#             # random.shuffle(parents)
#             # # truncate
#             # self.populations[it].individuals = parents[:self.options['max_population_size']]
#             # self.problem.add_population(population)
#             #
#             # offsprings = self.generate(self.populations[it].individuals)
