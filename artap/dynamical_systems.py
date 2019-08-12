#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 13:20:29 2019

@author: david
"""

import numpy as np
import pylab as pl


class Model:
    def __init__(self, dt=0.0):
        self.t = 0
        self.type = ""
        self.dt = dt  # Sampling period
        self.systems = []

    def run(self, t):
        n = int(t / self.dt)
        for i in range(n):
            for sub_system in self.systems:
                if sub_system.type == 'discrete':
                    if abs(self.t - sub_system.k * sub_system.dt) < 1e-12:
                        sub_system.discrete_step()
                else:
                    sub_system.continuous_step(self.dt)
            self.t += self.dt


class System:
    def __init__(self, model=None, x_0=None, dt=0, n_inputs=1, n=1):

        self.n = n
        if model is not None:
            self.model = model
            self.model.systems.append(self)

        if x_0 is None:
            self.x = np.zeros(n)
        else:
            self.x = x_0

        self.t = 0
        self.k = 0
        self.dt = dt
        self.y = []                     # current output
        self.u = np.zeros(n_inputs)     # current input

        self.inputs = []
        self.connections = []
        for i in range(n_inputs):
            self.inputs.append(self.dummy_input)
            self.connections.append(0)

        self.archive_t = []
        self.archive_y = []
        self.archive_x = []
        self.archive_u = []

        self.integrate = self.runge_kutta_step
        self.type = None

    def connect(self, system_output, output_index=0, input_index=0):
        self.inputs[input_index] = system_output
        self.connections[input_index] = output_index

    @staticmethod
    def dummy_input(t=None):
        return [t*0]

    def update_input(self):
        u = []
        for i in range(len(self.inputs)):
            inputs = self.inputs[i](self.t)
            index = self.connections[i]
            u.append(inputs[index])
        self.u = np.array(u)

    def update_output(self):
        return self.y

    def update_state(self):
        return self.x

    def output(self, time=None, index=0):
        return self.y

    def continuous_step(self, dt=0.0):
        self.dt = dt
        self.integrate()
        self.save_step()

    def discrete_step(self):
        self.k += 1
        self.t = self.k * self.dt
        self.update_input()
        self.x = self.update_state()
        self.y = self.update_output()
        self.save_step()

    def euler_step(self):
        self.t = self.t + self.dt
        self.update_input()
        self.x = self.x + self.dt * self.update_state()
        return self.x

    def runge_kutta_step(self):
        self.t = self.t + self.dt
        self.update_input()
        a = self.update_state()
        self.x = self.x + self.dt / 2 * a
        b = self.update_state()
        self.x = self.x + self.dt / 2 * b
        c = self.update_state()
        self.x = self.x + self.dt * c
        d = self.update_state()
        self.x = self.x + self.dt / 6 * (a + 2 * b + 2 * c + d)

    def save_step(self):
        self.archive_t.append(self.t)
        self.archive_u.append(self.u)
        self.archive_x.append(self.x)
        self.archive_y.append(self.update_output())

    def get_state(self):
        table = []
        for i in range(len(self.x)):
            x = []
            for item in self.archive_x:
                x.append(item[i])
            table.append(x)
        return table

    def plot(self, signal='output', index=None):
        # t = self.dt * np.linspace(0, len(self.archive_y), len(self.archive_y))
        # print(self.archive_time)
        # pl.figure()

        pl.grid(True)
        if signal == 'output':
            y = []

            if type(self.y) == np.array:
                n = len(self.y)
            else:
                n = 1
            for i in range(n):
                y.append([])
                for item in self.archive_y:
                    if n == 1:
                        y[i].append(item)
                    else:
                        y[i].append(item[i])

                if index is None:
                    pl.plot(self.archive_t, y[i], label='y')
                else:
                    if i == index:
                        pl.plot(self.archive_t, y[i], label='y')
        pl.ylabel('y[-]')

        if signal == 'input':
            for u in self.archive_u:
                pl.plot(self.archive_t, u)
            pl.ylabel('u[-]')

        if signal == 'state':
            for i in range(len(self.x)):
                x = []
                for item in self.archive_x:
                    x.append(item[i])
                pl.plot(self.archive_t, x, label='x_{0}'.format(i))

            pl.ylabel('x[-]')
            pl.legend()

        pl.xlabel('t[s]')


class Gain(System):

    def __init__(self, model=None, gain=1.0):
        super().__init__()
        self.gain = gain
        self.model = model

    def output(self, time=None, index=0):
        self.update_input()
        self.archive_t.append(time)
        self.archive_y.append(self.u * self.gain)
        return self.u * self.gain


class LTISystem(System):
    def __init__(self, model=None, matrix_a=None, matrix_b=None,
                 matrix_c=None, matrix_d=None, x_0=None, dt=0.0):

        self.matrix_a = np.array(matrix_a)
        self.matrix_b = np.array(matrix_b)
        self.matrix_c = np.array(matrix_c)
        self.matrix_d = np.array(matrix_d)
        self.n_inputs = len(matrix_b[0])
        self.n_outputs = len(matrix_c)
        self.n = len(matrix_a)
        self.u = np.zeros(self.n_inputs)

        super().__init__(model, x_0, n_inputs=self.n_inputs, n=self.n, dt=dt)

    def observability_matrix(self):
        n = len(self.x)
        h_o = np.zeros([n, n])
        for i in range(n):
            h_o[i, :] = self.matrix_c[:]
            for j in range(i):
                h_o[i, :] = h_o[i, :] @ self.matrix_a
        return h_o


class ContinuousLTISystem(LTISystem):
    def __init__(self, model=None, matrix_a=None, matrix_b=None,
                 matrix_c=None, matrix_d=None, x_0=None):

        self.type = 'continuous'
        super().__init__(model, matrix_a, matrix_b, matrix_c, matrix_d, x_0)
        self.y = self.update_output()
        self.save_step()

    def update_state(self):
        self.update_input()
        dx = self.matrix_a @ self.x + self.matrix_b @ self.u
        return dx

    def update_output(self):
        self.y = self.matrix_c @ self.x + self.matrix_d @ self.u
        return self.y


class DiscreteLTISystem(LTISystem):
    def __init__(self, model, matrix_a, matrix_b, matrix_c, matrix_d, x_0=None, dt=0.0):
        super().__init__(model, matrix_a, matrix_b, matrix_c, matrix_d, x_0, dt)
        self.type = 'discrete'
        self.dt = dt
        self.x = np.array(x_0)
        self.save_step()

    def update_state(self):
        self.update_input()
        self.x = self.matrix_a @ self.x + self.matrix_b @ self.u
        return self.x

    def update_output(self):
        self.update_input()
        self.y = self.matrix_c @ self.x + self.matrix_d @ self.u
        return self.y


class Sum(System):
    def __init__(self, model: Model, signs):
        self.n_inputs = len(signs)
        super().__init__(model, n_inputs=self.n_inputs)
        self.type = 'continuous'
        self.signs = signs
        self.archive_y.append([0])
        self.archive_t.append(0)
        self.y = 0

    def output(self, time=None, index=0):
        output = 0
        for i in range(len(self.inputs)):
            output += self.signs[i] * self.inputs[i](time)[0]

        self.archive_y.append([output])
        self.y = [output]
        self.archive_t.append(self.model.t)
        return output

    def continuous_step(self, time):
        self.output(time, 0)


class PI(System):
    def __init__(self, model: Model, p, i, x_0=None):
        super().__init__(model, x_0=x_0)
        self.y = self.x
        self.i = i
        self.p = p
        self.save_step()

    def continuous_step(self, time):
        self.update_input()
        self.x = self.x + self.i * self.u
        self.y = self.x + self.u * self.p
        self.t = time
        self.save_step()


class KalmanFilter(DiscreteLTISystem):
    def __init__(self, model: Model, controlled_system: DiscreteLTISystem, dt, error_obs, error_proc):

        self.n = len(controlled_system.x)
        self.controlled_system = controlled_system
        n_inputs = controlled_system.n_inputs + len(controlled_system.matrix_c)

        x0 = [-600, 3e3, 100, 500]
        super().__init__(model, controlled_system.matrix_a, controlled_system.matrix_b,
                         controlled_system.matrix_c, controlled_system.matrix_d, x_0=x0, dt=dt)

        for i in range(n_inputs):
            self.inputs.append(self.dummy_input)
            self.connections.append(0)

        self.error_proc = error_proc
        self.error_obs = error_obs

        self.P = self.covariance(self.error_proc)
        self.R = self.covariance(self.error_obs)
        self.Q = np.zeros(self.n)


    @staticmethod
    def covariance(sigma):
        cov_matrix = np.eye(len(sigma))
        for i in range(len(sigma)):
            cov_matrix[i, i] = sigma[i] ** 2
        return cov_matrix

    def update_output(self):
        # self.y = self.x
        return self.y

    def discrete_step(self):
        u = self.inputs[0](self.t)

        # Prediction steps
        self.x = self.matrix_a @ self.x + self.matrix_b @ u

        matrix_p = self.matrix_a @ self.P @ self.matrix_a.T + self.Q
        self.P = np.eye(self.n)

        for i in range(self.n):
            self.P[i, i] = matrix_p[i, i]  # Takes only diagonal

        matrix_s = self.R + self.matrix_c @ self.P @ self.matrix_c.T
        matrix_k = self.P @ self.matrix_c.T @ np.linalg.inv(matrix_s)

        # Difference between real output and estimated output
        self.k = self.k + 1
        self.t = self.k * self.dt
        y_meas = np.array(self.inputs[1](self.t))
        y = self.matrix_c @ self.x

        # Update equation
        self.x = self.x + matrix_k @ (y_meas - y)

        matrix_i = np.eye(self.n)
        self.P = (matrix_i - matrix_k @ self.matrix_c) @ self.P
        self.y = self.matrix_c @ self.x
        self.save_step()


def unit_step(t):
    if t >= 0:
        return [1]
    else:
        return [0]


def unit_impulse(t):
    if t == 0:
        return 1
    else:
        return 0


def programme_control(t):
    u = 5.5
    if t > 4:
        u = u * 0.6
    if t > 7:
        u = u * 0.35
    if t > 10:
        u = u * 0.1
    if t > 20:
        u = u * 0.1
    if t > 25:
        u = u * 1.4
    return [u + (np.random.rand()-0.5)]


def zeros():
    return 0


def white_noise(t):
    return [(np.random.rand() - 0.5) * 0]




