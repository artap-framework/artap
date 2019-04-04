#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 18:35:38 2019

@author: david
"""

import pylab as pl

file = open('M_time.txt')
lines = file.readlines()
time = []
moment = []
for line in lines:
    items = line.split()
    time.append(float(items[0])*1000)
    moment.append(float(items[1]))

pl.rcParams['figure.figsize'] = 6, 4
pl.xlabel('$t$ [ms]', fontsize=16)
pl.ylabel('$T[ \mathrm{N} \cdot \mathrm{m}]$', fontsize=16)
pl.xticks(fontsize=14)
pl.ylim([0, 4.2])
pl.yticks(fontsize=14)
pl.tight_layout()
pl.plot(time, moment, 'kx-')
pl.grid()

pl.savefig('moment.pdf')

