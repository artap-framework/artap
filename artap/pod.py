#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 09:50:41 2019

@author: david
"""

import scipy.io
import os
import numpy as np
from scipy.sparse import linalg as la
import pylab as pl
from artap.dynamical_systems import Model, DiscreteLTISystem


class POD:
    def __init__(self, stifness_matrix, mass_matrix, rhs_vector, solution):
        self.stifness_matrix = stifness_matrix
        self.mass_matrix = mass_matrix
        self.rhs = rhs_vector
        self.solution = solution
        self.steps = 80
        self.num = 3
        self.total_time = 30
        self.dt = self.total_time / self.steps

    def reduce(self, index):
        mass_matrix = self.mass_matrix / self.dt
        matrix_lhs = mass_matrix + self.stifness_matrix
        slnt = np.zeros([len(rhs), self.steps])
        for i in range(1, self.steps):
            slnt[:, i] = la.spsolve(matrix_lhs, mass_matrix @ slnt[:, i-1] + rhs[:, 0]*signal(i * self.dt))

        pl.plot(slnt[index, :])
        pl.show()
        c = np.dot(slnt, slnt.T)
        [D, V] = (np.linalg.eigh(c))

        L = np.zeros([len(V), self.num])
        L[:, :] = V[:, -self.num:]

        mor_rhs = np.dot(L.T, self.rhs)
        mor_mass = L.T @ mass_matrix @ L

        mor_lhs = L.T @ matrix_lhs @ L
        matrix_a = np.linalg.inv(mor_lhs) @ mor_mass
        matrix_b = np.linalg.inv(mor_lhs) @ mor_rhs
        matrix_c = L[index, :]
        return matrix_a, matrix_b, matrix_c

    @staticmethod
    def find_index(solution, px, py):
        ind = -1
        val = 1e6
        for i in range(len(solution)):
            tmp = (px - solution[i, 0])**2 + (py - solution[i, 1])**2
            if tmp < val:
                val = tmp
                ind = i

        print(ind, val)
        return ind


def signal(t):
    u = 1
    if t <= 7.5:
        u = 1.7 * 2
    if 7.5 < t <= 10:
        u = 0.8 * 1.7 * 2
    if t > 10:
        u = 0.1 * 1.7 * 2
    return [u]


# ToDo: Make tests from this
if __name__ == "__main__":
    working_dir = "/home/david/Dokumenty/Git/Software/artap-projects/brazing_mor"
    current_path = os.getcwd()
    os.chdir(working_dir)
    stiffness = scipy.io.loadmat('transient_solver-heat_matrix_stiffness.mat')['matrix_stiffness']
    mass = scipy.io.loadmat('transient_solver-heat_matrix_mass.mat')['matrix_mass']
    rhs = scipy.io.loadmat('transient_solver-heat_rhs.mat')['rhs']
    other = scipy.io.loadmat('transient_solver-heat_other.mat')['other']

    pod = POD(stiffness, mass, rhs, other)
    A, B, C = pod.reduce(10)
    print(A)
    print(B)
    print(C)
    D = [0]

    x0 = [0, 0, 0]
    plant = Model(dt=30/80)
    system = DiscreteLTISystem(plant, A, B, C, D, x0, dt=30/80)
    system.connect(signal)
    plant.run(30)
    system.plot('output')
    pl.show()