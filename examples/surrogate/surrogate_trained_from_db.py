from artap.problem import Problem
from artap.results import Results
from artap.surrogate_smt import SurrogateModelSMT
from artap.operators import LHSGenerator
from artap.datastore import SqliteDataStore
from artap.algorithm_sweep import SweepAlgorithm
# from artap.algorithm_nlopt import NLopt, LN_BOBYQA
from artap.algorithm_genetic import NSGAII

import numpy as np
from smt.surrogate_models import RBF, MGP


class ProblemBranin(Problem):
    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 3, 'bounds': [-10, 10]},
                           {'name': 'x_2', 'initial_value': 10, 'bounds': [-10, 10]}]
        self.costs = [{'name': 'F'}]

    def evaluate(self, individual):
        x = individual.vector
        y = (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2

        return [y]

    def predict(self, individual):
        sigma_MGP, sigma_KRG = self.surrogate.predict_variances(individual.vector, True)

        if sigma_MGP < 1e-3:
            self.surrogate.train_step *= 1.3

            value_problem = self.evaluate(individual)
            value_surrogate = self.surrogate.predict(individual.vector)
            # print(sigma_MGP, sigma_KRG, individual.vector, value_problem, value_surrogate)

            return value_surrogate

        return None


problem = ProblemBranin()
problem.data_store = SqliteDataStore(problem, database_name="data.sqlite", mode="rewrite")

# run optimization
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 10
algorithm.options['max_population_size'] = 10
algorithm.options['max_processes'] = 1
algorithm.run()

b = Results(problem)
optimum = b.find_optimum('F_1')  # Takes last cost function
print(optimum.vector, optimum.costs)

problem = None

# surrogate
trained_problem = ProblemBranin()
trained_problem.data_store = SqliteDataStore(trained_problem, database_name="data.sqlite")

# set custom regressor
trained_problem.surrogate = SurrogateModelSMT(trained_problem)
trained_problem.surrogate.regressor = MGP(theta0=[1e-2], n_comp=2, print_prediction=False)
trained_problem.surrogate.read_from_data_store()
trained_problem.surrogate.train()

# Tests
x = [0, 0]
print(trained_problem.surrogate.predict(x))
y = (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2
print(y)

algorithm = NSGAII(trained_problem)
algorithm.options['max_population_number'] = 50
algorithm.options['max_population_size'] = 10
algorithm.options['max_processes'] = 1
algorithm.run()


b = Results(trained_problem)
optimum = b.find_optimum('F_1')  # Takes last cost function
print(optimum.vector, optimum.costs)

trained_problem.logger.info("surrogate: predict / eval counter: {0:5.0f} / {1:5.0f}, total: {2:5.0f}".format(
    trained_problem.surrogate.predict_counter,
    trained_problem.surrogate.eval_counter,
    trained_problem.surrogate.predict_counter + trained_problem.surrogate.eval_counter))