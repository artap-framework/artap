import getpass
import numpy as np

from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem
from artap.enviroment import Enviroment
from artap.population import Population_NSGA_II
from artap.algorithm_genetic import NSGA_II


class ParameterEstimationProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):

        cp_d = 900
        k_d = 160
        sigma_d = 3.774e7
        rho_d = 2700

        self.parameters = {'Cp_Al': {'initial_value': cp_d, 'bounds': [cp_d*0.9, cp_d*1.1], 'precision': 1e-1},
                           'k_Al': {'initial_value': k_d, 'bounds': [k_d * 0.9, k_d * 1.1], 'precision': 1e-1},
                           'sigma_Al': {'initial_value': sigma_d, 'bounds': [sigma_d * 0.9, sigma_d * 1.1],
                                        'precision': 1e-1},
                           'rho_Al': {'initial_value': rho_d, 'bounds': [rho_d * 0.9, rho_d * 1.1], 'precision': 1e-1},
                           'Cp_inlet': {'initial_value': cp_d, 'bounds': [cp_d*0.9, cp_d*1.1], 'precision': 1e-1},
                           'k_inlet': {'initial_value': k_d, 'bounds': [k_d * 0.9, k_d * 1.1], 'precision': 1e-1},
                           'sigma_inlet': {'initial_value': sigma_d, 'bounds': [sigma_d * 0.9, sigma_d * 1.1],
                                           'precision': 1e-1},
                           'rho_inlet': {'initial_value': rho_d, 'bounds': [rho_d * 0.9, rho_d * 1.1],
                                         'precision': 1e-1},
                           'Cp_outlet': {'initial_value': cp_d, 'bounds': [cp_d*0.9, cp_d*1.1], 'precision': 1e-1},
                           'k_outlet': {'initial_value': k_d, 'bounds': [k_d * 0.9, k_d * 1.1], 'precision': 1e-1},
                           'sigma_outlet': {'initial_value': sigma_d, 'bounds': [sigma_d * 0.9, sigma_d * 1.1],
                                            'precision': 1e-1},
                           'rho_outlet': {'initial_value': rho_d, 'bounds': [rho_d * 0.9, rho_d * 1.1],
                                          'precision': 1e-1},
                           'Cp_outlet_sleeve': {'initial_value': cp_d, 'bounds': [cp_d*0.9, cp_d*1.1],
                                                'precision': 1e-1},
                           'k_outlet_sleeve': {'initial_value': k_d, 'bounds': [k_d * 0.9, k_d * 1.1],
                                               'precision': 1e-1},
                           'sigma_outlet_sleeve': {'initial_value': sigma_d, 'bounds': [sigma_d * 0.9, sigma_d * 1.1],
                                                   'precision': 1e-1},
                           'rho_outlet_sleeve': {'initial_value': rho_d, 'bounds': [rho_d * 0.9, rho_d * 1.1],
                                                 'precision': 1e-1},
                           'Cp_inlet_sleeve': {'initial_value': cp_d, 'bounds': [cp_d*0.9, cp_d*1.1],
                                               'precision': 1e-1},
                           'k_inlet_sleeve': {'initial_value': k_d, 'bounds': [k_d * 0.9, k_d * 1.1],
                                              'precision': 1e-1},
                           'sigma_inlet_sleeve': {'initial_value': sigma_d, 'bounds': [sigma_d * 0.9, sigma_d * 1.1],
                                                  'precision': 1e-1},
                           'rho_inlet_sleeve': {'initial_value': rho_d, 'bounds': [rho_d * 0.9, rho_d * 1.1],
                                                'precision': 1e-1}}

        self.costs = ['F1', 'F2']

        self.max_population_number = 1
        self.max_population_size = 1

        self.time_out = 4 * 60  # time out 4 minutes per one set of parameters
        super().__init__(name, self.parameters, self.costs, working_dir="./")

        output_files = ["max.txt", "inlet.txt", "outlet.txt", "inlet_tube.txt", "outlet_tube.txt", "inlet_sleeve.txt",
                        "outlet_sleeve.txt"]
        model_file = "brazing.mph"

        # current username
        if Enviroment.condor_host_login == "":
            user = getpass.getuser()
        else:
            user = Enviroment.condor_host_login
        # host        

        host = Enviroment.condor_host_ip

        self.executor = CondorComsolJobExecutor(self.parameters, model_file, output_files,
                                                username=user, hostname=host,
                                                working_dir="./", time_out=self.time_out)
        self.executor.parse_results = self.parse_results

    def eval(self, x):
        y = self.executor.eval(x)
        return y

    def parse_results(self, content, x):
        ref_temp = [600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    600, 600, 600, 600,
                    ]

        ref_param = [900.0, 160, 37740000.0, 2700, 900, 160, 37740000.0, 2700, 900, 160, 37740000.0, 2700, 900,
                     160, 37740000.0, 2700, 900, 160, 37740000.0, 2700]

        lines = content.split("\n")
        line_with_results = lines[10]  # 10th line contains results
        results = line_with_results.split(" ")

        f_1 = 0
        for i in range(len(results)):
            f_1 += (results[i] - ref_temp[i])**2

        f_2 = 0
        for i in range(len(x)):
            f_2 += ((x[i] - ref_param[i])/ref_param[i])**2

        return [np.sqrt(f_1), np.sqrt(f_2)]


if __name__ == '__main__':
    problem = ParameterEstimationProblem("Condor Comsol Problem")
    population = Population_NSGA_II(problem)
    # population.gen_random_population(100, len(problem.parameters), problem.parameters)
    population.gen_uniform_population(10)
    population.evaluate()

    problem = ParameterEstimationProblem("LocalPythonProblemNSGA_II")
    algorithm = NSGA_II(problem)
    algorithm.run()

