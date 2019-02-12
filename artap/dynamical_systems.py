#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 13:20:29 2019

@author: david
"""

import numpy as np
import pylab as pl
import random as rn


class Model:
    def __init__(self):
        self.time = 0
        self.dt = 0.01  # Sampling period
        self.systems = []

    def add_system(self, sub_system):
        sub_system.dt = self.dt
        self.systems.append(sub_system)

    def run(self, n):
        for i in range(n):
            self.time += self.dt
            for sub_system in self.systems:
                sub_system.step(self.time)

    def add_LTI(self, A, B, C, D, x0):
        sub_system = LTISystem(A, B, C, D, x0)
        self.add_system(sub_system)
        sub_system.dt = self.dt
        return sub_system

    def add_kalman_filter(self, controlled_system):
        sub_system = KalmanFilter(controlled_system, self.dt)
        self.add_system(sub_system)
        return sub_system

    def add_sum(self, signs):
        sub_system = Sum(signs)
        self.add_system(sub_system)
        return sub_system

    def add_pi(self, p, i, x0=0):
        sub_system = PI(p, i, x0)
        self.add_system(sub_system)
        return sub_system


class System:
    def __init__(self):
        self.inputs = []
        self.archive_time = [0]
        self.archive_y = []
        self.archive_x = []
        self.archive_u = []
        self.connections = []
        self.dt = 0

    def initialize(self, x, y, B):

        for i in range(len(x)):
            self.archive_x.append([float(x[i])])

        if y.size == 1:
            self.archive_y.append([y])
        else:
            for i in range(y.size):
                self.archive_y.append([y[i]])

        for i in range(self.B.shape[1]):
            self.archive_u.append([0])
            self.add_input()

    def update_data(self, u, x, y, time):

        if len(u) == 1:
            self.archive_u[0].append(float(u))
        else:
            for i in range(u.size):
                self.archive_u[i].append(float(u[i]))

        for i in range(len(x)):
            self.archive_x[i].append(float(x[i]))

        if y.size == 1:
            self.archive_y[0].append(float(y))
        else:
            for i in range(len(y)):
                self.archive_y[i].append(float(y[i]))

        self.archive_time.append(time)

    def add_input(self, inp=None):
        self.inputs.append(inp)
        self.connections.append(None)

    def connect(self, system_output, output_index=0, input_index=0):
        self.inputs[input_index] = system_output
        self.connections[input_index] = output_index

    def output(self, time, index=0):
        if self.y.size == 1:
            return self.y
        else:
            return self.y[index]

    def plot(self, item='output'):
        # t = self.dt * np.linspace(0, len(self.archive_y), len(self.archive_y))
        # print(self.archive_time)
        # pl.figure()
        if item == 'output':
            for y in self.archive_y:
                pl.plot(self.archive_time, y)
            pl.ylabel('y[-]')

        if item == 'input':
            for u in self.archive_u:
                pl.plot(self.archive_time, u)
            pl.ylabel('u[-]')

        if item == 'state':
            for x in self.archive_x:
                pl.plot(self.archive_time, x)
            pl.ylabel('x[-]')

        pl.xlabel('t[s]')
        pl.grid()


class Sum(System):
    def __init__(self, signs):
        super().__init__()
        self.signs = signs
        self.archive_y.append(0)

    def output(self, time, index=0):
        output = 0
        for i in range(len(self.inputs)):
            output += self.signs[i] * self.inputs[i](time, index)
        self.archive_y.append(output)
        self.archive_time.append(time)
        return output

    def step(self, time):
        self.output(time, 0)


class PI(System):
    def __init__(self, p, i, x0=0):
        super().__init__()
        self.x = x0
        self.archive_x = [self.x]
        self.y = x0
        self.archive_y = [self.y]
        self.archive_u = [0]
        self.dt = 0
        self.i = i
        self.p = p
        self.add_input()

    def step(self, time):
        self.x = self.x + self.dt * self.i * self.inputs[0](time)
        self.y = self.x + self.inputs[0](time) * self.p

        self.archive_x.append(self.x)
        self.archive_y.append(self.y)
        self.archive_u.append(self.inputs[0](time))
        self.archive_time.append(time)


class LTISystem(System):
    def __init__(self, A, B, C, D, x0):
        super().__init__()
        self.x = np.transpose(np.array(x0))
        self.A = np.matrix(A)
        self.B = np.matrix(B)
        self.C = np.matrix(C)
        self.D = np.matrix(D)

        self.x = np.transpose(np.matrix(x0))
        self.y = np.matrix(np.dot(self.C, self.x))

        self.initialize(self.x, self.y, B)
        self.dt = 0

    def step(self, time):
        u = list()
        for i in range(len(self.inputs)):
            u.append(self.inputs[i](time, self.connections[i]))
        u = np.transpose(np.matrix(u))
        self.x = self.dt * np.dot(self.A, self.x) + self.x + self.dt * np.dot(self.B, u + (rn.random() - 0.5) * 0.2)
        self.y = np.array(np.dot(self.C, self.x) + np.dot(self.D, u)) + (rn.random() - 0.5) * 0.2
        self.update_data(u, self.x, self.y, time)


class KalmanFilter(System):
    def __init__(self, controlled_system: System, dt):
        super().__init__()
        n = len(controlled_system.x)
        self.n = n
        self.dt = dt
        self.A = self.dt * controlled_system.A + np.eye(n)
        self.B = controlled_system.B * self.dt
        self.C = controlled_system.C
        self.D = controlled_system.D

        self.x = np.zeros([n, 1])
        self.y = np.zeros(n + 1)

        self.initialize(self.x, self.y, self.B)
        self.add_input()
        self.archive_u.append([0])

        self.error_obs_x_1 = 1
        self.error_obs_x_2 = 1

        self.error_proc_x_1 = 1
        self.error_proc_x_2 = 1

        # self.Q = np.eye(n)
        self.P = self.covariance2d(self.error_obs_x_1, self.error_obs_x_2)
        self.R = self.covariance2d(self.error_obs_x_1, self.error_obs_x_2)
        self.Q = 2 * self.covariance2d(self.error_obs_x_1, self.error_obs_x_2)
        print(self.Q)

    def covariance2d(self, sigma1, sigma2):
        cov1_2 = sigma1 * sigma2
        cov2_1 = sigma2 * sigma1
        cov_matrix = np.array([[sigma1 ** 2, cov1_2],
                               [cov2_1, sigma2 ** 2]])
        return np.diag(np.diag(cov_matrix))

    def step(self, time):
        u = list()
        for i in range(len(self.inputs)):
            u.append(float(self.inputs[i](time, self.connections[i])))
        u = np.matrix(u).T

        # Prediction steps
        self.x = np.dot(self.A, self.x) + np.dot(self.B, u[0])

        self.P = np.dot(np.dot(self.A, self.P), self.A.T)

        S = self.R + np.dot(self.C, np.dot(self.P, self.C.T))
        K = self.P.dot(C).dot(np.linalg.inv(S))

        # Difference between real output and estimated output
        y = u[1] - np.dot(self.C, self.x)
        # Update equation

        self.x = self.x + K.T.dot(y)
        self.P = self.P + np.dot(self.C, np.dot(self.P, self.C.T))

        I = np.eye(self.n)
        self.P = (I - K.T.dot(self.C).dot(self.P))
        self.y = self.C.dot(self.x)
        self.update_data(u, self.x, self.y, time)


def unit_step(t, index=0):
    if t > 0:
        return 1
    else:
        return 0


def unit_impulse(t, index=0):
    if t == 0:
        return 1
    else:
        return 0


def zeros():
    return 0


def white_noise():
    return np.random.normal(0., 0.1, 1)


# # Linear time invariant system with two inputs
# A = [[-1, 0], [0, -0.5]]
# B = [[1, 0], [0, 1]]
# C = [[1, 0], [0, 0.5]]
# D = [[0, 0], [0, 0]]
#
# x0 = [0, 0]
# model = Model()
# system = model.add_LTI(A, B, C, D, x0)
# system.connect(unit_impulse)
# system.connect(unit_step, 1, 1)
#
# C = [1, 1]
# B = [[1], [0]]
# D = [0]
# system_2 = model.add_LTI(A, B, C, D, x0)
#
# sum_block = model.add_sum([1, -1])
# sum_block.add_input(white_noise)
# sum_block.add_input(system_2.output)
#
# # Pi controller
# pi = model.add_pi(0.4, 0.8)
# pi.connect(sum_block.output)
#
# system_2.connect(pi.output)
#
# model.run(100)
# # system_2.plot()
# # system.plot()
# # system_2.plot()
# system.plot('state')
# sum_block.plot()
# pl.show()
# # system_2.plot()
# # sum_block.plot()
# # pi.plot()

# Kalman filter example
model = Model()
x0 = [10, 10]
A = [[-0.01, 0], [0, -1]]
C = [1, 0]
B = [[1], [0]]
D = [0]
system = model.add_LTI(A, B, C, D, x0)
kfilter = model.add_kalman_filter(system)
system.connect(unit_step)

kfilter.connect(unit_step)
kfilter.connect(system.output, 1, 1)

model.run(2500)
system.plot('state')
kfilter.plot('state')
# system.plot('state')

pl.show()
