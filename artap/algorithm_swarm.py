from random import random
# import math
from .problem import Problem
# from .algorithm import Algorithm
from .population import Population
from .individual import Individual
from .algorithm_genetic import NSGA_II


class PSO(NSGA_II):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.w = 0.1  # constant inertia weight (how much to weigh the previous velocity)
        self.c1 = 2  # cognitive constant
        self.c2 = 1   # social constant
        self.n = self.options['max_population_size']
        self.err_best_g = -1  # best error for group
        self.pos_best_g = []  # best position for group

    # TODO: Almost the same code as for genetic algorithm. Reuse.
    def gen_initial_population(self):
        super().gen_initial_population()
        population = self.problem.populations[-1]
        population.evaluate()
        for individual in population.individuals:
            self.evaluate_pso(individual)

    # evaluate current fitness
    def evaluate_pso(self, individual):
        individual.err_i = individual.costs[0]  # TODO: Only for one objective function - generalize

        # check to see if the current position is an individual best
        if individual.err_i < individual.best_costs or individual.best_costs == -1:
            individual.best_parameters = individual.parameters
            individual.best_costs = individual.err_i

    # update new particle velocity
    def update_velocity(self, individual):

        for i in range(0, len(individual.parameters)):
            r1 = random()
            r2 = random()

            vel_cognitive = self.c1 * r1 * (individual.best_parameters[i] - individual.parameters[i])
            vel_social = self.c2 * r2 * (self.pos_best_g[i] - individual.parameters[i])
            individual.velocity_i[i] = self.w * individual.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, individual, bounds):
        for i in range(0, len(individual.parameters)):
            individual.parameters[i] = individual.parameters[i] + individual.velocity_i[i]

            # adjust maximum position if necessary
            if individual.parameters[i] > bounds[i][1]:
                individual.parameters[i] = bounds[i][1]

            # adjust minimum position if necessary
            if individual.parameters[i] < bounds[i][0]:
                individual.parameters[i] = bounds[i][0]

    def run(self):
        self.gen_initial_population()
        self.fast_non_dominated_sort(self.problem.populations[-1].individuals)
        i = 0
        while i < self.options['max_population_number']:
            print(i, self.err_best_g)
            print(i, self.pos_best_g)
            population = Population(self.problem)

            for j in range(self.n):
                individual = Individual(self.problem.populations[-1].individuals[j].parameters.copy(), self.problem)
                individual.best_parameters = self.problem.populations[-1].individuals[j].best_parameters
                individual.best_costs = self.problem.populations[-1].individuals[j].best_costs
                individual.costs = self.problem.populations[-1].individuals[j].costs
                population.individuals.append(individual)

            for individual in population.individuals:
                if individual.costs[0] < self.err_best_g or self.err_best_g == -1:
                    self.pos_best_g = list(individual.parameters)
                    self.err_best_g = float(individual.costs[0])

            for individual in population.individuals:
                individual.costs = []
                # print(individual.velocity_i)
                self.update_velocity(individual)
                # print(individual.velocity_i)
                # print("---------------------")
                # print(individual.parameters)
                self.update_position(individual, self.problem.get_bounds())
                # print(individual.parameters)
                # print("---------------------")

            population.evaluate()
            for individual in population.individuals:
                self.evaluate_pso(individual)

            self.problem.add_population(population)
            i += 1
