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
    def __init__(self, dt=0):
        self.time = 0
        self.dt = dt  # Sampling period
        self.systems = []

    def add_system(self, sub_system):
        sub_system.dt = self.dt
        self.systems.append(sub_system)

    def run(self, n):
        for i in range(n):
            self.time += self.dt
            for sub_system in self.systems:
                sub_system.step(self.time)

    def add_LTI(self, A, B, C, D, x0, dt):
        sub_system = LTISystem(A, B, C, D, x0, dt)
        self.add_system(sub_system)
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
    def __init__(self, dt):
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
            return self.y

    def plot(self, item='output'):
        # t = self.dt * np.linspace(0, len(self.archive_y), len(self.archive_y))
        # print(self.archive_time)
        # pl.figure()
        if item == 'output':
            for y in self.archive_y:
                pl.plot(self.archive_time, self.archive_y[0])
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
        self.x = self.x + self.i * self.inputs[0](time)
        self.y = self.x + self.inputs[0](time) * self.p

        self.archive_x.append(self.x)
        self.archive_y.append(self.y)
        self.archive_u.append(self.inputs[0](time))
        self.archive_time.append(time)


class LTISystem(System):
    def __init__(self, A, B, C, D, x0=None, dt=0):
        super().__init__(dt)
        self.x = np.transpose(np.array(x0))
        self.A = np.matrix(A)
        self.B = np.matrix(B)
        self.C = np.matrix(C)
        self.D = np.matrix(D)
        if x0 is None:
            self.x = np.zeros([self.n, 1])
        else:
            self.x = np.transpose(np.matrix(x0))
        self.y = np.matrix(np.dot(self.C, self.x))

        self.initialize(self.x, self.y, B)

    def discretize(self, dt, method = None):
        if dt != 0:
            if method is None:
                self.A = np.eye(self.n) + dt * self.A
                self.B = dt * self.B

    def step(self, time):
        if self.dt == 0:
            pass
        else:
            if time == self.archive_time[-1] + self.dt:
                u = list()
                for i in range(len(self.inputs)):
                    u.append(self.inputs[i](time, self.connections[i]))
                u = np.transpose(np.matrix(u))
                self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
                self.y = np.array(np.dot(self.C, self.x) + np.dot(self.D, u))
                if time == 0:
                    self.y = np.array([[4000], [280]])
                if time == 1:
                    self.y = np.array([[4260], [282]])
                if time == 2:
                    self.y = np.array([[4550], [283]])
                if time == 3:
                    self.y = np.array([[4860], [286]])
                if time == 4:
                    self.y = np.array([[5110], [290]])

                self.update_data(u, self.x, self.y, time)


class KalmanFilter(System):
    def __init__(self, controlled_system: System, dt):
        super().__init__(dt)
        n = len(controlled_system.x)
        self.n = n
        self.dt = dt
        self.A = controlled_system.A
        self.B = controlled_system.B
        self.C = controlled_system.C
        self.D = controlled_system.D

        self.x = np.matrix([[4000], [280]])
        self.y = self.C @ self.x

        self.initialize(self.x, self.y, self.B)
        self.add_input()
        self.archive_u.append([0])

        self.error_obs = [25, 6]
        self.error_proc = [20, 5]

        self.P = self.covariance(self.error_proc)
        self.R = self.covariance(self.error_obs)
        self.Q = np.zeros(n)


    def covariance(self, sigma):
        cov_matrix = np.eye(len(sigma))
        for i in range(len(sigma)):
            cov_matrix[i, i] = sigma[i]**2
        return cov_matrix

    def step(self, time):
        u = self.inputs[0](time)
        y_meas = self.inputs[1](time)
        # for i in range(len(self.inputs)):
        # u.append(float(self.inputs[i](time, self.connections[i])))

        u = np.transpose(np.matrix(u))

        # Prediction steps
        self.x = self.A @ self.x + self.B * u[0]

        P = self.A @ self.P @ self.A.T + self.Q
        self.P = np.eye(self.n)

        for i in range(self.n):
            self.P[i, i] = P[i, i] # Takes only diagonal

        S = self.R + self.C @ self.P @ self.C.T
        K = self.P @ self.C @ np.linalg.inv(S)

        # Difference between real output and estimated output

        y = self.C @ self.x

        # Update equation
        self.x = self.x + K.T @ (y_meas - y)

        I = np.eye(self.n)
        self.P = (I - K @ self.C )@ self.P
        print(self.x)

        self.y = self.C @ self.x
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


model = Model(dt=1)

x0 = [4000, 280]
A = [[1,  1],
     [0,  1]]

C = [[1,  0], [0,  1]]

B = [[1], [2]]
D = [0]

system = model.add_LTI(A, B, C, D, x0=x0, dt=1)
kfilter = model.add_kalman_filter(system)
system.connect(unit_step)
kfilter.connect(unit_step)
kfilter.connect(system.output, 1, 1)
model.run(3)
kfilter.plot('output')
system.plot('output')
pl.show()
