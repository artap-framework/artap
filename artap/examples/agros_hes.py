import math
import pylab as pl
import scipy.io
import numpy as np
import scipy as sc
from scipy.sparse import linalg as la
import scipy.sparse as sp
import pylab as pl
import random




from artap.problem import Problem
from artap.results import Results
from artap.algorithm_sweep import SweepAlgorithm
from artap.operators import LHCGeneration

from agrossuite import agros

from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor, ExtraTreesRegressor, BaggingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, DotProduct, WhiteKernel, ConstantKernel, RationalQuadratic, ExpSineSquared

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

class TestProblem(Problem):
    def __init__(self, name):
        parameters = {'Jext': {'initial_value': 6.5e7, 'bounds': [6.1e7, 6.8e7]}}
        costs = ['F']

        super().__init__(name, parameters, costs)

    def evaluate(self, x: list):
        Jext = x[0]
        time_total = 30

        # problem
        problem = agros.problem(clear=True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        problem.parameters["IR"] = 0.0075
        problem.parameters["IZ"] = 0.0039
        problem.parameters["Ih"] = 0.0035
        problem.parameters["Ihs"] = 0.003
        problem.parameters["Iw"] = 0.0045
        problem.parameters["Iwsd"] = 0.0018
        problem.parameters["Jext"] = Jext
        problem.parameters["RI"] = 1

        problem.frequency = 200e3
        problem.time_step_method = "fixed"
        problem.time_method_order = 2
        problem.time_total = time_total
        problem.time_steps = 40

        # agros.options.save_matrix_and_rhs = True
        agros.options.save_system = True

        # fields
        # heat
        heat = problem.field("heat")
        heat.analysis_type = "transient"
        heat.matrix_solver = "umfpack"
        heat.transient_initial_condition = 293.15
        heat.number_of_refinements = 1
        heat.polynomial_order = 1
        heat.adaptivity_type = "disabled"
        heat.solver = "linear"

        # boundaries
        heat.add_boundary("Neumann", "heat_heat_flux", {"heat_convection_external_temperature": 0, "heat_convection_heat_transfer_coefficient": 0, "heat_heat_flux": 0, "heat_radiation_ambient_temperature": 0, "heat_radiation_emissivity": 0})
        heat.add_boundary("Convection", "heat_heat_flux", {"heat_convection_external_temperature": 293.15, "heat_convection_heat_transfer_coefficient": 15, "heat_heat_flux": 0, "heat_radiation_ambient_temperature": 293.15, "heat_radiation_emissivity": 0})

        # materials
        heat.add_material("Aluminum", {"heat_conductivity": 167, "heat_density": 2689, "heat_specific_heat": 896, "heat_velocity_angular": 0, "heat_velocity_x": 0, "heat_velocity_y": 0, "heat_volume_heat": 0})
        heat.add_material("Solder", {"heat_conductivity": 57, "heat_density": 9290, "heat_specific_heat": 180, "heat_velocity_angular": 0, "heat_velocity_x": 0, "heat_velocity_y": 0, "heat_volume_heat": 0})

        # magnetic
        magnetic = problem.field("magnetic")
        magnetic.analysis_type = "harmonic"
        magnetic.matrix_solver = "umfpack"
        magnetic.transient_time_skip = 0
        magnetic.number_of_refinements = 1
        magnetic.polynomial_order = 2
        magnetic.adaptivity_type = "disabled"
        magnetic.solver = "linear"

        # boundaries
        magnetic.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_imag": 0, "magnetic_potential_real": 0})

        # materials
        magnetic.add_material("Coil +", {"magnetic_conductivity": 0, "magnetic_current_density_external_imag": 0, "magnetic_current_density_external_real": "Jext", "magnetic_permeability": 1, "magnetic_remanence": 0, "magnetic_remanence_angle": 0, "magnetic_total_current_imag": 0, "magnetic_total_current_prescribed": 0, "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0, "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
        magnetic.add_material("Coil -", {"magnetic_conductivity": 0, "magnetic_current_density_external_imag": 0, "magnetic_current_density_external_real": "-Jext", "magnetic_permeability": 1, "magnetic_remanence": 0, "magnetic_remanence_angle": 0, "magnetic_total_current_imag": 0, "magnetic_total_current_prescribed": 0, "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0, "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
        magnetic.add_material("Air", {"magnetic_conductivity": 0, "magnetic_current_density_external_imag": 0, "magnetic_current_density_external_real": 0, "magnetic_permeability": 1, "magnetic_remanence": 0, "magnetic_remanence_angle": 0, "magnetic_total_current_imag": 0, "magnetic_total_current_prescribed": 0, "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0, "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
        magnetic.add_material("Aluminum", {"magnetic_conductivity": 33e6, "magnetic_current_density_external_imag": 0, "magnetic_current_density_external_real": 0, "magnetic_permeability": 1, "magnetic_remanence": 0, "magnetic_remanence_angle": 0, "magnetic_total_current_imag": 0, "magnetic_total_current_prescribed": 0, "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0, "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})

        # geometry
        geometry = problem.geometry()
        geometry.add_edge(0.006, 0.012, 0.005, 0.012, boundaries={"heat": "Convection"})
        geometry.add_edge(0.005, 0.012, 0.005, 0.01)
        geometry.add_edge(0.006, 0.01, 0.005, 0.01)
        geometry.add_edge(0.006, 0.012, 0.006, 0.01, boundaries={"heat": "Convection"})
        geometry.add_edge(0.005, 0.002, 0.005, 0, boundaries={"heat": "Convection"})
        geometry.add_edge("IR+Iw", "IZ+Ihs+2*Ih", "IR", "IZ+Ihs+2*Ih")
        geometry.add_edge("IR", "IZ+Ihs+2*Ih", "IR", "IZ+Ihs+Ih")
        geometry.add_edge("IR", "IZ+Ihs+Ih", "IR+Iw", "IZ+Ihs+Ih")
        geometry.add_edge("IR+Iw", "IZ+Ihs+2*Ih", "IR+Iw", "IZ+Ihs+Ih")
        geometry.add_edge("IR+Iw+Iwsd", "IZ+Ih", "IR+Iw+Iwsd", "IZ")
        geometry.add_edge("IR+Iwsd", "IZ+Ih", "IR+Iw+Iwsd", "IZ+Ih")
        geometry.add_edge("IR+Iwsd", "IZ+Ih", "IR+Iwsd", "IZ")
        geometry.add_edge("IR+Iwsd", "IZ", "IR+Iw+Iwsd", "IZ")
        geometry.add_edge(0.03, 0.045, 0.03, -0.005, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0, 0, 0, -0.005, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0.005, 0, 0.01, 0, boundaries={"heat": "Convection"})
        geometry.add_edge(0.01, 0, 0.01, -0.005, boundaries={"heat": "Convection"})
        geometry.add_edge(0.01, -0.005, 0.03, -0.005, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0.005, 0.045, 0.03, 0.045, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0.005, 0.045, 0.005, 0.012, boundaries={"heat": "Convection"})
        geometry.add_edge(0, 0.045, 0.003, 0.045, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0.005, 0.045, 0.003, 0.045, boundaries={"heat": "Neumann", "magnetic": "A = 0"})
        geometry.add_edge(0, 0.045, 0, 0, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(0.003, 0, 0.003, 0.045, boundaries={"heat": "Neumann"})
        geometry.add_edge(0.003, 0, 0.003, -0.005, boundaries={"heat": "Neumann"})
        geometry.add_edge(0, -0.005, 0.003, -0.005, boundaries={"heat": "Neumann", "magnetic": "A = 0"})
        geometry.add_edge(0.003, -0.005, 0.01, -0.005, boundaries={"heat": "Neumann", "magnetic": "A = 0"})
        geometry.add_edge(0.00625, 0.00975, 0.006, 0.01, angle=90, segments=5, curvilinear=False, boundaries={"heat": "Convection"})
        geometry.add_edge(0.00625, 0.00975, 0.00625, 0.00925, boundaries={"heat": "Convection"})
        geometry.add_edge(0.005, 0.002, 0.00625, 0.00925, boundaries={"heat": "Convection"})

        geometry.add_label("IR+Iw/2", "IZ+Ih/2", refinements={"magnetic": 3}, materials={"heat": "none", "magnetic": "Coil -"})
        geometry.add_label("IR+Iw/2", "IZ+Ihs+1.5*Ih", materials={"heat": "none", "magnetic": "Coil +"})
        geometry.add_label(0.00248807, 0.0213882, materials={"heat": "none", "magnetic": "Air"})
        geometry.add_label(0.00553685, 0.0108868, area=1e-7, materials={"heat": "Solder", "magnetic": "Aluminum"})
        geometry.add_label(0.0213736, 0.0357852, materials={"heat": "none", "magnetic": "Air"})
        geometry.add_label(0.00428749, 0.030142, materials={"heat": "Aluminum", "magnetic": "Aluminum"})

        computation = problem.computation()
        computation.solve()

        solution = computation.solution("heat")

        # temperature in Kelvines
        Ti1 = []
        Ti2 = []
        Ti3 = []
        To1 = []

        for i in range(40):
            Ti1.append(solution.local_values(4.980e-3, 1.767e-2, time_step=i)["T"])
            Ti2.append(solution.local_values(9.977e-3, -2.233e-5, time_step=i)["T"])
            Ti3.append(solution.local_values(4.977e-3, 2.003e-3,  time_step=i)["T"])
            To1.append(solution.local_values(6.009e-3, 9.668e-3,  time_step=i)["T"])

        return [Ti1, Ti2, Ti3, To1]


def regressor_stats(regressor, x_test, y_test):
    # test
    print(regressor.__class__.__name__)
    for i in range(len(x_test)):
        x = x_test[i]
        y = y_test[i]
        val = regressor.predict([x])

        value_problem = y[0]
        value_surrogate = val[0]
        percent = 100.0 * math.fabs(value_problem - value_surrogate) / math.fabs(value_problem)

        print("params = [{0:8.3f}, {1:8.3f}, {2:8.3f}], \teval = {3:8.3f}, \tpred = {4:8.3f}, \tdiff = {5:8.3f} \t({6:8.3f} %)".format(x[0], x[1], x[2], value_problem, value_surrogate,
                                                                                            math.fabs(value_problem - value_surrogate), percent))


def lhc(j_ext):
    problem = TestProblem("AgrosProblem")
    [ti1, ti2, ti3, to] = problem.evaluate([j_ext])

    Ti = []
    To = []
    for i in range(len(to)):
        Ti.append([ti1[i], ti2[i], ti3[i]])
        To.append([to[i]])

    return Ti, To

# def lhc():
#     problem = TestProblem("AgrosProblem")
#
#     # sweep analysis (for training)
#     n = 1
#     gen = LHCGeneration(problem.parameters)
#     gen.init(n)
#     algorithm_sweep = SweepAlgorithm(problem, generator=gen)
#     algorithm_sweep.run()
#
#     Jext = []
#     Ti = []
#     To = []
#     for individual in problem.data_store.individuals:
#         Ti.append([individual.costs[0], individual.costs[1], individual.costs[2]])
#         To.append([individual.costs[3]])
#         Jext.append(individual.vector[0])
#
#     print(Ti)
#     print(To)
#     print(Jext)


def surrogate(Ti_train, To_train, Ti, To):
    x_train = Ti_train
    y_train = To_train
    x_test = Ti
    y_test = To

    param_grid = {
        "hidden_layer_sizes": [(int(len(x_train)/2)), (len(x_train))],
        "activation": ['logistic', 'relu']
    }
    # gp = MLPRegressor(solver='lbfgs')
    # grid_search = GridSearchCV(gp, param_grid=param_grid, n_jobs=-1, scoring=None)  #

    # regressor = grid_search
    # regressor = gp

    regressor = MLPRegressor(solver='lbfgs')
    # regressor = RandomForestRegressor(n_estimators=10)
    # regressor = GaussianProcessRegressor(kernel=1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-5, 1e5), nu=1.5), n_restarts_optimizer=9)
    # regressor = DecisionTreeRegressor()

    regressor.fit(x_train, y_train)
    # regressor_stats(regressor, x_test, y_test)

    return regressor


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


def matrix_model(u, i1, i2, i3, o):
    total_time = 30
    steps = len(u)

    dt = total_time / steps

    stiffness = scipy.io.loadmat('transient_solver-heat_matrix_stiffness.mat')['matrix_stiffness']
    mass = scipy.io.loadmat('transient_solver-heat_matrix_mass.mat')['matrix_mass']
    mass = mass / dt

    matrix_lhs = mass + stiffness

    rhs = scipy.io.loadmat('transient_solver-heat_rhs.mat')['rhs']


    slnt = np.zeros([len(rhs), steps])
    for i in range(1, steps):
        slnt[:, i] = la.spsolve(matrix_lhs, mass @ slnt[:, i - 1] + rhs[:, 0] * u[i])

    ti1 = slnt[i1, :]
    ti2 = slnt[i2, :]
    ti3 = slnt[i3, :]
    to = slnt[o, :]

    Ti = []
    To = []
    for i in range(steps):
        Ti.append([float(ti1[i])+293, float(ti2[i])+293, float(ti3[i])+293])
        To.append([float(to[i])+293])

    return Ti, To


total_time = 30
steps = 250
u = np.ones(steps)

other = scipy.io.loadmat('transient_solver-heat_other.mat')['other']
i1 = find_index(other, 4.980e-3, 1.767e-2)
i2 = find_index(other, 9.977e-3, -2.233e-5)
i3 = find_index(other, 4.977e-3, 2.003e-3)
o = find_index(other, 6.009e-3, 9.668e-3)

Ti_train, To_train = matrix_model(u, i1, i2, i3, o)
#Ti_train, To_train = lhc(6.1e7)

# Ti, To = lhc(5e7)
u = np.zeros(steps)
u[:60] = np.ones(60) * 1.7
u[60:90] = np.ones(30) * 1.1
u[90:] = np.ones(steps-90) * 0.1

Ti, To = matrix_model(u, i1, i2, i3, o)

regressor = surrogate(Ti_train, To_train, Ti, To)
Top = regressor.predict(Ti)

tm = pl.linspace(0, total_time, steps)
# pl.plot(Ti)

pl.plot(tm, To, label='exact solution')
pl.plot(tm, Top, label='prediction')
pl.legend()
pl.show()