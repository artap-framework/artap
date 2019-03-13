import math

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
        Ti1 = solution.local_values(4.980e-3, 1.767e-2)["T"]
        Ti2 = solution.local_values(9.977e-3, -2.233e-5)["T"]
        Ti3 = solution.local_values(4.977e-3, 2.003e-3)["T"]
        To1 = solution.local_values(6.009e-3, 9.668e-3)["T"]

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


def lhc():
    problem = TestProblem("AgrosProblem")

    # sweep analysis (for training)
    n = 50
    gen = LHCGeneration(problem.parameters)
    gen.init(n)
    algorithm_sweep = SweepAlgorithm(problem, generator=gen)
    algorithm_sweep.run()

    Jext = []
    Ti = []
    To = []
    for individual in problem.data_store.individuals:
        Ti.append([individual.costs[0], individual.costs[1], individual.costs[2]])
        To.append([individual.costs[3]])
        Jext.append(individual.vector[0])

    print(Ti)
    print(To)
    print(Jext)


def surrogate():
    x_data = [[776.0100747742531, 837.5993208254577, 825.2519915234318], [827.5937508361477, 895.7625421493797, 882.0961544529697], [839.8134469116156, 909.5408716832276, 895.5620112451402], [852.5168607097335, 923.8646175795648, 909.5609151393703], [795.807201542774, 859.9215892972356, 847.0680229791197], [774.3420436234893, 835.7185307693109, 823.4138550867892], [761.7279609731238, 821.4955102906774, 809.5133923023287], [759.0411713473952, 818.4660181803404, 806.5526047256783], [841.015883556784, 910.8966802269373, 896.8870719966875], [779.999470008028, 842.0975670856233, 829.6482240134816], [845.3512748740532, 915.785054688863, 901.6645851407089], [791.5377748783183, 855.1075933402145, 842.3632015422332], [790.504150850787, 853.9421296185759, 841.2241688653397], [867.9723805866071, 941.2915032128535, 926.5925840143798], [863.8962104943841, 936.695413881363, 922.1007273934509], [772.0255723085006, 833.1065914103875, 820.8611507643478], [811.2956301476783, 877.3855811970623, 864.1359566037821], [807.8038706241978, 873.4484445391103, 860.2881085553842], [856.8674142350288, 928.7700882030572, 914.3551367285538], [866.0516707601352, 939.1258050838122, 924.476000811087], [802.4189626314053, 867.3766865857262, 854.3540493593027], [757.599792723974, 816.8407903895671, 804.9642347689775], [784.7493400121504, 847.4532873716051, 834.882484248922], [805.9071347033897, 871.3097782094189, 858.1979441090286], [801.493458808291, 866.3331338998963, 853.3341629508686], [849.6687250845125, 920.6531996393081, 906.4223275495515], [809.1260025909382, 874.939215652611, 861.7450711193059], [823.7533098273697, 891.4322493624296, 877.8640664923812], [769.8115347189258, 830.6101512926339, 818.4213263260322], [833.1866366544834, 902.0688056909852, 888.25940098705], [822.1609541663482, 889.6367872742512, 876.1093229078485], [763.8517345308545, 823.8901731164312, 811.8537476115762], [861.159491971077, 933.6096243966664, 919.0849191861105], [818.0941559504971, 885.0512652105543, 871.6277939042415], [826.1680398029603, 894.1549803643828, 880.5250498623739], [788.8868544229128, 852.1185455458119, 839.4419410624714], [857.766406009144, 929.7837472036847, 915.3458073976677], [794.7323081892775, 858.70959230921, 845.8835123435381], [784.0030433451245, 846.611799879201, 834.0600804852996], [837.2862043327559, 906.6912769921524, 892.7770412724236], [766.2054098036069, 826.5440618320897, 814.447449939544], [798.6937419666206, 863.1763106034622, 850.2489318767116], [817.6527197551105, 884.5535234229887, 871.1413401861485], [813.8119951537019, 880.2229108708975, 866.9089397122441], [781.4722879915457, 843.7582443557419, 831.2712395062141], [834.0010309868424, 902.9870767684837, 889.156846994242], [846.4846133545644, 917.0629515335381, 902.9135011187554], [768.3675852615964, 828.9820247557313, 816.8301233625995], [830.1690233010205, 898.6662929825641, 884.9340523841943], [850.4068333598294, 921.485454303099, 907.2357078718732]]
    y_data = [[819.1322440213304], [875.3226376930376], [888.6336225907687], [902.4715239732449], [840.6973675568644], [817.3152481386617], [803.5746556868746], [800.6479203646021], [889.9434437127896], [823.477915090412], [894.6660102965424], [836.046656647084], [834.9207240759787], [919.307310264248], [914.8671148450582], [814.7919026725081], [857.5690015137177], [853.7654078730773], [907.2106068370157], [917.2150700534258], [847.8995967657429], [799.0778183776522], [828.6519756808087], [851.6992825749609], [846.8914401523468], [899.3690335299528], [855.2056137941712], [871.1392233140832], [812.38013884992], [881.4150002364793], [869.4046611756557], [805.8880943827887], [911.8859916887827], [864.9746745950462], [873.769602501805], [833.1589938174141], [908.189883723657], [839.5264800727012], [827.8390304485689], [885.880682780106], [808.4519663331461], [843.8416925671836], [864.4938156200047], [860.3100923220145], [825.08226415233], [882.3021246454643], [895.9005623921894], [810.8072364388657], [878.1278967335079], [900.1730591002264]]
    Jz = [62272674.863322966, 65514566.82025235, 66259307.08561908, 67024755.56955151, 63536432.599254474, 62165021.91285617, 61344806.552677915, 61168680.53896497, 66332138.78460527, 62529394.46039568, 66594072.51090893, 63266027.03459662, 63200388.15907377, 67944406.0711816, 67703074.4052169, 62015209.35927996, 64507883.37210025, 64290158.115267694, 67284897.90326867, 67830796.4679012, 63952934.44625695, 61073985.11133313, 62833683.15905225, 64171579.377889805, 63894796.60033953, 66853902.392015204, 64372684.991411224, 65278752.98609571, 61871682.43529808, 65856475.441679426, 65180727.68720712, 61483668.385775305, 67540561.80571558, 64929704.26268192, 65427123.36452834, 63097546.96241009, 67338528.03007591, 63468462.38136747, 62785971.155681536, 66105970.21331556, 61637196.75277991, 63718602.41263401, 64902398.16782406, 64664334.344020054, 62623905.060110934, 65906113.68080527, 66662376.35457389, 61777897.49832106, 65672221.48626305, 66898221.71637714]

    n = 10
    x_train = x_data[:len(x_data) - n]
    y_train = y_data[:len(y_data) - n]
    x_test = x_data[-n:]
    y_test = y_data[-n:]

    param_grid = {
        "hidden_layer_sizes": [(int(len(x_train)/2)), (len(x_train))],
        "activation": ['logistic', 'relu']
    }
    gp = MLPRegressor(solver='lbfgs')
    grid_search = GridSearchCV(gp, param_grid=param_grid, n_jobs=-1, scoring=None)  #
    regressor = grid_search

    regressor.fit(x_train, y_train)

    regressor_stats(regressor, x_test, y_test)


# lhc()
surrogate()
