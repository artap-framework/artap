import getpass
import os

from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem
from artap.enviroment import Enviroment
from artap.population import Population_NSGA_II


class ParameterEstimationProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):

        self.parameters = {'Cp_Al': {'initial_value': 900, 'bounds': [850, 950], 'precision': 1e-1},
                           'k_Al': {'initial_value': 160, 'bounds': [50, 300], 'precision': 1e-1},
                           'sigma_Al': {'initial_value': 3.774e7, 'bounds': [3.0e7, 4.5e7], 'precision': 1e-1},
                           'rho_Al': {'initial_value': 2700, 'bounds': [2000, 3500], 'precision': 1e-1},
                           'Cp_inlet': {'initial_value': 900, 'bounds': [850, 950], 'precision': 1e-1},
                           'k_inlet': {'initial_value': 160, 'bounds': [50, 300], 'precision': 1e-1},
                           'sigma_inlet': {'initial_value': 3.774e7, 'bounds': [3.0e7, 4.5e7], 'precision': 1e-1},
                           'rho_inlet': {'initial_value': 2700, 'bounds': [2000, 3500], 'precision': 1e-1},
                           'Cp_outlet': {'initial_value': 900, 'bounds': [850, 950], 'precision': 1e-1},
                           'k_outlet': {'initial_value': 160, 'bounds': [50, 300], 'precision': 1e-1},
                           'sigma_outlet': {'initial_value': 3.774e7, 'bounds': [3.0e7, 4.5e7], 'precision': 1e-1},
                           'rho_outlet': {'initial_value': 2700, 'bounds': [2000, 3500], 'precision': 1e-1},
                           'Cp_outlet_sleeve': {'initial_value': 900, 'bounds': [850, 950], 'precision': 1e-1},
                           'k_outlet_sleeve': {'initial_value': 160, 'bounds': [50, 300], 'precision': 1e-1},
                           'sigma_outlet_sleeve': {'initial_value': 3.774e7, 'bounds': [3.0e7, 4.5e7], 'precision': 1e-1},
                           'rho_outlet_sleeve': {'initial_value': 2700, 'bounds': [2000, 3500], 'precision': 1e-1},
                           'Cp_inlet_sleeve': {'initial_value': 900, 'bounds': [850, 950], 'precision': 1e-1},
                           'k_inlet_sleeve': {'initial_value': 160, 'bounds': [50, 300], 'precision': 1e-1},
                           'sigma_inlet_sleeve': {'initial_value': 3.774e7, 'bounds': [3.0e7, 4.5e7], 'precision': 1e-1},
                           'rho_inlet_sleeve': {'initial_value': 2700, 'bounds': [2000, 3500], 'precision': 1e-1}}

        self.costs = ['F1']

        self.max_population_number = 1
        self.max_population_size = 1

        self.time_out = 4 * 60  # time out 4 minutes per one set of parameters
        super().__init__(name, self.parameters, self.costs, working_dir="." + os.sep)

        output_file = "max.txt"
        model_file = "brazing.mph"

        # current username
        if Enviroment.condor_host_login == "":
            user = getpass.getuser()
        else:
            user = Enviroment.condor_host_login
        # host        

        host = Enviroment.condor_host_ip

        self.executor = CondorComsolJobExecutor(self.parameters, model_file, output_file,
                                                username=user, hostname=host,
                                                working_dir="." + os.sep, time_out=self.time_out)
        self.executor.parse_results = self.parse_results

    def eval(self, x):
        y = self.executor.eval(x)
        return y

    def parse_results(self, content):
        lines = content.split("\n")
        line_with_results = lines[10]  # 10th line contains results
        result = float(line_with_results.split(" ")[-1])
        return result


if __name__ == '__main__':
    problem = ParameterEstimationProblem("Condor Comsol Problem")
    population = Population_NSGA_II(problem)
    population.gen_random_population(50, len(problem.parameters),
                                     problem.parameters)
    population.evaluate()

