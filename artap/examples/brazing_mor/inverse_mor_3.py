#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 09:50:41 2019

@author: david
"""

import scipy.io
import numpy as np
import scipy as sc
from scipy.sparse import linalg as la
import scipy.sparse as sp
import pylab as pl
import random


def find_index(other, px, py):
    ind = -1
    val = 1e6
    for i in range(len(other)):
        tmp = (px - other[i, 0])**2 + (py - other[i, 1])**2
        if tmp < val:
            val = tmp
            ind = i

    print(ind, val)
    return ind


num = 6
total_time = 30
steps = 30
time = np.linspace(0, total_time, steps)
dt = total_time / steps;

stiffness = scipy.io.loadmat('transient_solver-heat_matrix_stiffness.mat')['matrix_stiffness']
mass = scipy.io.loadmat('transient_solver-heat_matrix_mass.mat')['matrix_mass']
mass = mass / dt
matrix_lhs = mass + stiffness
rhs = scipy.io.loadmat('transient_solver-heat_rhs.mat')['rhs']
other = scipy.io.loadmat('transient_solver-heat_other.mat')['other']

point_n = find_index(other, 3.759e-3, 4.463e-2)
point_meas = find_index(other, 6.009e-3, 9.668e-3)
# point_meas = find_index(other, 3.759e-3, 4.463e-2)

u = np.zeros(steps)
u[:int(steps/4)] = np.ones(int(steps/4)) * 1.7 * 2
u[int(steps/4):int(steps/3)] = np.ones(int(steps/3) - int(steps/4)) * 0.8 * 1.7 * 2
u[int(steps/3):] = np.ones(steps-int(steps/3)) * 0.1 * 1.7 * 2

slnt = np.zeros([len(rhs), steps])
for i in range(1, steps):            
    slnt[:, i] = la.spsolve(matrix_lhs, mass @ slnt[:,i-1] + rhs[:,0] * u[i])
    

c = np.dot(slnt, slnt.T)
[D, V] = (np.linalg.eigh(c))

L = np.zeros([len(V), num])
L [:,:]= V[:, -num:]


mor_rhs = np.dot(L.T, rhs) 
mor_mass = L.T @ mass @ L 


mor_lhs = L.T @ matrix_lhs @ L
A = np.linalg.inv(mor_lhs) @ mor_mass
B = np.linalg.inv(mor_lhs) @ mor_rhs
C = L[point_n, :]

x= np.zeros([num, steps])
y = np.zeros(steps)

for i in range(0, steps):
    x[:, i] = A @ x[:, i-1] + B.T * u[i]
    y[i] = C @ x[:, i-1]

# H_c[3, :] = C[:] @ A @ A @ A
y_hat = []
C_bar = L[point_meas, :]
Y = np.zeros([num, 1])

for k in range(steps-num):    
    H_c = np.zeros([num, num])
        
    for i in range(num): 
        H_c[i, :] = C[:] 
        for j in range(i):
            H_c[i, :] = H_c[i, :] @ A 
            
    hc_inv = np.linalg.inv(H_c)
    
    coefs = []
    for i in range(1, num):
        coef = C
        for j in range(i-1):
            coef = coef @ A
        coef = coef @ B
        coefs.append(coef)
    
    Y[0, 0] = y[k]
    for i in range(1, num):
        Y[i, 0] = y[k+i]
        for j in range(0, i):
            Y[i, 0] = Y[i, 0] - coefs[i-j-1] * u[k + j]

    x_hat = hc_inv @ Y[:num, 0]
    y_hat.append(C_bar @ x_hat[:])    

pl.figure(0)
pl.plot(time[:steps-num], y_hat[:steps-num], 'b--')
pl.grid()
pl.tick_params(axis='both', which='major', labelsize=16)
pl.tick_params(axis='both', which='minor', labelsize=12)
pl.plot(time, slnt[point_meas, :], 'k')
pl.plot(time, y[:], 'g')
pl.plot(time, slnt[point_n, :], 'r')
pl.xlabel(r'$t$ [s]', size=16)
pl.ylabel(r'$T [^\circ \mathrm{C}]$ ', size=16)
pl.tight_layout()
pl.savefig('comparison.png')


pl.tick_params(axis='both', which='major', labelsize=16)
pl.tick_params(axis='both', which='minor', labelsize=12)

pl.figure(1)
pl.plot(time[:steps-num], slnt[point_meas, :steps-num] - y_hat, '--k')
pl.ylabel(r'$\Delta T [^\circ \mathrm{C}]$ ', size=16)
pl.xlabel(r'$t$ [s]', size=16)
pl.grid()
pl.tight_layout()
pl.savefig('error.png')
pl.show()
