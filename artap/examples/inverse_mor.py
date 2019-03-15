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

num = 3
total_time = 25;
steps = 250;

dt = total_time / steps;

stiffness = scipy.io.loadmat('transient_solver-heat_matrix_stiffness.mat')['matrix_stiffness']
mass = scipy.io.loadmat('transient_solver-heat_matrix_mass.mat')['matrix_mass']
mass = mass /dt

matrix_lhs = mass + stiffness

rhs = scipy.io.loadmat('transient_solver-heat_rhs.mat')['rhs']
# u = scipy.io.loadmat('transient_solver-heat_solutions.mat')['slns']
 
u = np.zeros(steps)
u[:70] = np.ones(70) * 2.5


slnt = np.zeros([len(rhs), steps])
for i in range(1, steps):            
    slnt[:, i] = la.spsolve(matrix_lhs, mass @ slnt[:,i-1] + rhs[:,0] * u[i])
    
   
c = np.dot(slnt, slnt.T)
[D, V] = (np.linalg.eigh(c))

L = np.zeros([len(V), num])
L [:,:]= V[:, -num:]


mor_rhs = np.dot(L.T, rhs) 
mor_mass = L.T @ mass @ L 
point_n = 1000
#
##

pl.tick_params(axis='both', which='major', labelsize=14)
pl.tick_params(axis='both', which='minor', labelsize=10)

pl.tight_layout()
pl.figure(0)
pl.grid()
pl.plot(slnt[point_n, :] + 293.15, 'rx')
pl.plot(slnt[point_n-10, :] + 293.15, 'gx')
pl.plot(slnt[point_n+10, :] + 293.15, 'bx')
pl.xlabel(r'$t$ [s]', size=16)
pl.ylabel(r'$T [^\circ \mathrm{C}]$ ', size=16)
pl.show()
#pl.savefig('comparison.pdf')
print(len(slnt))




