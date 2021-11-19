import numpy as np
from .algorithm import Algorithm
from .problem import Problem
import sys
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .individual import Individual
from artap.operators import RandomGenerator
from artap.benchmark_functions import BenchmarkFunction as bm
import time


class Monte_Carlo(Algorithm):
    """
    Monte Carlo simulation
        1) make a list of random values of x
        2) pick a small number of random value of x
        3) evaluate the objective function
        4) pick the lowest
    """
    def __init__(self, problem: Problem, n):
        super().__init__(problem)
        self.evaluation = 0
        self.z_min, self.z_max = 0, 1
        self.dimension = 1
        self.n = n  # number of divisions
        self.sampling_size = 10  # 1000 sampling points in each division
        self.problem = problem
        self.problem.parameters = bm.generate_paramlist(self, dimension=self.dimension, lb=0.0, ub=1.0)
        self.intervals = np.linspace(self.z_min, self.z_max, self.n)
        self.generator = RandomGenerator(self.problem.parameters)

    def generate(self):
        costs = []
        best_vector = []
        for _ in range(self.sampling_size):
            self.generator.init(self.n)
            self.individuals = self.generator.generate()
            self.evaluate(self.individuals)
            for individual in self.individuals:
                costs.append(individual.costs)
                best_vector.append(individual.vector)
                # for individual in self.individuals:
                # append to problem
                self.problem.individuals.append(individual)
                # add to population
                individual.population_id = 0

                self.problem.data_store.sync_individual(individual)
        costs = np.array(costs).reshape(-1, 1)
        best_vector = np.array(best_vector).reshape(-1, 1)
        return costs, best_vector

    def simulate(self):
        var_array = []
        I_array = []
        for i in range(self.n - 1):
            # random sampling in each of the interval
            costs, vectors = self.generate()
            I_array.append(min(costs))  # add up the integral value
            index = np.argmin(costs)
            var_array.append(vectors[index])

        return I_array, var_array

    def run(self):
        I_array, var_array = self.simulate()
        self.evaluation += (len(self.intervals) - 1) * self.sampling_size
        new_I = min(I_array)
        index = np.argmin(I_array)
        new_var = var_array[index]
        relative_accuracy = 1  # assign a non-zero value of initial relative accuracy
        while relative_accuracy >= 1e-2:
            old_I = new_I
            I_array, var_array = self.simulate()
            new_I = min(I_array)
            index = np.argmin(I_array)
            new_var = var_array[index]
            # calculate relative accuracy
            relative_accuracy = abs((new_I - old_I) / old_I)

        for i in range(self.n - 1):
            for individual in self.individuals:
                # add to population
                individual.population_id = i + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)

        return new_I, new_var


class Integral_Monte_Carlo(Algorithm):
    """
    Adaptive Monte Carlo Integral Approximation.
    Summation is used to estimate the expected value of a function under a distribution, instead of integration.
    """
    def __init__(self, problem: Problem, n):
        super().__init__(problem)
        self.evaluation = 0
        self.z_min, self.z_max = 0, 1
        self.dimension = 1
        self.n = n  # number of divisions
        self.sampling_size = 10  # 1000 sampling points in each division
        self.problem = problem
        self.problem.parameters = bm.generate_paramlist(self, dimension=self.dimension, lb=0.0, ub=1.0)
        self.intervals = np.linspace(self.z_min, self.z_max, self.n)
        self.generator = RandomGenerator(self.problem.parameters)

    def generate(self):
        elements = []
        for _ in range(self.sampling_size):
            self.generator.init(self.n)
            self.individuals = self.generator.generate()
            self.evaluate(self.individuals)
            for individual in self.individuals:
                elements.append(individual.costs)
                # append to problem
                self.problem.individuals.append(individual)
                # add to population
                individual.population_id = 0

                self.problem.data_store.sync_individual(individual)
        elements = np.array(elements).reshape(-1, 1)
        return elements

    def simulate(self):
        var_array = []
        I_array = []
        for i in range(self.n - 1):
            # random sampling in each of the interval
            elements = self.generate()
            # integral of segment of integration
            average = sum(elements) / self.sampling_size
            # weight of integral is correspond to the width of the sub-interval
            weight = self.intervals[i + 1] - self.intervals[i]
            I_array.append(weight * average)  # add up the integral value
            # calculate the variance of this segment of integration
            var = sum((elements[i] - average) ** 2 for i in range(self.sampling_size))
            var_array.append(var)  # add variance to the array
        # return the integral value and variance of each sub-interval in an
        # array
        return I_array, var_array

    def run(self):
        I_array, var_array = self.simulate()
        self.evaluation += (len(self.intervals) - 1) * self.sampling_size
        new_I = sum(I_array)
        relative_accuracy = 1  # assign a non-zero value of initial relative accuracy
        while relative_accuracy >= 1e-2:
            old_I = new_I
            # adaption
            # find the index of the largest variance
            largest_var_index = var_array.index(max(var_array))
            # removing the result of section with largest variance
            I_array = np.delete(I_array, largest_var_index)
            var_array = np.delete(var_array, largest_var_index)
            # divide sub-interval with the largest variance into 10 more
            # sub-intervals
            self.intervals = np.insert(self.intervals,
                                       largest_var_index + 1,
                                       np.linspace(self.intervals[largest_var_index],
                                                   self.intervals[largest_var_index + 1],
                                                   self.n,
                                                   endpoint=False))
            self.intervals = np.delete(self.intervals, largest_var_index)
            # run Monte Carlo in the new intervals
            I_array, var_array = self.simulate()
            new_I = sum(I_array)
            # calculate relative accuracy
            relative_accuracy = abs((new_I - old_I) / old_I)
            # amount of evaluations increases by the number of intervals * random
            # points in each interval
            self.evaluation += (len(self.intervals) - 1) * self.sampling_size
            # print((len(intervals)-1)*sampling_size,new_I,relative_accuracy)    #
            # show realtime evaluations
        err = 0
        for i in range(self.n - 1):
            # sum up the variance of each interval
            err += ((self.intervals[i + 1] - self.intervals[i]) /
                    (self.z_max - self.z_min)) ** 2 * var_array[i]

            for individual in self.individuals:
                # add to population
                individual.population_id = i + 1
                # append to problem
                self.problem.individuals.append(individual)
                # sync to datastore
                self.problem.data_store.sync_individual(individual)
        # divide the standard deviation by sqrt of n to get standard error (error
        # of estimation)

        err = np.sqrt(err / (len(self.intervals) * self.sampling_size))
        return self.evaluation, new_I
