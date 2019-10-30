import unittest
from artap.dynamical_systems import DiscreteLTISystem
from artap.dynamical_systems import Model
from artap.dynamical_systems import Gain
from artap.dynamical_systems import ContinuousLTISystem
import pylab as pl


class TestDynamicalSystems(unittest.TestCase):

    def test_discrete_LTI(self):

        matrix_a = [[-1, 0],
                    [0, -1]]

        matrix_c = [[1, 0], [0, 1]]

        matrix_b = [[1], [2]]
        matrix_d = [0]

        plant = Model(dt=0.1)
        x_0 = [10, 5]
        system = DiscreteLTISystem(plant, matrix_a, matrix_b, matrix_c, matrix_d, x_0, dt=1)
        plant.run(10)

        self.assertEqual(len(system.archive_t), len(system.archive_u))
        self.assertEqual(len(system.archive_t), len(system.archive_x))
        self.assertEqual(len(system.archive_t), len(system.archive_y))
        self.assertEqual(system.archive_x[0][0], x_0[0])
        self.assertEqual(system.archive_x[0][1], x_0[1])
        self.assertAlmostEqual(system.archive_x[-2][0], -10)
        self.assertAlmostEqual(system.archive_x[-2][1], -5)

    def test_continuous_LTI(self):
        plant = Model(dt=0.1)
        A = [[-1,  -1],
             [1,  0]]

        C = [0,  1]

        B = [[1], [1]]
        D = [0]

        plant = Model(dt=0.01)
        x0 = [10, 5]
        system = ContinuousLTISystem(plant, A, B, C, D, x0)
        plant.run(10)
        system.plot('output')
        # pl.show()


# A = [[-1, 0],
#      [0, -1]]
#
# C = [[1, 0], [0, 1]]
#
# B = [[1], [2]]
# D = [0]
#
# plant = Model(dt=0.1)
# x0 = [10, 5]
# system = DiscreteLTISystem(plant, A, B, C, D, x0, dt=1)
# system.connect(unit_step)
# plant.run(10)
# system.plot('output')
# pl.show()


# plant = Model(dt=0.1)
# x0 = [4000, 280]
# A = [[1,  1],
#      [0,  1]]
#
# C = [[1,  0], [0,  1]]
#
# B = [[1], [2]]
# D = [0]
#
#
# def train_sequence(time):
#
#     y = np.array([4000, 280])
#     if time == 1:
#         y = np.array([4260, 282])
#     if time == 2:
#         y = np.array([4550, 285])
#     if time == 3:
#         y = np.array([4860, 286])
#     if time == 4:
#         y = np.array([5110, 290])
#     return y
#
#
# error_obs = [25, 6]
# error_proc = [20, 5]
#
# system = DiscreteLTISystem(plant, A, B, C, D, x_0=x0, dt=1)
# kalman_filter = KalmanFilter(plant, system, dt=1, error_obs=error_obs, error_proc=error_proc)
#
# system.connect(unit_step)
# kalman_filter.connect(unit_step)
# kalman_filter.connect(train_sequence, 1, 1)
#
# plant.run(3)
# kalman_filter.plot('output', index=1)
# pl.show()


# plant = Model(0.1)
# pi = PI(plant, 1, 0.015)
# pi.connect(unit_step)
# sumator = Sum(plant, [1, 1])
# sumator.connect(pi.output, output_index=0, input_index=0)
# sumator.connect(unit_step, output_index=0, input_index=1)
# plant.run(10)
# sumator.plot('output')
# pl.show()


# A = [[-1,  -1],
#      [0,  -1]]
#
# C = [[1,  0], [0,  1]]
#
# B = [[1, 1], [2, 2]]
# D = [0, 0]
#
# plant = Model(dt=0.01)
# x0 = [0, 1]
# system = ContinuousLTISystem(plant, A, B, C, D, x0)
# plant.run(100)
# system.plot('state')
# pl.show()

# x0 = [0, 0, 0]
# A = [[-1,  -1,  0],
#      [1,  0, -1],
#      [0,  1, 0]]
#
# C = [[1,  0,  0]]
#
# B = [[1], [-1], [2]]
# D = [0]
#
# plant = Model(dt=0.01)
# system = ContinuousLTISystem(plant, A, B, C, D, x0)
# system.connect(unit_step, output_index=0, input_index=0)
# plant.run(20)
# system.plot('output')
# pl.show()
# T = system.observability_matrix()
# T_1 = np.linalg.inv(T)
# A_ = T @ A @ T_1
# B_ = T @ B
# C_ = C @ T
# x0_ = T @ x0
# print(A_)
# print(B_)
# print(C_)
#
# plant = Model(dt=0.01)
# system_ = ContinuousLTISystem(plant, A_, B_, C_, D, x0_)
# system_.connect(unit_step, output_index=0, input_index=0)
# plant.run(20)
# system_.plot('output')
# pl.show()
# print((A_[-1]))
# nom = list(np.array(B_)[:, 0])
# nom.reverse()
# print(nom)
# print(np.roots(nom))


# A = [[0.596,   -0.214,   -0.051,    0.002],
#      [-0.435,    0.642,  -0.093,    0.004],
#      [-0.152,   -0.166,   0.933,    0.004],
#      [0.278,    0.350,    0.109,    0.994]]
#
# B = [[-60.846],
#      [-107.441],
#      [-83.854],
#      [217.776]]
#
# C = [[.0287,    0.0081,    0.0181,    0.0208]]
#
# D = [0]
#
# x0 = [0, 0, 0, 0]
#
# error_obs = [1]
# error_proc = [100, 100, 100, 100]
#
# plant = Model(dt=0.01)
# system = DiscreteLTISystem(plant, A, B, C, D, x0, dt=0.1)
# system.connect(programme_control)
# suma = Sum(plant, signs=[1, 1])
# suma.connect(system.output, input_index=1, output_index=0)
# suma.connect(white_noise, input_index=0, output_index=0)
# kalman_filter = KalmanFilter(plant, system, dt=0.1, error_obs=error_obs, error_proc=error_proc)
# kalman_filter.connect(programme_control)
# kalman_filter.connect(suma.output, input_index=1, output_index=0)
# plant.run(400)
# suma.plot('output')
# pl.figure()
# kalman_filter.plot('output')
# system.plot('output')
# pl.show()

# dt = 0.2
#
# A = [[1,   0,   0,    0],
#      [dt,  1,   0,    0],
#      [0,   0,   1,    0],
#      [0,   0,   dt,   1]]
#
# B = [[0],
#      [0],
#      [-9.8],
#      [0]]
#
# C = [[1,    0,    0,    0],
#      [0,    1,    0,    0],
#      [0,    0,    1,    0],
#      [0,    0,    0,    1]]
#
# D = [[0], [0], [0], [0]]
#
# x0 = [-600, 3e3, 100, 600]
#
# error_obs = [10, 10, 10, 10]
# error_proc = [200, 20, 20, 20]
#
# plant = Model(dt=0.01)
# system = DiscreteLTISystem(plant, A, B, C, D, x0, dt=0.2)
# system.connect(unit_step)
#
# suma = Sum(plant, signs=[1.0, 1.0])
# # suma.connect(system.output, input_index=0, output_index=0)
# suma.connect(white_noise, input_index=0, output_index=0)
# kalman_filter = KalmanFilter(plant, system, dt=0.2, error_obs=error_obs, error_proc=error_proc)
#
# kalman_filter.connect(unit_step)
# kalman_filter.connect(system.output, input_index=1, output_index=0)
# plant.run(6.5)
# kalman_filter.plot('input')
#
# x = system.get_state()
# pl.plot(x[3])
# x_hat = kalman_filter.get_state()
# pl.plot(x_hat[3], 'x')
# pl.show()
# pl.figure(1)
# system.plot('output',index=0)
# pl.show()


if __name__ == '__main__':
    unittest.main()
