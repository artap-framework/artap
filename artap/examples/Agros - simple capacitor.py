from artap.problem import Problem
from artap.results import Results
from artap.algorithm_bayesopt import BayesOptSerial
from artap.algorithm_nlopt import NLopt, LN_BOBYQA, LN_COBYLA
from artap.algorithm_genetic import NSGAII

from agrossuite import agros as a2d


class Capacitor(Problem):
    def set(self):
        self.name = "AgrosProblem"
        self.parameters = [{'name': 'r1', 'initial_value': 0.02, 'bounds': [0.01, 0.03]},
                      {'name': 'r2', 'initial_value': 0.04, 'bounds': [0.035, 0.1]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        # problem
        problem = a2d.problem(clear=True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"

        # project parameters
        problem.parameters["r1"] = individual.vector[0]
        problem.parameters["r2"] = individual.vector[1]
        problem.parameters["eps"] = 2.5

        # fields
        # electrostatic
        electrostatic = problem.field("electrostatic")
        electrostatic.analysis_type = "steadystate"
        electrostatic.matrix_solver = "umfpack"
        electrostatic.number_of_refinements = 1
        electrostatic.polynomial_order = 1
        electrostatic.adaptivity_type = "disabled"
        electrostatic.solver = "linear"

        # boundaries
        electrostatic.add_boundary("GND", "electrostatic_potential", {"electrostatic_potential": 0})
        electrostatic.add_boundary("V", "electrostatic_potential", {"electrostatic_potential": 1})
        electrostatic.add_boundary("neumann", "electrostatic_surface_charge_density",
                                   {"electrostatic_surface_charge_density": 0})

        # materials
        electrostatic.add_material("dielectric",
                                   {"electrostatic_permittivity": "eps", "electrostatic_charge_density": 0})

        # geometry
        geometry = problem.geometry()
        geometry.add_edge("r1", 0, "r2", 0, boundaries={"electrostatic": "neumann"})
        geometry.add_edge("r2", 0, 0, "r2", angle=90, boundaries={"electrostatic": "GND"})
        geometry.add_edge(0, "r2", 0, "r1", boundaries={"electrostatic": "neumann"})
        geometry.add_edge("r1", 0, 0, "r1", angle=90, boundaries={"electrostatic": "V"})

        geometry.add_label("(r1 + r2) / 2.", "(r2 - r1) / 2", materials={"electrostatic": "dielectric"})

        computation = problem.computation()
        computation.solve()

        solution = computation.solution("electrostatic")
        result = solution.volume_integrals()["We"]

        capacitance_req = 80.  # pF
        capacitance = 4.0 * 2.0 * result * 1e12  # pF
        print('Evaluated capacitance: {}, required capacitance: {}, difference: {}'.format(capacitance, capacitance_req, abs(capacitance - capacitance_req)))

        return [abs(capacitance - capacitance_req)]


def bobyqa():
    problem = Capacitor()
    algorithm = NLopt(problem)
    algorithm.options['n_iterations'] = 30
    algorithm.options['algorithm'] = LN_BOBYQA
    algorithm.options['verbose_level'] = 0
    algorithm.run()

    results = Results(problem)
    optimum = results.find_minimum('F')
    print(optimum)


def bayesopt():
    problem = Capacitor()
    algorithm = BayesOptSerial(problem)
    algorithm.options['n_iterations'] = 10
    algorithm.options['verbose_level'] = 0
    algorithm.run()

    results = Results(problem)
    optimum = results.find_minimum('F')
    print(optimum)


def nsga2():
    problem = Capacitor()
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 10
    algorithm.options['max_population_size'] = 10
    algorithm.run()

    results = Results(problem)
    optimum = results.find_minimum('F')
    print(optimum)

# nsga2()
bobyqa()
# bayesopt()