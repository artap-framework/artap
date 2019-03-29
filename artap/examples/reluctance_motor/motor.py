from artap.executor import CondorJobExecutor
from artap.problem import Problem
from artap.datastore import SqliteDataStore
from artap.algorithm_genetic import NSGAII


class Motor(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        self.pev = 0.3
        parameters = {'gamma1': {'initial_value': 50, 'bounds': [47, 60]},
                      'sb1': {'initial_value': 2.5, 'bounds': [2 * self.pev, 3.5]},
                      'sb2': {'initial_value': 2.3, 'bounds': [2 * self.pev, 3.5]},
                      'sb3': {'initial_value': 2.1, 'bounds': [2 * self.pev, 3.5]},
                      'sb4': {'initial_value': 1.5, 'bounds': [2 * self.pev, 3.5]},
                      'pos': {'initial_value': 1.5, 'bounds': [self.pev, 2]},
                      'k2': {'initial_value': 1.5, 'bounds': [0, 1]},
                      'k3': {'initial_value': 1.5, 'bounds': [0, 1]},
                      'k4': {'initial_value': 1.5, 'bounds': [0, 1]},
                      }
        costs = ['F1', 'F2']

        super().__init__(name, parameters, costs, working_dir=".")

        self.executor = CondorJobExecutor(self,
                                          command="run.sh",
                                          model_file="OPT_AM_quarter.mph",
                                          output_file="out.txt",
                                          supplementary_files=["run.sh"])

    def evaluate_constraints(self, x):
        dh = 22
        d3 = 71.6
        vv = ((d3/2)-(dh/2) - self.pev)/4
        poc = (dh/2)+(vv/2)

        constraints = [0]*5
        constraints[0] = (poc - x[1] - dh/2 - self.pev) > 0
        constraints[1] = (vv - x[1] - x[2] - self.pev) > 0
        constraints[2] = (vv - x[2] - x[3] - self.pev) > 0
        constraints[3] = (vv - x[3] - x[4] - self.pev) > 0
        constraints[4] = (3 * vv + x[4] + poc - d3/2 + self.pev) < 0
        return constraints

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        parameters = content.split()
        result = [float(parameters[10]), float(parameters[11])]
        print(result)

        param_str = "parameters:"
        for parameter in parameters:
            param_str += str(parameter) +", "
        costs = "costs:"
        for number in result:
            costs += str(number) + ", "

        with open('results.txt', 'a') as file:
            file.write( param_str + "; " + costs + "\n")

        return [result]


if __name__ == '__main__':
    """ Tests one calculation of goal function."""
    problem = Motor("CondorComsolProblem")
    # set datastore
    database_name = "./data.sqlite"
    problem.data_store = SqliteDataStore(problem, database_name=database_name)

    algorithm = NSGAII(problem)
    algorithm.options['verbose_level'] = 0
    algorithm.options['max_population_number'] = 25
    algorithm.options['max_population_size'] = 50
    algorithm.options['max_processes'] = 8
    algorithm.run()


    # results = GraphicalResults(problem)
    # results.plot_populations()
