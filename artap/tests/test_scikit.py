# import math
#
# import unittest
# from scipy import integrate
#
# from artap.problem import Problem
# from artap.algorithm_nlopt import NLopt, LN_BOBYQA
# from artap.benchmark_functions import Booth
# from artap.results import Results
# from artap.datastore import  DummyDataStore
#
#
# class MyProblemCoil(Problem):
#     def __init__(self, name, costs):
#         parameters = {'x1': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x2': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x3': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x4': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x5': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x6': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x7': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x8': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x9': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]},
#                       'x10': {'initial_value': 0.01, 'bounds': [5e-3, 50e-3]}}
#
#         super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
#         self.options['max_processes'] = 1
#         self.options['save_level'] = "individual"
#
#         # self.init_surrogate_model()
#
#     def intl22(self, R2, R, dZ, phi):
#         return math.sqrt(R2 ** 2 + R ** 2 - 2.0 * R2 * R * math.cos(phi) + dZ ** 2)
#
#     def intg(self, R2, R, dZ):
#         # div J = 0 - nonconstant current density
#         f = lambda phi: math.log(R2 - R * math.cos(phi) + self.intl22(R2, R, dZ, phi)) * math.cos(phi)
#         return integrate.quad(f, 0, 2.0 * math.pi, epsabs=1e-3, epsrel=1e-3)[0]
#
#     def inth(self, R2, R, dZ):
#         # div J = 0 - nonconstant current density
#         f = lambda phi: - math.log(dZ + self.intl22(R2, R, dZ, phi))
#         return integrate.quad(f, 0, 2.0 * math.pi, epsabs=1e-3, epsrel=1e-3)[0]
#
#     def integral(self, rc, zc, R, Z):
#         w = 0.001
#         h = 0.0015
#
#         R1 = rc
#         R2 = rc + w
#         Z1 = zc
#         Z2 = zc + h
#
#         mu0 = 4.0 * math.pi * 1e-7
#         Jext = 2e6
#         # div J = 0 - nonconstant current density
#         C = mu0 * Jext * w * h / (4 * math.pi * (Z2 - Z1) * math.log(R2 / R1))
#
#         # upper coil
#         Bru = C * (self.intg(R2, R, Z2 - Z) - self.intg(R2, R, Z1 - Z) - self.intg(R1, R, Z2 - Z) + self.intg(R1, R, Z1 - Z))
#         Bzu = C * (self.inth(R2, R, Z2 - Z) - self.inth(R2, R, Z1 - Z) - self.inth(R1, R, Z2 - Z) + self.inth(R1, R, Z1 - Z))
#
#         # lower coil
#         Brl = C * (self.intg(R2, R, -Z1 - Z) - self.intg(R2, R, -Z2 - Z) - self.intg(R1, R, -Z1 - Z) + self.intg(R1, R, -Z2 - Z))
#         Bzl = C * (self.inth(R2, R, -Z1 - Z) - self.inth(R2, R, -Z2 - Z) - self.inth(R1, R, -Z1 - Z) + self.inth(R1, R, -Z2 - Z))
#
#         return [Bru + Brl, Bzu + Bzl]
#
#     def integral_all(self, R, Z, x):
#         Br = 0.0
#         Bz = 0.0
#
#         for k in range(0, 9):
#             rc = x[k]
#             zc = k * 1.5e-3
#
#             B = self.integral(rc, zc, R, Z)
#
#             Br = Br + B[0]
#             Bz = Bz + B[1]
#
#         return [Br, Bz]
#
#     def evaluate(self, x):
#         pass
#
#
# class MyProblemCoilOne(MyProblemCoil):
#     def __init__(self, name):
#         super().__init__(name, costs=['F1'])
#
#     def evaluate(self, x):
#         B0 = 2e-3
#
#         dxy = 0.5e-3
#         nx = 8
#         ny = 8
#         dx = (5e-3 - dxy) / (nx - 1)
#         dy = (5e-3 - dxy) / (ny - 1)
#
#         f1 = 0.0
#         for i in range(0, nx):
#             xx = dxy + i * dx
#             for j in range(0, ny):
#                 yy = dxy + j * dy
#
#                 [Br, Bz] = self.integral_all(xx, yy, x)
#                 Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
#                 f1 = max(f1, Bp1s)
#
#         return [f1]
#
#
# class MyProblemCoilMultiTwo1(MyProblemCoil):
#     def __init__(self, name):
#         super().__init__(name, costs=['F1', 'F2'])
#
#     def evaluate(self, x):
#         B0 = 2e-3
#
#         dxy = 0.5e-3
#         nx = 8
#         ny = 8
#         dx = (5e-3 - dxy) / (nx - 1)
#         dy = (5e-3 - dxy) / (ny - 1)
#
#         f1 = 0.0
#         f2 = sum(x) * 1e3
#         for i in range(0, nx):
#             xx = dxy + i * dx
#             for j in range(0, ny):
#                 yy = dxy + j * dy
#
#                 [Br, Bz] = self.integral_all(xx, yy, x)
#                 Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
#                 f1 = max(f1, Bp1s)
#
#         return [1e3 * f1, 1e3 * f2]
#
#
# class MyProblemCoilMultiTwo2(MyProblemCoil):
#     def __init__(self, name):
#         super().__init__(name, costs=['F1', 'F2'])
#
#     def evaluate(self, x):
#         B0 = 2e-3
#
#         dxy = 0.5e-3
#         nx = 8
#         ny = 8
#         dx = (5e-3 - dxy) / (nx - 1)
#         dy = (5e-3 - dxy) / (ny - 1)
#
#         f1 = 0.0
#         f3 = 0.0
#         for i in range(0, nx):
#             xx = dxy + i * dx
#             for j in range(0, ny):
#                 yy = dxy + j * dy
#
#                 [Br, Bz] = self.integral_all(xx, yy, x)
#                 Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
#                 f1 = max(f1, Bp1s)
#
#                 dxsi = 0.5e-3
#                 [Brp, Bzp] = self.integral_all(xx + dxsi, yy, x)
#                 [Brm, Bzm] = self.integral_all(xx - dxsi, yy, x)
#                 Bp3 = math.sqrt((Brp - Br) ** 2 + (Bzp - Bz) ** 2) + math.sqrt((Brm - Br) ** 2 + (Bzm - Bz) ** 2)
#                 f3 = max(f3, Bp3)
#
#         return [1e3 * f1, 1e3 * f3]
#
#
# class MyProblemCoilMultiThree(MyProblemCoil):
#     def __init__(self, name):
#         super().__init__(name, costs=['F1', 'F2', 'F3'])
#
#     def evaluate(self, x):
#         B0 = 2e-3
#
#         dxy = 0.5e-3
#         nx = 8
#         ny = 8
#         dx = (5e-3 - dxy) / (nx - 1)
#         dy = (5e-3 - dxy) / (ny - 1)
#
#         f1 = 0.0
#         f2 = sum(x)*1e3
#         f3 = 0.0
#         for i in range(0, nx):
#             xx = dxy + i * dx
#             for j in range(0, ny):
#                 yy = dxy + j * dy
#
#                 [Br, Bz] = self.integral_all(xx, yy, x)
#                 Bp1s = math.sqrt((Br - 0.0)**2 + (Bz - B0)**2)
#                 f1 = max(f1, Bp1s)
#
#                 dxsi = 0.5e-3
#                 [Brp, Bzp] = self.integral_all(xx + dxsi, yy, x)
#                 [Brm, Bzm] = self.integral_all(xx - dxsi, yy, x)
#                 Bp3 = math.sqrt((Brp - Br) ** 2 + (Bzp - Bz) ** 2) + math.sqrt((Brm - Br) ** 2 + (Bzm - Bz) ** 2)
#                 f3 = max(f3, Bp3)
#
#         return [f1, f2, f3]
#
#
# class MyProblemBooth(Problem):
#     """ Describe simple one objective optimization problem. """
#     def __init__(self, name):
#         parameters = {'x_1': {'initial_value': 2.5, 'bounds': [-10, 10], 'precision': 1e-1},
#                       'x_2': {'initial_value': 1.5, 'bounds': [-10, 10], 'precision': 1e-1}}
#
#         # costs = {'F': {'type': Problem.MINIMIZE, 'value': 0.0}}
#         costs = ['F']
#
#         super().__init__(name, parameters, costs, data_store=DummyDataStore(self))
#         self.options['max_processes'] = 1
#         self.options['save_level'] = "population"
#
#         self.init_surrogate_model()
#
#     def evaluate(self, x):
#         return [Booth.eval(x)]
#
#
# class TestSimpleOptimization(unittest.TestCase):
#     """ Tests optimization problem."""
#
#     def test_local_problem_booth(self):
#         problem = MyProblemBooth("MyProblemBooth")
#
#         algorithm = NLopt(problem)
#         algorithm.options['algorithm'] = LN_BOBYQA
#         algorithm.options['n_iterations'] = 200
#         algorithm.run()
#
#         # print("surrogate_predict_counter: ", problem.surrogate_predict_counter)
#         # print("surrogate_eval_counter: ", problem.eval_counter)
#
#         results = Results(problem)
#         optimum = results.find_minimum('F')
#         self.assertAlmostEqual(optimum, 1e-6, 3)
#
#     def test_local_problem_coil_one(self):
#         problem = MyProblemCoilOne("MyProblemCoilOne")
#
#         algorithm = NLopt(problem)
#         algorithm.options['algorithm'] = LN_BOBYQA
#         algorithm.options['n_iterations'] = 50
#         algorithm.run()
#
#         #print("surrogate_predict_counter: ", problem.surrogate_predict_counter)
#         #print("surrogate_eval_counter: ", problem.eval_counter)
#
#         results = Results(problem)
#         optimum = results.find_minimum('F1')
#         self.assertAlmostEqual(optimum, 1e-6, 3)
#
# """
# class TestSimpleOptimization(unittest.TestCase):
#     def test_local_problem_booth(self):
#         problem = MyProblemCoilOne("LocalPythonProblem")
#         #problem = MyProblemMultiTwo2("LocalPythonProblem")
#
#         #algorithm = BayesOptSerial(problem)
#         #algorithm.options['verbose_level'] = 0
#         #algorithm.options['n_iterations'] = 100
#
#         algorithm = NLopt(problem)
#         algorithm.options['algorithm'] = LN_BOBYQA
#         algorithm.options['n_iterations'] = 200
# =======
#         # algorithm = BayesOptSerial(problem)
#         # algorithm.options['verbose_level'] = 0
#         # algorithm.options['n_iterations'] = 100
#
#         # algorithm = NLopt(problem)
#         # algorithm.options['algorithm'] = LN_BOBYQA
#         # algorithm.options['n_iterations'] = 200
# >>>>>>> 0c047fded2e42fe0fce8024cdb3c0856555ea07d
#
#         #algorithm = NSGA_II(problem)
#         #algorithm.options['max_population_number'] = 80
#         #algorithm.options['max_population_size'] = 20
#
#         t_s = time.time()
#
#         algorithm.run()
#
#         t = time.time() - t_s
#         print('Elapsed time:', t)
#
#         print("surrogate_predict_counter: ", problem.surrogate_predict_counter)
#         print("surrogate_eval_counter: ", problem.surrogate_eval_counter)
#
#         results = Results(problem)
#         optimum = results.find_minimum('F1')
#         print(optimum)
#         self.assertAlmostEqual(optimum, 1e-6, 3)
#
# """
# """
# def figures(name):
#     import matplotlib
#     matplotlib.use('Agg')
#
#     import pylab as pl
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     from matplotlib.figure import Figure
#     from matplotlib import rc
#
#     data_store = SqliteDataStore(database_file=name + ".sqlite")
#     problem = ProblemDataStore(data_store)
#
#     data_x = []
#     data_y = []
#     pareto_front_x = []
#     pareto_front_y = []
#     for population in problem.populations:
#         if len(population.individuals) > 1:
#             for individual in population.individuals:
#                 data_x.append(individual.costs[0])
#                 data_y.append(individual.costs[1])
#
#     results = GraphicalResults(problem)
#     pareto_front_x, pareto_front_y = results.find_pareto({'F1': Results.MINIMIZE, 'F2': Results.MINIMIZE})
#
#     pl.rcParams['figure.figsize'] = 10, 4
#     pl.rcParams['legend.fontsize'] = 17
#     pl.rcParams['text.usetex'] = True
#     pl.rcParams['font.size'] = 20
#     pl.rcParams['font.serif'] = "Times"
#     pl.figure()
#     pl.plot(data_x, data_y, 'o', color='#d0d0d0', markersize=3)
#     pl.plot(pareto_front_x, pareto_front_y, 'o', markersize=4, label="Pareto Front")
#     pl.xlim(1e-4, 8e-4)
#     pl.ylim(0, 1e-3)
#     pl.grid(True)
#     pl.tight_layout()
#     pl.legend(loc="upper right")
#     pl.xlabel("$F_1$")
#     pl.ylabel("$F_2$")
#     pl.savefig(name + ".pdf", dpi=200)
# """
#
# if __name__ == '__main__':
#     unittest.main()
