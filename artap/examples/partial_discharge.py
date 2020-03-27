"""
A non-linear curve fitting example for partial discharges.
"""

from artap.problem import Problem
from artap.results import Results
# from artap.algorithm_bayesopt import BayesOptSerial
from artap.algorithm_nlopt import NLopt, LN_BOBYQA, LN_COBYLA, LN_NELDERMEAD
from artap.algorithm_genetic import NSGAII
from artap.algorithm_swarm import PSO
import matplotlib.pyplot as plt
import numpy as np

# Data Samples from the test examples (page 20 in the bsc theses)
# n = 1
C1x = [9.627, 19.589]
R1x = [5.870, 2.1663]

# (tdchi, SRi)
SR1 = [(1.0, 46.83347), (2.0, 45.74274), (4.0, 43.6369), (6.0, 41.62801), (8.0, 39.7116), (10.0, 37.88341),
       (15.0, 33.67273), (20.0, 29.93007), (30.0, 23.64647), (50.0, 14.75991), (75.0, 8.188986), (100.0, 4.543356),
       (150.0, 1.398524), (200.0, 0.43049), (300.0, 0.04079), (500.0, 0.000366)]

# n = 2
C2x = [9.627, 10.236, 9.4081]
R2x = [5.870, 2.1663, 1.7806]

C2o1 = [9.627, 9.958385741447383, 9.68637611277249]
R2o1 = [5.870, 1.692170503816123,  2.3120386928356145] # from the newton method based search

C2o2 = [9.627, 2.355104843390313, 17.3250807222832]
R2o2 = [5.870, 13.017148342665315, 1.0569093531258873]


# (tdchi, SRi)
SR2 = [(1.0, 100.7923), (2.0, 95.58673), (4.0, 85.98188), (6.0, 77.35857), (8.0, 69.6149), (10.0, 62.65971),
       (15.0, 48.20685), (20.0, 37.13707), (30.0, 22.12758), (50.0, 7.979435), (75.0, 2.29236), (100.0, 0.676797),
       (150.0, 0.062897), (200.0, 0.062897), (300.0, 6.49E-05), (500.0, 7.75E-09)]

# n = 3
C3x = [9.627, 10.236, 9.4081, 46.288]
R3x = [5.870, 2.1663, 1.7806, 3.0078]

# (tdchi, SRi)
SR3 = [(1.0, 135.0715), (2.0, 129.6215), (4.0, 119.5329), (6.0, 110.4325), (8.0, 102.2183), (10.0, 94.79905),
       (15.0, 79.21414), (20.0, 67.05153), (30.0, 49.96951), (50.0, 32.09568), (75.0, 22.44427), (100.0, 17.51621),
       (150.0, 11.8215), (200.0, 8.217025), (300.0, 4.003668), (500.0, 0.951871)]

Uch = 1000.  # V
tch = 4000.  # s
c0 = 9.627


def sri(x, tdch, Uch, tch, c0):
    """
    Calculates the ui voltage from the given parameters
    :param x: list of individuals from the optimized paramters in the ri, ci order
    :param Sri: measured data at the ith case, contains tuples : (tdchi, Sri) format
    :return:
    """
    sri = 0.
    for j in range(2, len(x), 2):  # step is 2, because r,c pairs
        taui = x[j] * x[j + 1]  # ri*ci
        sri += Uch * (1.0 - np.exp(-tch / taui)) * np.exp(-tdch / taui) / x[j] / c0
    return sri


def test_ui():
    # C1x = [9.627, 19.589]
    # R1x = [5.870, 2.1663]

    # shape of the x  in the case of n = 1:
    # x = [r0,c0,r1,c1]

    # in the simplest testproblem
    # x = [R1x[0], C1x[0], R1x[1], C1x[1]]
    #
    # for sr in SR1:
    #     print('measured:',sr[1], 'calculated',sri(x, sr[0], Uch, tch, c0), 'error:', sr[1]-sri(x, sr[0], Uch, tch, c0))

    # tests for n = 2
    x = [R2x[0], C2x[0], R2x[1], C2x[1], R2x[2], C2x[2]]

    err = 0.0
    for sr in SR2:
        err += (sr[1] - sri(x, sr[0], Uch, tch, c0))**2.
        #print('measured:',sr[1], 'calculated',sri(x, sr[0], Uch, tch, c0), 'error:', sr[1]-sri(x, sr[0], Uch, tch, c0))
    print("standard error:", err)

    # x2 = [R2o1[0], C2o1[0], R2o1[1], C2o1[1], R2o1[2], C2o1[2]]
    # err = 0.0
    # for sr in SR2:
    #     err += (sr[1] - sri(x2, sr[0], Uch, tch, c0)) ** 2.
    #     # print('measured:',sr[1], 'calculated',sri(x, sr[0], Uch, tch, c0), 'error:', sr[1]-sri(x, sr[0], Uch, tch, c0))
    # print("standard error:", err)
    # tests for n = 3
    # x = [R3x[0], C3x[0], R3x[1], C3x[1], R3x[2], C3x[2], R3x[3], C3x[3]]
    #
    # for sr in SR3:
    #     print('measured:', sr[1], 'calculated', sri(x, sr[0], Uch, tch, c0), 'error:',
    #           sr[1] - sri(x, sr[0], Uch, tch, c0))


class ExponentialFittingSimple(Problem):

    def set(self):
        self.name = 'Exponential fitting Problem'
        self.parameters = [{'name': 'r_1', 'bounds': [1.0, 20.]},
                           {'name': 'c_1', 'bounds': [1.0, 20.]},
                           {'name': 'r_2', 'bounds': [1.0, 20.]},
                           {'name': 'c_2', 'bounds': [1.0, 20.]}]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        # The individual.vector function contains the problem parameters in the appropriate (previously defined) order

        x = [5.870, 9.627] # r0, C0 because its known
        x += individual.vector
        #print(x)
        error = 0.0

        # we just minimizing the square of the error
        for sr in SR2:
            error += (sr[1] - sri(x, sr[0], Uch, tch, c0))**2.

        m = len(SR2)
        #aic = m*(np.log(error/m))+4.
        return [np.log(error)]


#test_ui()
# Initialization of the problem

def nsgaii():
    problem = ExponentialFittingSimple()

    # Perform the optimization iterating over 100 times on 100 individuals.
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 200
    algorithm.options['max_population_size'] = 100
    algorithm.run()

    results = Results(problem)
    optimum = results.find_minimum('f_1')
    print(optimum)
    x = [5.870, 9.627]  # r0, C0 because its known
    x += optimum.vector
    print(x)
    err = 0.0
    for sr in SR2:
        err += (sr[1] - sri(x, sr[0], Uch, tch, c0))**2.
    print("standard error, now:", err)


nsgaii()
test_ui()


