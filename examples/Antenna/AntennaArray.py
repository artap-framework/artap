import matplotlib.pyplot as plt
import numpy as np
from artap.algorithm_genetic import NSGAII
import pandas as pd
from artap.algorithm_swarm import PSOGA, SMPSO, OMOPSO
from artap.problem import Problem
from artap.results import Results
from scipy.signal import argrelextrema
from artap.datastore import SqliteDataStore


class AntennaArray:

    def __init__(self, nx, ny):
        self.c = 3e8
        self.f = 6e9
        self.lambda_0 = self.c / self.f
        self.k_0 = 2 * np.pi / self.lambda_0

        self.d_x = self.lambda_0 / 2
        self.d_y = self.lambda_0 / 2

        self.n_x = nx
        self.n_y = ny

        self.n_phi = 18
        self.n_theta = 18
        self.phi = np.linspace(-np.pi, np.pi, self.n_phi+1)
        self.theta = np.linspace(-np.pi / 2, np.pi / 2, self.n_theta+1)
        self.phi_r = 0
        self.theta_r = -10
        self.phi_index = int((self.phi_r + 180) * self.n_phi / 360)
        self.theta_index = int((self.theta_r + 90) * self.n_theta / 180)
        self.S = np.zeros([self.n_phi, self.n_theta], dtype=complex)
        self.I = np.zeros([self.n_x, self.n_y], dtype=complex)

    def set_inputs(self, vector):
        k = 0
        for i in range(self.n_x):
            for j in range(self.n_y):
                self.I[i, j] = vector[k] * (np.cos(vector[k + 1])
                                            + 1j * np.sin(vector[k + 1]))
                k += 2

    def array_factor(self, individual):
        self.set_inputs(individual.vector)
        self.S = np.zeros([self.n_phi+1, self.n_theta+1], dtype=complex)
        for l in range(self.n_phi + 1):
            for k in range(self.n_theta + 1):
                for i in range(0, self.n_x):
                    for j in range(0, self.n_y):
                        self.S[k, l] += self.I[i, j] * np.exp(1j * (self.k_0 * (i + 1) * self.d_x * np.sin(self.theta[l]) *
                                                          np.cos(self.phi[k]) + self.k_0 * (j + 1) * self.d_y *
                                                          np.sin(self.theta[l]) * np.sin(self.phi[k]))) * 1 / self.n_x / self.n_y

    def calculate(self):
        # Initialization of the problem
        self.problem = AntennaArrayProblem()
        print(self.problem)
        self.problem.antenna = self
        self.database_name = "database.sqlite"
        self.problem.data_store = SqliteDataStore(self.problem, database_name=self.database_name)

        # Perform the optimization iterating over 100 times on 100 individuals.
        algorithm = NSGAII(self.problem)
        algorithm.options['max_population_number'] = 10
        algorithm.options['max_population_size'] = 10
        algorithm.run()

    def process_results(self):
        # Post - processing the results
        # reads in the result values into the b, results class
        self.problem = AntennaArrayProblem()
        database_name = "database.sqlite"
        self.problem.data_store = SqliteDataStore(self.problem, database_name=database_name)
        b = Results(self.problem)
        pareto = []
        pareto_vector = []
        last_population = b.population(0)
        print(last_population)
        for individual in last_population:
            # print(individual.features['front_number'])
            if individual.features['front_number'] != 0:
                plt.plot(individual.costs[0], individual.costs[1], 'o')
                pareto.append(individual)
                pareto_vector.append(individual.vector)

        print(f'pareto: {pareto}')
        plt.xlabel("$f_1(x)$ - Error")
        plt.ylabel("$f_2(x)$ - Maximum size")

        df = pd.DataFrame(pareto_vector)
        df.to_csv('dataframe.csv', index=False)
        self.evaluate(pareto[0])

        # fig = plt.figure()
        # ax = fig.gca(projection='3d')
        # X, Y = np.meshgrid(phi / np.pi * 180, theta / np.pi * 180)
        # urf = ax.plot_surface(X, Y, 20*np.log(abs(S)), cmap=cm.coolwarm,
        #                       linewidth=0, antialiased=False)
        # plt.xlabel(r'$\Phi$')
        # plt.ylabel(r'$\Theta$')

        plt.figure()
        plt.plot(self.theta / np.pi * 180,
                 abs(self.S[self.phi_r, :]))
        plt.grid()
        plt.show()

        s = b.pareto_plot()
        plt.show()

    def evaluate(self, individual):
        self.array_factor(individual)
        peaks = []
        maxims = argrelextrema(self.S[self.phi_index, :], np.less)
        for maxim in maxims[0]:
            peaks.append([self.phi_index, maxim])

        maxims = argrelextrema(self.S[self.theta_index, :], np.less)
        for maxim in maxims[0]:
            peaks.append([maxim, self.theta_index])

        peak_r = abs(self.S[self.phi_index, self.theta_index])

        diff = 0
        for peak in peaks:
            diff += (peak_r - abs(self.S[peak[0], peak[1]])) ** 2

        f_1 = peak_r
        f_2 = diff
        return [f_1, f_2]


class AntennaArrayProblem(Problem):

    def set(self):

        # Not mandatory to give a name for the test problem
        self.name = 'Antenna array'

        self.parameters = [{'name': 'I_1', 'bounds': [0, 1], 'parameter_type':'float'},
                           {'name': 'alpha_1', 'bounds': [-np.pi, np.pi], 'parameter_type': 'float'},
                           {'name': 'I_2', 'bounds': [0, 1], 'parameter_type': 'float'},
                           {'name': 'alpha_2', 'bounds': [-np.pi, np.pi], 'parameter_type': 'float'},
                           {'name': 'I_3', 'bounds': [0, 1], 'parameter_type': 'float'},
                           {'name': 'alpha_3', 'bounds': [-np.pi, np.pi], 'parameter_type': 'float'},
                           {'name': 'I_4', 'bounds': [0, 1], 'parameter_type': 'float'},
                           {'name': 'alpha_4', 'bounds': [-np.pi, np.pi], 'parameter_type': 'float'},
                           ]

        # The two, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'f_1', 'criteria': 'maximize'},
                      {'name': 'f_2', 'criteria': 'maximize'}]

    def evaluate(self, individual):
        return self.antenna.evaluate(individual)


antenna = AntennaArray(4, 1)
antenna.calculate()
antenna.process_results()

