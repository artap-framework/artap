# -*- coding: utf-8 -*-

from math import pi
from scipy.constants import mu_0
from cvxopt.base import matrix
from cvxopt import solvers, log, exp

from collections import namedtuple

# constants
RHO_CU = 0.0216        # 0.0216        # ohm * mm2 / m @ 75°C
RHO_COPPER = 8960.0    # kg/m3

# model variables
# - represents the positions in the solution matrix
W = 0       # conductor width
H = 1       # conductor height
Nc = 2      # number of conductors
Nr = 3      # number of radial conductors
Nax = 4     # number of axial conductors
Nsrad = 5

Ploss = 6   # winding loss
Acu = 7     # copper area
Vol = 8     # copper volume

"""
    Notes
    -----

    - in the first step only the sci impedance is calculated analytically from the maximum of bg
    - a simple algorithm is needed to search the local maxima of br and bz in the given segment
"""


def b_gap(n, i, h_w):
    """
    peak value of the induction in the main gap
    @param winding: is the result of the optimization
    This value is calculated from the constants of this calculation
    """
    return (2.**0.5)*mu_0*n*i/(h_w*1e-3)


def gp_model_winding(N, Rm, Tw, Hw, Ins_rad, Ins_sr, Ins_ax, Current, Omega, B_ax, B_rad, n_ax, ff_min, w_max, h_max, ph_n):
    """
    The goal of this model to determine the optimal sizes of a conductor: w and h.

    :param N: total number of turns
    :param Rm: mean radius in mm
    :param Tw: winding thickness in mm
    :param Hw: winding height in mm
    :param Ins_ax: insulation distance between two horizontal blocks
    :param Ins_rad: insulation distance between two conductor
    :param Current: Amps in one turn
    :param Omega: 2pi*f
    :param B_ax: the value of the magnetic flux density in the middle of the leakage flux channel
    :param B_rad:
    :param n_ax: number of axial conductors in one turn
    :param ff_min: filling factor of the winding
    :param Nsrad: number of radial strands
    :param w_max: maximum width
    :param h_max: maximum height
    :param ph_n: phase number
    :param Ins_sr: strand insulation

    :return: A, b, F, g - matrices and vectors for the geometric programming problem
    """

    K = []

    F = matrix(0.0, (16, 9))  # inequality matrix
    g = matrix(0.0, (16, 1))  # norm for F matrix

    A = matrix(0.0, (3, 9))  # Equalities
    b = matrix(0.0, (3, 1))  # norm for A matrix

    # -------------------------------------------
    # inequalities: [g][F] <= 1
    # -------------------------------------------
    # objective function 1, maximize the copper volume in the winding
    K.append(1)
    F[0, [Ploss]] = 1.
    g[0] = 1.

    # Nax * H/ HW + Nax * ins_ax/HW <= 1
    K.append(2)

    F[1, [H, Nax]] = 1.
    g[1] = n_ax / Hw

    F[2, [Nax]] = 1.
    g[2] = Ins_ax / Hw

    # Nrad * Nc * Ins_rad / Tw <= 1
    K.append(3)

    #
    # !!!! Normal conductor
    #
    # F[3, [Nr, Nc]] = 1.
    # g[3] = Ins_rad/Tw

    # F[4, [W, Nr, Nc]] = 1.
    # g[4] = 1./Tw

    F[3, [Nr, Nc]] = 1.
    g[3] = Ins_rad / Tw

    F[4, [Nr, Nc, Nsrad]] = 1.
    g[4] = Ins_sr / Tw

    F[5, [W, Nr, Nsrad, Nc]] = 1.
    g[5] = 1. / Tw

    # dc loss + ac loss
    K.append(3)

    F[6, [Acu, Ploss]] = -1  # dc loss
    g[6] = RHO_CU * 1e-3 * pi * 2. * Rm * N * Current ** 2. * ph_n/3.

    # ac loss axial
    # (omega**2.)*((w*1e-3)**2.)/24./(const.RHO_CU*1e-6)*vol*(b_gp**2.)/3.

    F[7, [Vol]] = 1.
    F[7, [W]] = 2.
    F[7, [Ploss]] = -1
    g[7] = Omega ** 2. / 24. / (RHO_CU * 1e-6) * (B_ax ** 2.) / 3. * 1e-6 * ph_n

    # ac loss radial
    # (omega**2.)*((w*1e-3)**2.)/24./(const.RHO_CU*1e-6)*vol*(b_gp**2.)/3.

    F[8, [Vol]] = 1.
    F[8, [H]] = 2.
    F[8, [Ploss]] = -1
    g[8] = Omega ** 2. / 24. / (RHO_CU * 1e-6) * (B_rad ** 2.) / 3. * 1e-6 * ph_n

    # 7
    K.append(1)
    F[9, [Nax]] = -1.
    g[9] = 1.

    # 8
    K.append(1)
    F[10, [Nc]] = -1.
    g[10] = 1.

    # 9
    K.append(1)
    F[11, [Nsrad]] = -1.
    g[11] = 1.

    # 10
    K.append(1)

    F[12, [Acu, Nax, Nr]] = 1.
    g[12] = ff_min / (Hw * Tw)

    # 10
    K.append(1)

    F[13, [W]] = 1.
    g[13] = 1. / (w_max)

    # 11
    K.append(1)

    F[14, [H]] = 1.
    g[14] = 1. / (h_max)

    # 12 --- h/w ratio --- because the axial height is not considered
    K.append(1)

    F[15, [H]] = 1.
    F[15, [W]] = -1.
    g[15] = 1./3.

    # -------------------------------------------
    # equality constraints: Ax = b --->  Ab^(-1)
    # -------------------------------------------

    # criteria for the turn number
    # Nr * Nax = N
    A[0, [Nr, Nax]] = 1.
    b[0] = N

    # copper area in one turn
    A[1, [W, H, Nc, Nsrad]] = 1.
    A[1, [Acu]] = -1.
    b[1] = 1. / (n_ax)

    # copper volume in the winding [m3]
    A[2, [Vol]] = -1.
    A[2, [Acu, Nax, Nr]] = 1.
    b[2] = 1. / (2. * pi * Rm * 1e-9)

    ##### solving the problem #####

    g = log(g)
    b = log(b)

    solvers.options['show_progress'] = False
    sol = solvers.gp(K, F, g, A=A, b=b)

    m = exp(sol['x'])
    # print "Status: ",sol['status']
    status = sol['status']
    objval = exp(sol['primal objective'])

    # print('w: ', m[W])
    # print('h: ', m[H])
    # print('Ploss', m[Ploss])

    return status, m, objval

if __name__ == "__main__":

    ff_min = 0.4 # filling factor minimum

    N = 85.             # [#]
    Rm = 495./2.        # [mm]
    Tw = 73.            # [mm]
    Hw = 1766.          # [mm]
    Ins_rad = 0.5       # [mm]
    Ins_ax = 3.5        # [mm]
    Current = 1399.64   # [A]
    Freq = 50.          # [Hz]
    Omega = 2.*pi*Freq
    ph_n = 3.
    Ins_sr = 0.1
    h_max = 9. #12.
    w_max = 3.5
    n_ax = 2.

    Bg = b_gap(N, Current, Hw)

    status, m, objval = gp_model_winding(N, Rm, Tw, Hw, Ins_rad, Ins_sr, Ins_ax, Current, Omega, Bg/2./1.41, Bg/3./1.41, n_ax, ff_min, w_max, h_max, ph_n)

    # print('Bg', Bg)
    # print('w: ', m[W])
    # print('h: ', m[H])
    # print('Ploss', m[Ploss])