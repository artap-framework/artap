from unittest import TestCase, main
import getpass

from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem
from artap.enviroment import Enviroment


class ParameterEstimationProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):

        self.parameters = {'Cp_Al': {'initial_value': 900},
                           'k_Al': {'initial_value': 160},
                           'sigma_Al': {'initial_value': 3.774e7},
                           'rho_Al': {'initial_value': 2700}}
        self.costs = ['F1']

        self.max_population_number = 1
        self.max_population_size = 1

        self.time_out = 4 * 60  # time out 4 minutes per one set of parameters
        super().__init__(name, self.parameters, self.costs)

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
                                                working_dir="./", time_out=self.time_out)

    def eval(self, x):
        y = self.executor.eval(x)
        return y

    def eval_batch(self, table):
        y = self.executor.eval_batch(table)
        return y


if __name__ == '__main__':
    problem = ParameterEstimationProblem("Condor Comsol Problem")
    result = problem.eval_batch([[900, 160, 3.774e7, 2700]])
    print(result)
