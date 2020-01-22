"""
This file contains the implementation of the following benchmark functions::

    - 1D synthetic test function for rubust design optimization (RDO)
    - 2D synthetic test function for RDO
    - 5D synthetic test function for RDO

    - Ackley test function

Definition and a plot of the 2D synthetic function for testing the robustness.
"""
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import artap.colormaps as cmaps
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import exp
import numpy as np


def eval_2d_synthetic(x1, x2):
    """
    Gaussian 2D synthetic test function for testing the robustness.

    Peaks:
    -----
    (1,1) - width 0.3, multiplier 0.7
    (1,3) - width 0.4, multiplier 0.75
    (3,1)*- width 1.0, multiplier 1.0  <- robust solution
    (3,4) - width 0.4, multiplier 1.2  <- global optimum
    (5,2) - width 0.6, multiplier 1.0

    The function is defined on the [0,5], [0,5] region.

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    res = 0.7 * exp(-((x1 - 1.) ** 2. + (x2 - 1.) ** 2.) / 0.18) + \
          0.75 * exp(-((x1 - 1.) ** 2. + (x2 - 3.) ** 2.) / 0.32) + \
          exp(-((x1 - 3) ** 2 + (x2 - 1) ** 2) / 2.) + \
          1.2 * exp(-((x1 - 3) ** 2 + (x2 - 4) ** 2) / 0.32) + \
          exp(-((x1 - 5) ** 2. + (x2 - 2) ** 2.) / 0.72)

    return res


def plot_2d_synthetic():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(0, 5, .01)
    Y = np.arange(0, 5, .01)
    X, Y = np.meshgrid(X, Y)

    # print(eval_2d_synthetic(X,Y))
    print(eval_2d_synthetic(X, Y))

    Z = eval_2d_synthetic(X, Y)  # np.sqrt(X**2 + Y**2)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cmaps.viridis,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def eval_1d_synthetic(y: list):
    """
    This function was introduced to test the MEM - multiple-evaluation model schema, to compare it with the single
    evaluation model.

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    x = y[0]

    res = exp(-(x - 1) ** 2. / 0.5) + 2. * exp(-(x - 1.25) ** 2. / 0.045) + 0.5 * exp(-(x - 1.5) ** 2. / 0.0128) + \
          2. * exp(-(x - 1.6) ** 2. / 0.005) + 2.5 * exp(-(x - 1.8) ** 2. / 0.02) + \
          2.5 * exp(-(x - 2.2) ** 2. / 0.02) + 2. * exp(-(x - 2.4) ** 2. / 0.005) + \
          2. * exp(-(x - 2.75) ** 2. / 0.045) + exp(-(x - 3) ** 2. / 0.5) + 2. * exp(-(x - 6.) ** 2. / 0.32) + \
          2.2 * exp(-(x - 7.) ** 2. / 0.18) + 2.4 * exp(-(x - 8.) ** 2. / 0.5) + \
          2.3 * exp(-(x - 9.5) ** 2. / 0.5) + 3.2 * exp(-(x - 11.) ** 2. / 0.18) + 1.2 * exp(-(x - 12.) ** 2. / 0.18)

    return res


def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,)) / N)[(N - 1):]


def plot_1d_synthetic():
    x = np.arange(0.0, 12.0, 0.1)

    plt.figure()
    plt.plot(x, eval_1d_synthetic([x]), 'black',
             x, runningMeanFast(eval_1d_synthetic([x]), 10), '--')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend(['f(x)', 'avg(f(x))'])
    plt.show()


def atom_nd(width, multiplier, x: list, z: list):
    """
    Atomic function to generate an n-dimensional gaussian test function.

    multiplier: the amplitude/peak value of the function
    width: is the divider
    z: represents the zeros of the function
    x: represents the variables
    """
    res = 0
    for i in range(0, len(x)):
        res += (x[i] - z[i]) ** 2.

    res /= -width

    return exp(res) * multiplier


def eval_5d_synthetic(x: list):
    """
    Evaluates a 5 dimensional Gaussian - test function

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """
    result = atom_nd(0.3, 0.7, x, [10., 1.0, 6.0, 7.0, 8.0])
    result += atom_nd(0.4, 0.75, x, [1.0, 3.0, 8.0, 9.5, 2.0])
    result += atom_nd(1.0, 1.0, x, [3.0, 1.0, 3.0, 2.0, 5.0])  # robust solution
    result += atom_nd(0.4, 1.2, x, [3.0, 4.0, 1.3, 5.0, 5.0])  # highest peak
    result += atom_nd(0.6, 1.0, x, [5.0, 2.0, 9.6, 7.3, 8.6])
    result += atom_nd(0.5, 0.6, x, [7.5, 8.0, 9.0, 3.2, 4.6])
    result += atom_nd(0.1, 0.5, x, [5.7, 9.3, 2.2, 8.4, 7.1])
    result += atom_nd(1.0, 0.2, x, [5.5, 7.2, 5.8, 2.3, 4.5])
    result += atom_nd(0.2, 0.4, x, [4.7, 3.2, 5.5, 7.1, 3.3])
    result += atom_nd(0.3, 0.1, x, [9.7, 8.4, 0.6, 3.2, 8.5])

    return result


def eval_10d_synthetic(x: list):
    """
    Evaluates a 10 dimensional Gaussian - test function

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """
    result = atom_nd(0.3, 0.7, x, [10., 1.0, 6.0, 7.0, 8.0, 1.0, 1.0, 6.0, 7.0, 8.0])
    result += atom_nd(0.4, 0.75, x, [1.0, 3.0, 8.0, 9.5, 2.0, 1.0, 3.0, 8.0, 9.5, 2.0])
    result += atom_nd(1.0, 1.0, x, [3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0])  # robust solution
    result += atom_nd(0.4, 1.2, x, [3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0])  # highest peak
    result += atom_nd(0.6, 1.0, x, [5.0, 2.0, 9.6, 7.3, 8.6, 5.0, 2.0, 9.6, 7.3, 8.6])
    result += atom_nd(0.5, 0.6, x, [7.5, 8.0, 9.0, 3.2, 4.6, 7.5, 8.0, 9.0, 3.2, 4.6])
    result += atom_nd(0.1, 0.5, x, [5.7, 9.3, 2.2, 8.4, 7.1, 5.7, 9.3, 2.2, 8.4, 7.1])
    result += atom_nd(1.0, 0.2, x, [5.5, 7.2, 5.8, 2.3, 4.5, 5.5, 7.2, 5.8, 2.3, 4.5])
    result += atom_nd(0.2, 0.4, x, [4.7, 3.2, 5.5, 7.1, 3.3, 4.7, 3.2, 5.5, 7.1, 3.3])
    result += atom_nd(0.3, 0.1, x, [9.7, 8.4, 0.6, 3.2, 8.5, 9.7, 8.4, 0.6, 3.2, 8.5])

    return result


def eval_ackley(x: list):
    """
    Implementation is based on: https://en.wikipedia.org/wiki/Ackley_function
    The minimum is placed in [0,0]
    """
    return -20. * exp(-0.2 * (0.5 * (x[0] ** 2 + x[1] ** 2)) ** 0.5) - \
           exp(0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))) + np.e + 20.


def plot_2d_ackley():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(-32, 32, .1)
    Y = np.arange(-32, 32, .1)
    X, Y = np.meshgrid(X, Y)

    Z = eval_ackley([X, Y])
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cmaps.viridis,
                           linewidth=0, antialiased=True)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == "__main__":
    plot_2d_synthetic()
    plot_1d_synthetic()
    plot_2d_ackley()
