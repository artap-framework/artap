import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from utils import *
from artap.algorithm_genetic import NSGAII
from artap.algorithm_nlopt import NLopt, LN_BOBYQA
from artap.datastore import SqliteDataStore
from artap.problem import Problem
from artap.results import Results
from artap.NNQuantized import QNN_model
import pandas as pd


class AntennaArray:
    """
    Class antenna array describes the main properties of the patch array like number of patches,
    distances between patches, working frequency etc. It can calculate and display the array factor and radiation
    pattern.
    """
    phi_index: int

    def __init__(self, nx, ny, n_phi, n_theta):

        # the resolution in phase an magnitudes
        self.n_bits: int = 6

        self.c = 3e8  # speed of the light
        self.f = 3.6e9  # working frequency

        self.lambda_0 = self.c / self.f  # wave length
        self.k_0 = 2 * np.pi / self.lambda_0  # wave number

        self.d_x = self.lambda_0 / 4  # distance between patches
        self.d_y = self.lambda_0 / 4

        self.n_x = nx  # number of patches
        self.n_y = ny

        self.n_phi = n_phi  # resolution in azimuth
        self.n_theta = n_theta  # resolution in elevation

        self.phi_mesh = np.ones((self.n_theta, self.n_phi))
        self.theta_mesh = np.ones((self.n_theta, self.n_phi))

        self.phi = np.linspace(-np.pi, np.pi, self.n_phi)  # azimuth
        self.theta = np.linspace(-np.pi / 2, np.pi / 2, self.n_theta)  # elevation

        self.sin_phi = np.sin(self.phi)
        self.cos_phi = np.cos(self.phi)
        self.sin_theta = np.sin(self.theta)
        self.cos_theta = np.cos(self.theta)

        self.inputs = np.zeros([self.n_x, self.n_y], dtype=complex)

        # Matrices for array factor calculation
        self.delta_i = np.zeros([self.n_theta, self.n_phi])
        self.delta_j = np.zeros([self.n_theta, self.n_phi])
        for i in range(self.n_theta):
            for j in range(self.n_phi):
                self.delta_i[i, j] += (self.d_x * self.sin_theta[i] * self.cos_phi[j])
                self.delta_j[i, j] += (self.d_y * self.sin_theta[i] * self.sin_phi[j])

    def phi_index(self, angle):
        return int((angle + 180) * self.n_phi / 360)

    def theta_index(self, angle):
        return int((angle + 90) * self.n_theta / 180)

    def set_inputs(self, vector: list):
        k = 0
        for i in range(self.n_x):
            for j in range(self.n_y):
                self.inputs[i, j] = vector[k] * (np.cos(vector[k + 1])
                                                 + 1j * np.sin(vector[k + 1]))
                k += 2

    def set_uniform_inputs(self):
        """ Sets the amplitude 1 and angle 0 for all patches """
        k = 0
        for i in range(self.n_x):
            for j in range(self.n_y):
                self.inputs[i, j] = 1
                k += 2

    def calculate_array_factor(self, vector=None):
        """ Calculates the array factor for given set of inputs """
        array_factor: ndarray = np.zeros([self.n_theta, self.n_phi], dtype=complex)
        if vector is None:
            self.set_uniform_inputs()
        else:
            self.set_inputs(vector)
        for i in range(0, self.n_x):
            for j in range(0, self.n_y):
                array_factor = array_factor + np.exp(1j * self.k_0 * (i * self.delta_i + j * self.delta_j)) * \
                               self.inputs[i, j]
        array_factor = array_factor * 1 / self.n_x / self.n_y
        return array_factor

    def plot_array_factor_2d(self, array_factor, phi=0):
        phi_index = self.phi_index(phi)
        plt.figure()
        plt.plot([-90, 90], [-25, -25], 'r')
        plt.plot(self.theta / np.pi * 180, 20 * np.log10(np.abs(array_factor[:, phi_index])),
                 '--', label='exact solution')

        plt.ylim([-60, 0])
        plt.xlim([-90, 90])
        plt.grid()
        plt.show()

    def plot_array_factor_3d(self, array_factor, ax=None, logarithmic=True, log_range=-40):
        """ Plot 3D Array Factor

            Args:
                ax: Axis object to plot into
                logarithmic: Plot in dB

            Return:
                ax: Axes object
                :param array_factor:
                :param logarithmic:
                :param ax:
                :param log_range:
        """

        for t, theta in enumerate(self.theta):
            for p, phi in enumerate(self.phi):
                self.theta_mesh[t, p] = theta
                self.phi_mesh[t, p] = phi

        array_factor = np.abs(array_factor) / np.max(np.abs(array_factor))

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        if logarithmic is True:
            array_factor_db = lin2db(array_factor)
            # array_factor_min = np.min(array_factor_db)
            # array_factor_max = np.max(array_factor_db)

            # AF = array_factor_db - (log_range + array_factor_max)
            # AF[AF < 0.0] = 0.0
        else:
            pass
            # array_factor_min = np.min(array_factor)
            # array_factor_max = np.max(array_factor)

        x, y, z = sph2cart(self.phi_mesh, self.theta_mesh, array_factor)

        ax.plot_surface(x, y, z, facecolors=cm.jet(array_factor))
        plt.xlabel('X')
        plt.ylabel('Y')
        # lim_left, lim_right = ax.get_zlim()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)

        mp = cm.ScalarMappable(cmap=plt.cm.jet)
        if logarithmic is True:
            mp.set_array(array_factor_db)
        else:
            mp.set_array(array_factor)
        plt.colorbar(mp)
        plt.show()
        return ax

    @staticmethod
    def set_graphics():
        label_size = 14
        mpl.rcParams['xtick.labelsize'] = label_size
        mpl.rcParams['ytick.labelsize'] = label_size


class AntennaArrayProblem(Problem):

    def set_tolerance_scheme(self, theta_r: float, phi_r: float, width: float, attenuation: list):
        self.phi_r = phi_r
        self.theta_r = theta_r
        self.width = width
        self.theta_index = self.antenna.theta_index(self.theta_r)
        self.phi_index = self.antenna.phi_index(self.phi_r)
        angles = [theta_r - width, theta_r + width]
        indices = []
        for angle in angles:
            for i, theta in enumerate(self.theta):
                angle_rad = angle * np.pi / 180
                if angle_rad < theta:
                    if abs(angle_rad - self.theta[i]) > abs(self.theta[i]):
                        indices.append(i - 1)
                    else:
                        indices.append(i)
                    break

        self.indices = indices
        self.pattern_radiation = []
        self.data = []

        # tolerance scheme which array factor should fit
        self.reference[0:indices[0]] = attenuation[0]
        self.reference[indices[0]:indices[1]] = attenuation[1]
        self.reference[indices[1]:] = attenuation[2]

    def process_results(self):
        # Post - processing the results
        # reads in the result values into the b, results class
        # database_name = "database.sqlite"
        # self.problem.data_store = SqliteDataStore(self.problem, database_name=database_name)
        b = Results(self)
        pareto = []

        # plt.figure()
        # for individual in b.pareto_individuals():
        #     plt.plot(individual.costs[0], individual.costs[1], 'ro', markersize=12)
        #     pareto.append(individual)
        # for individual in b.population(-1):
        #     plt.plot(individual.costs[0], individual.costs[1], 'o')
        # plt.grid()
        # plt.xlabel(r"$\mathcal{F}_1$", fontsize=16)
        # plt.ylabel(r"$\mathcal{F}_2$", fontsize=16)
        # plt.tight_layout()
        # plt.savefig('pareto_front.pdf')
        # plt.show()
        array_factor = self.antenna.calculate_array_factor(b.pareto_individuals()[0].vector)
        self.pattern_radiation = 20 * np.log10(np.abs(array_factor[:, self.phi_index]) /
                      np.max(np.abs(array_factor)))
        exact = array_factor[:, self.phi_index]
        # df0 = pd.DataFrame(exact)
        # df0.to_csv('exact.csv')
        exact_solution = 20 * np.log10(np.abs(array_factor[:, self.phi_index]) /
                      np.max(np.abs(array_factor)))
        # plt.figure()
        # plt.plot([-90, 90], [-25, -25], 'r')
        # plt.plot(self.theta / np.pi * 180, 20*np.log10(self.reference), 'k-')
        # plt.plot(self.theta / np.pi * 180, exact_solution, '--', label='exact solution')
        #
        # plt.ylim([-60, 0])
        # plt.xlim([-90, 90])
        # plt.legend()
        # plt.grid()
        # plt.savefig('1.pdf')
        # plt.show()
        # for k in range(len(pareto)):
        #     saved_vector = b.pareto_individuals(-1)[k].vector.copy()
        #     plt.figure()
        #     plt.plot(self.theta / np.pi * 180,
        #              20 * np.log10(np.abs(array_factor[:, self.phi_index]) /
        #                            np.max(np.abs(array_factor))), 'k-', label='exact solution')
        #
        #     for n_bits in range(8, 0, -1):
        #         vector = saved_vector.copy()
        #         for i in range(len(vector)):
        #             vector[i] = round(vector[i] * 2 ** n_bits) / 2 ** n_bits
        #         array_factor = self.antenna.calculate_array_factor(b.pareto_individuals(-1)[k].vector)
        #         b.pareto_individuals(-1)[k].vector = vector
        #         plt.plot(self.theta / np.pi * 180,
        #                  20 * np.log10(np.abs(array_factor[:, self.phi_index]) /
        #                                np.max(np.abs(array_factor))), '--', label='{} bits'.format(n_bits + 1))
        #     plt.xlabel(r'$\theta$', fontsize=16)
        #     plt.ylabel(r'$AF$ [dB]', fontsize=16)
        #     plt.ylim([-60, 0])
        #     plt.xlim([-90, 90])
        #     plt.legend()
        #     plt.grid()
        #     plt.tight_layout()
        #     plt.savefig('pareto_front_{}.pdf'.format(k))
        #     plt.show()
        # plt.plot(self.antenna.inputs[0])
        # plt.show()
        AF_real = array_factor[0, 0:len(self.antenna.inputs)].real
        AF_imag = array_factor[0, 0:len(self.antenna.inputs)].imag
        print(np.shape(AF_real))
        print(np.shape(AF_imag))
        inp_real = self.antenna.inputs[0, :].real
        inp_imag = self.antenna.inputs[0, :].imag
        print(np.shape(inp_real))
        print(np.shape(inp_imag))
        data = [AF_real, AF_imag, inp_real, inp_imag]

        nparray = np.array(data)
        transpose = nparray.transpose()
        data = transpose.tolist()

        df = pd.DataFrame(data, columns=('AF_real', 'AF_imag', 'inp_real', 'inp_imag'))
        print(df)
        print(df.shape)
        self.data = df

        # self.antenna.plot_array_factor_3d(array_factor)

    def evaluate(self, individual):

        array_factor = self.antenna.calculate_array_factor(individual.vector)

        # compute module of complex numbers in array factor
        magnitude = np.abs(array_factor)
        magnitude_norm = magnitude - np.max(magnitude)

        # magnitude on required position
        magnitude_r = magnitude[self.theta_index, self.phi_index]

        # maximum from the whole array factor
        # maximum = np.max(magnitude)

        side_lobes_integral = np.sum((magnitude[:, self.phi_index] > self.reference) *
                                     (magnitude[:, self.phi_index] - self.reference) ** 2)

        # integral within the pass band
        main_lobe_integral = np.sum(magnitude[self.indices[0]:self.indices[1], self.phi_index])

        # added ends of the interval
        # lobe_maximum = [magnitude[0, self.phi_index], magnitude[self.n_theta - 1, self.phi_index]]

        # look for local maxims (lobes) in the left
        # for i in range(1, self.indices[0] - 1):
        #     if magnitude[i - 1, self.phi_index] < magnitude[i, self.phi_index] > magnitude[i + 1, self.phi_index]:
        #         lobe_maximum.append(magnitude[i, self.phi_index])

        # look for local maxims (lobes) in the right
        # for i in range(self.indices[1], self.n_theta - 1):
        #     if magnitude[i - 1, self.phi_index] < magnitude[i, self.phi_index] > magnitude[i + 1, self.phi_index]:
        #         lobe_maximum.append(magnitude[i, self.phi_index])
        #
        # maximal amplitude from both lobes
        # lobe_maximum = max(lobe_maximum)

        # f_7 = max(max(magnitude[:self.indices[0], self.phi_index]),
        #        max(magnitude[self.indices[1]:, self.phi_index]))
        # print(magnitude_r, side_lobes_integral)
        self.mag.append(magnitude_r)
        self.side.append(side_lobes_integral)
        s = [self.mag, self.side, self.theta]
        return [magnitude_r, side_lobes_integral]

    def set(self, **kwargs):
        # Not mandatory to give a name for the test problem
        self.name = 'Antenna array'
        # required direction of radiation and calculation of appropriate indices to array factor matrix
        self.n_x = kwargs['n_x']
        self.n_y = kwargs['n_y']
        self.n_phi = kwargs['n_phi']
        self.n_theta = kwargs['n_theta']

        self.antenna = AntennaArray(self.n_x, self.n_y, self.n_phi, self.n_theta)
        self.theta = self.antenna.theta
        self.phi = self.antenna.phi
        self.reference = np.zeros(len(self.theta))
        self.indices = []
        self.mag = []
        self.side = []

        # Dynamically prepare parameters for given number of patches
        self.parameters = []
        for i in range(self.n_x * self.n_y):
            self.parameters.append(
                {'name': 'I_{}'.format(i), 'bounds': [0, 1], 'parameter_type': 'float', 'initial_value': 0.5})
            self.parameters.append(
                {'name': 'alpha_{}'.format(i), 'bounds': [-np.pi / 2, np.pi / 2], 'parameter_type': 'float'})

        # The two, separate optimization functions and the direction of the optimization
        # is set to minimization. It is also possible to use the maximize keyword.
        self.costs = [{'name': 'f_1', 'criteria': 'maximize'},
                      {'name': 'f_2', 'criteria': 'minimize'}]

        """ Process the requirements on the beam shape. """
        theta_r = 40  # target elevation
        phi_r = 0  # target azimuth
        width = 30  # beam width

        # attenuation of left side lobe, main beam, right side lobe
        attenuation = [0.01, 1, 0.01]
        self.set_tolerance_scheme(theta_r, phi_r, width, attenuation)


database_file = 'data.sqlite'
problem = AntennaArrayProblem(n_x=10, n_y=10, n_phi=100, n_theta=100)
datastore = SqliteDataStore(problem, database_name=database_file)
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 20
algorithm.run()
# model = QNN_model(problem)
# model.train(problem)
problem.process_results()

model = QNN_model(problem)
model.train(problem)

# plt.plot(problem.pattern_radiation)
# plt.show()
datastore.sync_all()
# cost = []
# vector = []
# for individual in datastore.problem.individuals:
#     cost.append(datastore.problem.individuals[0].costs)
#     vector.append(datastore.problem.individuals[0].vector)
# print(np.shape(cost))
# results = Results(problem)
# print(results.get_population_ids())

# datass = pd.read_csv('magnitude.csv')
# datass = datass.values
# plt.plot(datass[:, 1])
# plt.plot(datass[:, 2])
# plt.show()


