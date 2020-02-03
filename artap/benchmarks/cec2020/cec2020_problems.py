"""
IMPLEMENTATION of BENCHMARK FUNCTIONS from CEC2020:
---------------------------------------------------

Referecces:

[1] https://github.com/P-N-Suganthan/2020-Multimodal-Multi-Objective-Benchmark
[2] J. J. Liang1, P. N. Suganthan2, B. Y. Qu3, D. W. Gong4 and C. T. Yue1,
    "Problem Definitions and Evaluation Criteria for the CEC 2020 Special Session on Multimodal Multiobjective
    Optimization"

"""
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import artap.colormaps as cmaps
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from numpy import vectorize
from numpy import pi, sin, e, cos
import numpy as np


def MMF1(x1, x2):
    """
    Properties
    =================================================================
    Scalable number of variables :        x
    Scalable number of objectives:        x
    Pareto optima known:                  yes
    Pareto front geometry:                convex
    Pareto set geometry:                  nonlinear
    Scalable number of Pareto set:        x
    Nr of global optimums:                2
    NR of local optimums:                 1
    =================================================================

    Solution
    --------
    global pareto set:

    x1 = x1
    x2 = sin(6*pi*abs(x1-2)+pi)

    global pareto front:    f2 =  1 - sqrt(f1) , where 0<=f1<=1

    :param x1: [1,3]
    :param x2: [-1,1]
    :return: [f1, f2]
    """

    # a = e  # this can be any other number, the search space of x2 is [-a^3, a^3]
    # if x1 < 2.:
    #    a = 1.
    a = np.where(x1 < 2., 1., e)
    f1 = abs(x1 - 2)
    f2 = 1 - abs(x1 - 2) ** 0.5 + 2. * (x2 - (a ** x1) * sin(6. * pi * abs(x1 - 2.) + pi)) ** 2.
    return [f1, f2]


def MMF2(x1, x2):
    """
    Properties
    =================================================================
    Scalable number of variables :        x
    Scalable number of objectives:        x
    Pareto optima known:                  yes
    Pareto front geometry:                convex
    Pareto set geometry:                  nonlinear
    Scalable number of Pareto set:        x
    Nr of global optimums:                2
    NR of local optimums:                 1
    =================================================================

    Solution
    --------
    global pareto set:

    x1 = x2**2  if x1<1
         (x2-1) if 1<x1<2
    x2 = x2

    global pareto front:    f2 =  1 - sqrt(f1) , where 0<=f1<=1

    :param x1: [0,1]
    :param x2: [0,2]
    :return: [f1, f2]
    """

    f1 = abs(x1)

    a = x1 ** 0.5

    f2a = 1 - a + 2. * (4. * (x2 - a)) ** 2. - 2. * cos(20.0 * pi / (2.0 ** 0.5) * (x2 - a)) + 2.
    f2b = 1 - a + 2. * (4. * (x2 - 1.0 - a)) ** 2. - 2. * cos(20.0 * pi / (2.0 ** 0.5) * (x2 - 1.0 - a)) + 2.

    f2 = np.where(x2 < 1., f2a, f2b)

    return [f1, f2]


def plot_MMF1(selector):
    """
    :param selector: 0 or 1 to plot f1 or f2
    :return:
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(1., 3., .01)
    Y = np.arange(-e, e, .01)
    X, Y = np.meshgrid(X, Y)

    Z = MMF1(X, Y)
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z[selector], cmap=cmaps.viridis,
                           linewidth=0, antialiased=True)

    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def plot_MMF2(selector):
    """
    :param selector: 0 or 1 to plot f1 or f2
    :return:
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(0., 1., .01)
    Y = np.arange(0., 2., .01)
    X, Y = np.meshgrid(X, Y)

    Z = MMF2(X, Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z[selector], cmap=cmaps.viridis, linewidth=0, antialiased=True)

    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == "__main__":
    plot_MMF1(0)
    plot_MMF1(1)

    #plot_MMF2(0)
