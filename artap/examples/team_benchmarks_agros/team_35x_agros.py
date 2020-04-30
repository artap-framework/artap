import math
from artap.problem import Problem
from artap.individual import Individual
from artap.algorithm_genetic import NSGAII
from artap.results import Results

try:
    from agrossuite import agros as a2d

    from artap.examples.team_benchmarks_agros.team_35x_semi_analytical import ProblemAnalytical

    class AgrosSimple(Problem):

        def set(self):

            self.name = "Agros-solution"

            self.parameters = [{'name': 'x1', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x2', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x3', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x4', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x5', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x6', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x7', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x8', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x9', 'bounds': [5.01e-3, 50e-3]},
                               {'name': 'x10', 'bounds': [5.01e-3, 50e-3]}]

            self.costs = [{'name': 'F1', 'criteria': 'minimize'},
                          {'name': 'F2', 'criteria': 'minimize'}]

        def evaluate(self, x):
            x = x.vector

            # problem
            problem = a2d.problem(clear=True)
            problem.coordinate_type = "axisymmetric"
            problem.mesh_type = "triangle"

            problem.parameters["MH"] = 0.04
            problem.parameters["MW"] = 0.1
            problem.parameters["h"] = 0.00145
            problem.parameters["r1"] = x[0]
            problem.parameters["r10"] = x[9]
            problem.parameters["r2"] = x[1]
            problem.parameters["r3"] = x[2]
            problem.parameters["r4"] = x[3]
            problem.parameters["r5"] = x[4]
            problem.parameters["r6"] = x[5]
            problem.parameters["r7"] = x[6]
            problem.parameters["r8"] = x[7]
            problem.parameters["r9"] = x[8]
            problem.parameters["w"] = 0.001

            # fields
            # magnetic
            magnetic = problem.field("magnetic")
            magnetic.analysis_type = "steadystate"
            magnetic.matrix_solver = "umfpack"
            magnetic.number_of_refinements = 1
            magnetic.polynomial_order = 2
            magnetic.adaptivity_type = "disabled"
            magnetic.solver = "linear"

            # boundaries
            magnetic.add_boundary("A=0", "magnetic_potential", {"magnetic_potential_real": 0})
            magnetic.add_boundary("Symmetry", "magnetic_surface_current", {"magnetic_surface_current_real": 0})

            # materials
            magnetic.add_material("air", {"magnetic_conductivity": 0, "magnetic_current_density_external_real": 0,
                                          "magnetic_permeability": 1, "magnetic_remanence": 0,
                                          "magnetic_remanence_angle": 0, "magnetic_total_current_prescribed": 0,
                                          "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0,
                                          "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
            magnetic.add_material("uniform_field", {"magnetic_conductivity": 0, "magnetic_current_density_external_real": 0,
                                                    "magnetic_permeability": 1, "magnetic_remanence": 0,
                                                    "magnetic_remanence_angle": 0, "magnetic_total_current_prescribed": 0,
                                                    "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0,
                                                    "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
            magnetic.add_material("turn",
                                  {"magnetic_conductivity": "58*1e6", "magnetic_current_density_external_real": "2*1e6",
                                   "magnetic_permeability": 1, "magnetic_remanence": 0, "magnetic_remanence_angle": 0,
                                   "magnetic_total_current_prescribed": 0, "magnetic_total_current_real": 0,
                                   "magnetic_velocity_angular": 0, "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})

            # geometry
            geometry = problem.geometry()
            geometry.add_edge(0, 0, 0.005, 0, boundaries={"magnetic": "Symmetry"})
            geometry.add_edge(0.005, 0, 0.005, 0.005)
            geometry.add_edge(0.005, 0.005, 0, 0.005)
            geometry.add_edge(0, 0.005, 0, 0, boundaries={"magnetic": "A=0"})
            geometry.add_edge("r1", 0, "r1+w", 0, boundaries={"magnetic": "Symmetry"})
            geometry.add_edge("r1+w", 0, "r1+w", "h")
            geometry.add_edge("r1+w", "h", "r1", "h")
            geometry.add_edge("r1", "h", "r1", 0)
            geometry.add_edge(0.005, 0, "r1", 0, boundaries={"magnetic": "Symmetry"})
            geometry.add_edge("r2", "2*h", "r2+w", "2*h")
            geometry.add_edge("r2+w", "2*h", "r2+w", "h+1e-5")
            geometry.add_edge("r2+w", "h+1e-5", "r2", "h+1e-5")
            geometry.add_edge("r2", "h+1e-5", "r2", "2*h")
            geometry.add_edge("r3", "2*h+1e-5", "r3+w", "2*h+1e-5")
            geometry.add_edge("r3+w", "2*h+1e-5", "r3+w", "3*h")
            geometry.add_edge("r3+w", "3*h", "r3", "3*h")
            geometry.add_edge("r3", "3*h", "r3", "2*h+1e-5")
            geometry.add_edge("r4", "3*h+2e-5", "r4+w", "3*h+2e-5")
            geometry.add_edge("r4+w", "3*h+2e-5", "r4+w", "4*h")
            geometry.add_edge("r4+w", "4*h", "r4", "4*h")
            geometry.add_edge("r4", "4*h", "r4", "3*h+2e-5")
            geometry.add_edge("r5", "4*h+2e-5", "r5+w", "4*h+2e-5")
            geometry.add_edge("r5", "4*h+2e-5", "r5", "5*h")
            geometry.add_edge("r5", "5*h", "r5+w", "5*h")
            geometry.add_edge("r5+w", "5*h", "r5+w", "4*h+2e-5")
            geometry.add_edge("r6", "5*h+2e-5", "r6+w", "5*h+2e-5")
            geometry.add_edge("r6+w", "5*h+2e-5", "r6+w", "6*h")
            geometry.add_edge("r6+w", "6*h", "r6", "6*h")
            geometry.add_edge("r6", "6*h", "r6", "5*h+2e-5")
            geometry.add_edge("r7", "6*h+2e-5", "r7+w", "6*h+2e-5")
            geometry.add_edge("r7+w", "6*h+2e-5", "r7+w", "7*h")
            geometry.add_edge("r7+w", "7*h", "r7", "7*h")
            geometry.add_edge("r7", "7*h", "r7", "6*h+2e-5")
            geometry.add_edge("r8", "7*h+2e-5", "r8+w", "7*h+2e-5")
            geometry.add_edge("r8+w", "7*h+2e-5", "r8+w", "8*h")
            geometry.add_edge("r8+w", "8*h", "r8", "8*h")
            geometry.add_edge("r8", "8*h", "r8", "7*h+2e-5")
            geometry.add_edge("r9", "8*h+2e-5", "r9+w", "8*h+2e-5")
            geometry.add_edge("r9+w", "8*h+2e-5", "r9+w", "9*h")
            geometry.add_edge("r9+w", "9*h", "r9", "9*h")
            geometry.add_edge("r9", "9*h", "r9", "8*h+2e-5")
            geometry.add_edge("r10", "9*h+2e-5", "r10+w", "9*h+2e-5")
            geometry.add_edge("r10+w", "9*h+2e-5", "r10+w", "10*h")
            geometry.add_edge("r10+w", "10*h", "r10", "10*h")
            geometry.add_edge("r10", "10*h", "r10", "9*h+2e-5")
            geometry.add_edge("r1+w", 0, "MW", 0, boundaries={"magnetic": "Symmetry"})
            geometry.add_edge("MW", 0, "MW", "MH", boundaries={"magnetic": "A=0"})
            geometry.add_edge("MW", "MH", 0, "MH", boundaries={"magnetic": "A=0"})
            geometry.add_edge(0, "MH", 0, 0.005, boundaries={"magnetic": "A=0"})

            geometry.add_label("0.8*MW", "0.8*MH", materials={"magnetic": "air"})
            geometry.add_label("r1+w/2", "0.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r2+w/2", "1.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r3+0.5*w", "2.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r4+0.5*w", "3.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r5+0.5*w", "4.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r6+w/2", "5.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r7+w/2", "6.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r8+w/2", "7.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r9+w/2", "8.5*h", materials={"magnetic": "turn"})
            geometry.add_label("r10+w/2", "9.5*h", materials={"magnetic": "turn"})
            geometry.add_label(0.0025, 0.0025, materials={"magnetic": "uniform_field"})

            # recipes
            magnetic.add_recipe_volume_integral("Wm", "magnetic_energy", [11], -1, -1)

            computation = problem.computation()
            computation.solve()

            solution = computation.solution("magnetic")

            B0 = 2e-3

            dxy = 0.5e-3
            nx = 8
            ny = 8
            dx = (5e-3 - dxy) / (nx - 1)
            dy = (5e-3 - dxy) / (ny - 1)

            f1 = 0.0
            f2 = 0.0
            f3 = 0.0
            for i in range(0, nx):
                xx = dxy + i * dx
                if xx > 0.005:
                    xx = 0.005
                for j in range(0, ny):
                    yy = dxy + j * dy
                    if yy > 0.005:
                        yy = 0.005

                    point = solution.local_values(xx, yy)
                    Br = point["Brr"]
                    Bz = point["Brz"]

                    Bp1s = math.sqrt((Br - 0.0) ** 2 + (Bz - B0) ** 2)
                    f1 = max(f1, Bp1s)

                    # Bp2 = math.sqrt((Brp - Br) ** 2 + (Bzp - Bz) ** 2) + math.sqrt((Brm - Br) ** 2 + (Bzm - Bz) ** 2)
                    # f3 = max(f2, Bp2)

            f2 = sum(x) * 1e3

            return [f1, f2]
            # return [f1, f2, f3]


    def check_analytical_agros():
        vec = [0.00808, 0.0149, 0.00674, 0.0167, 0.00545, 0.0106, 0.0117, 0.0111, 0.01369, 0.00619]
        vec = [5.1e-3] * 10
        vec = [0.016932781137, 0.020220367784, 0.040397700883, 0.039838420509, 0.028051772403, 0.02469698998,
               0.024829362232, 0.014442787471, 0.024972441459, 0.037526654441]
        vec = [0.020798867779511312, 0.006138154021970008, 0.010012220217557183, 0.00690835649565163, 0.012212694015280686,
               0.00809716361914133, 0.018352792299856494, 0.00878331012406535, 0.02486595541682808, 0.00983825681954835]
        vec = [0.01020404406824542, 0.007528926158292741, 0.008708935266330736, 0.007283700503797654, 0.005215395421823215,
               0.01894915013137104, 0.020218991198109815, 0.005188444416722139, 0.015520989779088109, 0.0160617361729709]
        # vec = Individual([10e-3] * 10)
        ind = Individual(vec)

        problem_analytical = ProblemAnalytical()
        a = problem_analytical.evaluate(ind)
        problem_agros = AgrosSimple()
        n = problem_agros.evaluate(ind)

        print("anal ", a)
        print("agros", n)
        print("diff", math.fabs(a[0] - n[0]))


    def optim_single():
        problem = AgrosSimple()
        # optimization
        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        b = Results(problem)
        b.pareto_plot()


    # check_analytical_agros()
    optim_single()

except ImportError:
    print("Agros is not present test skipped")