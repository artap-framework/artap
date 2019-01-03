# import random
# import math
from .problem import Problem
# from .algorithm import Algorithm
from .population import Population
from .individual import Individual
from .algorithm_genetic import GeneticAlgorithm


class PSO(GeneticAlgorithm):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)

    # TODO: The same code as for genetic algorithm. Reuse.
    def gen_initial_population(self):
        population = Population(self.problem)
        population.gen_random_population(self.options['max_population_size'],
                                         self.parameters_length,
                                         self.problem.parameters)
        population.evaluate()
        for individual in population.individuals:
            individual.evaluate_pso()
        self.problem.populations.append(population)

    def run(self):
        self.gen_initial_population()
        n = self.options['max_population_size']
        err_best_g = -1  # best error for group
        pos_best_g = []  # best position for group

        i = 0
        while i < self.options['max_population_number']:
            print(i, err_best_g)
            print(i, pos_best_g)
            population = Population(self.problem)

            for j in range(n):
                individual = Individual(self.problem.populations[-1].individuals[j].parameters.copy(), self.problem)
                individual.pos_best_i = self.problem.populations[-1].individuals[j].pos_best_i
                individual.err_best_i = self.problem.populations[-1].individuals[j].err_best_i
                individual.costs = self.problem.populations[-1].individuals[j].costs
                population.individuals.append(individual)

            for individual in population.individuals:
                if individual.costs[0] < err_best_g or err_best_g == -1:
                    pos_best_g = list(individual.parameters)
                    err_best_g = float(individual.costs[0])

            for individual in population.individuals:
                individual.costs = []
                # print(individual.velocity_i)
                individual.update_velocity(pos_best_g)
                # print(individual.velocity_i)
                # print("---------------------")
                # print(individual.parameters)
                individual.update_position(self.problem.get_bounds())
                # print(individual.parameters)
                # print("---------------------")

            population.evaluate()
            for individual in population.individuals:
                individual.evaluate_pso()

            self.problem.add_population(population)
            i += 1
