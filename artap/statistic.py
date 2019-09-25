#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:34:51 2019

@author: david
"""
from agrossuite import agros as a2d

print(a2d.datadir())

#import numpy as np
#import scipy.stats as stats
#
#a = [5.32, 5.24, 5.47, 4.98, 5.16]
#b = [5.88, 5.31, 4.86, 5.45, 5.12]
#c = [5.32, 4.21, 5.44, 5.33, 5.24]
#
#a_bar = np.mean(a)
#b_bar = np.mean(b)
#c_bar = np.mean(c)
#
#n = len(a)
#m = 3
#
#s_a = 1 / (n-1) * sum((a - a_bar)**2)
#s_b = 1 / (n-1) * sum((b - b_bar)**2)
#s_c = 1 / (n-1) * sum((c - c_bar)**2)
#
#
#x_bar = 1 / m * (a_bar + b_bar + c_bar)
#
#s_x = 1 / (m -1) * ((a_bar - x_bar)**2 + (b_bar - x_bar)**2 + (c_bar - x_bar)**2) # rozptyl mezi třídami
#s_p = 1 / m * ((s_a) + (s_b) + (s_c))
#
#F_r = 5 * s_x / s_p
#
#print(F_r)
#
#stats.f_oneway(a, b, c)
## print(s_a)
## print(s_b)
## print(s_c)
#
## print(s)


