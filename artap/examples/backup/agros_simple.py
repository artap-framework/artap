import math

from artap.problem import Problem
from artap.individual import Individual
from artap.results import Results
from artap.algorithm_nlopt import NLopt
from artap.algorithm_nlopt import LN_BOBYQA

from agrossuite import agros as a2d

class AgrosProblem(Problem):

    def set(self):
        self.name = "agros problem"
        self.working_dir = "team_22/"
        self.parameters = [{'name': 'R2', 'initial_value': 3.0, 'bounds': [2.6, 3.4]},
                           {'name': 'h2', 'initial_value': 1.0, 'bounds': [0.408, 2.2]},
                           {'name': 'd2', 'initial_value': 0.3, 'bounds': [0.1, 0.4]}]

        self.costs = [{'name': 'F', 'criteria': 'minimize', 'weight': 0}]

    def evaluate(self, individual: Individual):
        # problem
        x = individual.vector
        problem = a2d.problem(clear=True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        problem.parameters["J1"] = 2.25e+7
        problem.parameters["J2"] = -2.25e+7
        problem.parameters["R1"] = 2.0
        problem.parameters["R2"] = x[0]
        problem.parameters["d1"] = 0.27
        problem.parameters["d2"] = x[2]
        problem.parameters["h1"] = 1.6
        problem.parameters["h2"] = x[1]

        # fields
        # magnetic
        magnetic = problem.field("magnetic")
        magnetic.analysis_type = "steadystate"
        magnetic.matrix_solver = "umfpack"
        magnetic.number_of_refinements = 2
        magnetic.polynomial_order = 2
        magnetic.adaptivity_type = "disabled"
        magnetic.solver = "linear"

        # boundaries
        magnetic.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_real": 0})
        magnetic.add_boundary("Neumann", "magnetic_surface_current", {"magnetic_surface_current_real": 0})

        # materials
        magnetic.add_material("Coil 1", {"magnetic_conductivity": 0, "magnetic_current_density_external_real": "J1",
                                         "magnetic_permeability": 1, "magnetic_remanence": 0,
                                         "magnetic_remanence_angle": 0, "magnetic_total_current_prescribed": 0,
                                         "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0,
                                         "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
        magnetic.add_material("Coil 2", {"magnetic_conductivity": 0, "magnetic_current_density_external_real": "J2",
                                         "magnetic_permeability": 1, "magnetic_remanence": 0,
                                         "magnetic_remanence_angle": 0, "magnetic_total_current_prescribed": 0,
                                         "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0,
                                         "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})
        magnetic.add_material("Air", {"magnetic_conductivity": 0, "magnetic_current_density_external_real": 0,
                                      "magnetic_permeability": 1, "magnetic_remanence": 0,
                                      "magnetic_remanence_angle": 0, "magnetic_total_current_prescribed": 0,
                                      "magnetic_total_current_real": 0, "magnetic_velocity_angular": 0,
                                      "magnetic_velocity_x": 0, "magnetic_velocity_y": 0})

        # geometry
        geometry = problem.geometry()
        geometry.add_edge("R1-d1/2", 0, "R1+d1/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge("R1+d1/2", 0, "R1+d1/2", "h1/2")
        geometry.add_edge("R1+d1/2", "h1/2", "R1-d1/2", "h1/2")
        geometry.add_edge("R1-d1/2", "h1/2", "R1-d1/2", 0)
        geometry.add_edge("R2-d2/2", "h2/2", "R2+d2/2", "h2/2")
        geometry.add_edge("R2+d2/2", "h2/2", "R2+d2/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge("R2-d2/2", "h2/2", "R2-d2/2", 0)
        geometry.add_edge("R2-d2/2", 0, "R2+d2/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge(0, 0, "R1-d1/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge("R1+d1/2", 0, "R2-d2/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge(0, 25, 0, 0, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(25, 0, "R2+d2/2", 0, boundaries={"magnetic": "Neumann"})
        geometry.add_edge(0, 25, 25, 25, boundaries={"magnetic": "A = 0"})
        geometry.add_edge(25, 25, 25, 0, boundaries={"magnetic": "A = 0"})

        geometry.add_label(12, 12, materials={"magnetic": "Air"})
        geometry.add_label("R1", "h1/4", materials={"magnetic": "Coil 1"})
        geometry.add_label("R2", "h2/4", materials={"magnetic": "Coil 2"})

        # recipes
        magnetic.add_recipe_volume_integral("Wm", "magnetic_energy", [], -1, -1)
        magnetic.add_recipe_local_value("B00", "magnetic_flux_density_real", "magnitude", 0, 10, -1, -1)
        magnetic.add_recipe_local_value("B01", "magnetic_flux_density_real", "magnitude", 1, 10, -1, -1)
        magnetic.add_recipe_local_value("B02", "magnetic_flux_density_real", "magnitude", 2, 10, -1, -1)
        magnetic.add_recipe_local_value("B03", "magnetic_flux_density_real", "magnitude", 3, 10, -1, -1)
        magnetic.add_recipe_local_value("B04", "magnetic_flux_density_real", "magnitude", 4, 10, -1, -1)
        magnetic.add_recipe_local_value("B05", "magnetic_flux_density_real", "magnitude", 5, 10, -1, -1)
        magnetic.add_recipe_local_value("B06", "magnetic_flux_density_real", "magnitude", 6, 10, -1, -1)
        magnetic.add_recipe_local_value("B07", "magnetic_flux_density_real", "magnitude", 7, 10, -1, -1)
        magnetic.add_recipe_local_value("B08", "magnetic_flux_density_real", "magnitude", 8, 10, -1, -1)
        magnetic.add_recipe_local_value("B09", "magnetic_flux_density_real", "magnitude", 9, 10, -1, -1)
        magnetic.add_recipe_local_value("B10", "magnetic_flux_density_real", "magnitude", 10, 10, -1, -1)
        magnetic.add_recipe_local_value("B11", "magnetic_flux_density_real", "magnitude", 10, 10, -1, -1)
        magnetic.add_recipe_local_value("B12", "magnetic_flux_density_real", "magnitude", 10, 9, -1, -1)
        magnetic.add_recipe_local_value("B13", "magnetic_flux_density_real", "magnitude", 10, 8, -1, -1)
        magnetic.add_recipe_local_value("B14", "magnetic_flux_density_real", "magnitude", 10, 7, -1, -1)
        magnetic.add_recipe_local_value("B15", "magnetic_flux_density_real", "magnitude", 10, 6, -1, -1)
        magnetic.add_recipe_local_value("B16", "magnetic_flux_density_real", "magnitude", 10, 5, -1, -1)
        magnetic.add_recipe_local_value("B17", "magnetic_flux_density_real", "magnitude", 10, 4, -1, -1)
        magnetic.add_recipe_local_value("B18", "magnetic_flux_density_real", "magnitude", 10, 3, -1, -1)
        magnetic.add_recipe_local_value("B19", "magnetic_flux_density_real", "magnitude", 10, 2, -1, -1)
        magnetic.add_recipe_local_value("B20", "magnetic_flux_density_real", "magnitude", 10, 1, -1, -1)
        magnetic.add_recipe_local_value("B21", "magnetic_flux_density_real", "magnitude", 10, 0, -1, -1)

        computation = problem.computation()
        computation.solve()

        solution = computation.solution("magnetic")

        B00 = solution.local_values( 0, 10)["Br"]
        B01 = solution.local_values( 1, 10)["Br"]
        B02 = solution.local_values( 2, 10)["Br"]
        B03 = solution.local_values( 3, 10)["Br"]
        B04 = solution.local_values( 4, 10)["Br"]
        B05 = solution.local_values( 5, 10)["Br"]
        B06 = solution.local_values( 6, 10)["Br"]
        B07 = solution.local_values( 7, 10)["Br"]
        B08 = solution.local_values( 8, 10)["Br"]
        B09 = solution.local_values( 9, 10)["Br"]
        B10 = solution.local_values(10, 10)["Br"]
        B11 = solution.local_values(10, 10)["Br"]
        B12 = solution.local_values(10,  9)["Br"]
        B13 = solution.local_values(10,  8)["Br"]
        B14 = solution.local_values(10,  7)["Br"]
        B15 = solution.local_values(10,  6)["Br"]
        B16 = solution.local_values(10,  5)["Br"]
        B17 = solution.local_values(10,  4)["Br"]
        B18 = solution.local_values(10,  3)["Br"]
        B19 = solution.local_values(10,  2)["Br"]
        B20 = solution.local_values(10,  1)["Br"]
        B21 = solution.local_values(10,  0)["Br"]

        Wm = solution.volume_integrals()["Wm"]

        of = (B00**2 + B01**2 + B02**2 + B03**2 + B04**2 + B05**2 + B06**2 + B07**2 + B08**2 + B09**2 + B10**2 + B11**2 + B12**2 + B13**2 + B14**2 + B15**2 + B16**2 + B17**2 + B18**2 + B19**2 + B20**2 + B21**2)/22/9e-6 + math.fabs(2*Wm - 180e6) / 180e6

        return [of]


def bobyqa():
    problem = AgrosProblem()
    algorithm = NLopt(problem)
    algorithm.options['n_iterations'] = 10
    algorithm.options['algorithm'] = LN_BOBYQA
    algorithm.options['verbose_level'] = 0
    algorithm.run()

    results = Results(problem)
    optimum = results.find_minimum('F')
    print(optimum)


bobyqa()
