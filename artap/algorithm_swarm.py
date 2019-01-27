from random import random, randint
from .problem import Problem
from .population import Population
from .individual import Individual
from .algorithm_genetic import NSGAII

import time


class PSO(NSGAII):

    def __init__(self, problem: Problem, name="NSGA_II Evolutionary Algorithm"):
        super().__init__(problem, name)
        self.w = 0.1  # constant inertia weight (how much to weigh the previous velocity)
        self.c1 = 2  # cognitive constant
        self.c2 = 1   # social constant
        self.n = self.options['max_population_size']
        self.err_best_g = [-1]  # best error for group
        self.pos_best_g = []  # best position for group

    # TODO: Almost the same code as for genetic algorithm. Reuse.
    def gen_initial_population(self):
        super().gen_initial_population()
        self.evaluate_population()
        for individual in self.population.individuals:
            self.evaluate_pso(individual)

    # evaluate current fitness
    def evaluate_pso(self, individual):

        dominates = True

        for i in range(len(individual.best_costs)):
            if individual.costs[i] > individual.best_costs[i]:
                dominates = False

        # check to see if the current position is an individual best
        if dominates:
            individual.best_vector = individual.vector
            individual.best_costs = individual.costs

    # update new particle velocity
    def update_velocity(self, individual):

        for i in range(0, len(individual.vector)):
            r1 = random()
            r2 = random()

            vel_cognitive = self.c1 * r1 * (individual.best_vector[i] - individual.vector[i])
            vel_social = self.c2 * r2 * (self.pos_best_g[i] - individual.vector[i])
            individual.velocity_i[i] = self.w * individual.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, individual, bounds):
        for i in range(0, len(individual.vector)):
            individual.vector[i] = individual.vector[i] + individual.velocity_i[i]

            # adjust maximum position if necessary
            if individual.vector[i] > bounds[i][1]:
                individual.vector[i] = bounds[i][1]

            # adjust minimum position if necessary
            if individual.vector[i] < bounds[i][0]:
                individual.vector[i] = bounds[i][0]

    def run(self):
        self.gen_initial_population()
        self.fast_non_dominated_sort(self.population.individuals)
        self.problem.data_store.write_population(self.population)

        t_s = time.time()
        self.problem.logger.info("PSO: {}/{}".format(self.options['max_population_number'],
                                                     self.options['max_population_size']))

        i = 0
        while i < self.options['max_population_number']:
            population = Population()

            pareto_front = []
            for j in range(self.options['max_population_size']):
                if self.population.individuals[j].front_number == 1:
                    pareto_front.append(self.population.individuals[j])
                individual = Individual(self.population.individuals[j].vector.copy())
                individual.best_vector = self.population.individuals[j].best_vector
                individual.best_costs = self.population.individuals[j].best_costs
                individual.costs = self.population.individuals[j].costs

                population.individuals.append(individual)
            self.population = population

            index = randint(0, len(pareto_front)-1)  # takes random individual from Pareto front
            individual = pareto_front[index]
            self.pos_best_g = list(individual.vector)
            self.err_best_g = individual.costs

            for individual in self.population.individuals:
                individual.costs = []
                # print(individual.velocity_i)
                self.update_velocity(individual)
                # print(individual.velocity_i)
                # print("---------------------")
                # print(individual.vector)
                self.update_position(individual, self.problem.get_bounds())
                # print(individual.vector)
                # print("---------------------")

            self.evaluate_population()
            for individual in self.population.individuals:
                self.evaluate_pso(individual)
            self.fast_non_dominated_sort(self.population.individuals)
            self.problem.data_store.write_population(self.population)

            i += 1

        t = time.time() - t_s
        self.problem.logger.info("PSO: elapsed time: {} s".format(t))
