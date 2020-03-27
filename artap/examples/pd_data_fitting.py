"""
This function shows, how you can fit a function with NSGA II to your measured data.

The measured data is coming from a partial discharge measurement, where the initial slope of the voltage responses
measured. The task is to find out the R and C elements of the modeling R-C circuit. The theory says, that
these elements can be found if we can search these elements in the following, exponential shape:


The detailed description of the analytical model can be founc here: doi....
"""

import matplotlib.pyplot as plt
import numpy as np

# (tdchi, SRi)
SR2 = [(1.0, 100.7923), (2.0, 95.58673), (4.0, 85.98188), (6.0, 77.35857), (8.0, 69.6149), (10.0, 62.65971),
       (15.0, 48.20685), (20.0, 37.13707), (30.0, 22.12758), (50.0, 7.979435), (75.0, 2.29236), (100.0, 0.676797),
       (150.0, 0.062897), (200.0, 0.062897), (300.0, 6.49E-05), (500.0, 7.75E-09)]

x_val = [x[0] for x in SR2]
y_val = [x[1] for x in SR2]
plt.plot(x_val, y_val, 'bo', label="Measured data")

C2o1 = [9.627, 9.958385741447383, 9.68637611277249]
R2o1 = [5.870, 1.692170503816123, 2.3120386928356145]

# NSGA result - 200 generations
sol_nsga = [5.87, 9.627, 1.2254465803764465, 14.458027617643706, 4.8264795611077655, 5.208973499033958]
sol_qlnp = [R2o1[0], C2o1[0], R2o1[1], C2o1[1], R2o1[2], C2o1[2]]


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


Uch = 1000.  # V
tch = 4000.  # s
c0 = 9.627

y_nsga = [sri(sol_nsga, t[0], Uch, tch, c0) for t in SR2]
y_nm = [sri(sol_qlnp, t[0], Uch, tch, c0) for t in SR2]

plt.plot(x_val, y_nsga, 'blue', label="Fitted data -- NSGA --")
plt.plot(x_val, y_nm, 'r+--', label="Fitted data -- NLP --")

plt.legend(loc='upper left')
plt.xlabel(r"$\t$", fontsize=16)
plt.show()
