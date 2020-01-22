"""
Poloni (POL) function is a classic test function for multi-objective optimization methods as its Pareto optimal
solutions are not continous and non-convex.

References:
---------

[1] Lei, Gang; Zhu, Jianguo; Guo, Youguang, "Design Optimization Methods for Electrical Machines", 2016

[2] Lei G, Shao KR, Guo YG, Zhu JG (2012), "Multiobjective sequential optimization method for the design of
    industrial electromagnetic devices. IEEE Trans Magn 48(11):4538–4541"

section: 4.4.2
formula: 4.13 and 3.13
"""
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import artap.colormaps as cmaps
import numpy as np

from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy import sin, cos


def func_POL(x1, x2):
    """

    :param x1: [-pi ; pi]
    :param x2: [-pi ; pi]
    :return:
    """
    A1 = 0.5 * sin(1.) - 2. * cos(1.) + sin(2.) - 1.5 * cos(2.)
    A2 = 1.5 * sin(1.) - cos(1.) + 2. * sin(2.) - 0.5 * cos(2.)

    B1 = 0.5 * sin(x1) - 2. * cos(x1) + sin(x2) - 1.5 * cos(x2)
    B2 = 1.5 * sin(x1) - cos(x1) + 2. * sin(x2) - 0.5 * cos(x2)

    f1 = 1. + (A1 - B1) ** 2. + (A2 - B2) ** 2.
    f2 = (x1 + 3.) ** 2. + (x2 + 1.) ** 2.

    return [f1, f2]


def plot_pol(pic):
    """
    pic = 0 -> plots the f1 function which has a maxima and two minima
    pic = 1 -> plots the f2 function which i a hyperbola in the given region
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')


# Make data.
    X = np.arange(-np.pi, np.pi, .1)
    Y = np.arange(-np.pi, np.pi, .1)
    X, Y = np.meshgrid(X, Y)

    Z = func_POL(X, Y)
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z[pic], cmap=cmaps.viridis,
                           linewidth=0, antialiased=True)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

if __name__ == "__main__":
    plot_pol(0)
    plot_pol(1)