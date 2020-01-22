"""
Poloni (POL) function is a classic test function for multi-objective optimization methods as its Pareto optimal
solutions are not continous and non-convex.

Reference:
---------

[1] Design Optimization Methods for Electrical Machines,
"""

from scipy import sin, cos

def func_POL(x1,x2):

    A1 = 0.5*sin(1.) - 2. * cos(1.) + sin(2.) - 1.5*cos(2.)
    A2 = 1.5*sin(1.) - cos(1.) + 2.*sin(2.) - 0.5*cos(2.)

    B1 = 0.5*sin(x1) - 2.* cos(x1) + sin(x2) - 1.5*cos(x2)
    B2 = 1.5*sin(x1) - cos(x1) + 2.*sin(x2) -0.5*cos(x2)

    f1 = 1. + (A1 - B1)**2. + (A2 - B2)**2.
    f2 = (x1+3.)**2. + (x2 + 1.)**2.

    return [f1,f2]

