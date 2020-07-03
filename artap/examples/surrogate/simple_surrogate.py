from math import sin

from artap.problem import Problem
from artap.results import Results
from artap.operators import LHSGenerator
from artap.algorithm_nlopt import NLopt, LN_BOBYQA, GN_DIRECT_L_RAND
from artap.algorithm_sweep import SweepAlgorithm
from artap.surrogate_smt import SurrogateModelSMT

class ArtapProblem(Problem):
    def set(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 0.1, 'bounds': [0.0, 1.0]}]
        self.costs = [{'name': 'F_1'}]

    def evaluate(self, individual):
        x = individual.vector

        # the goal function
        F1 = (6*x[0] - 2) ** 2 * sin(12*x[0] - 4)

        return [F1]


# Optimization with Nelder-Mead
problem = ArtapProblem()

# enable surrogate
problem.surrogate = SurrogateModelSMT(problem)
problem.surrogate.regressor = SurrogateModelSMT.get_kpls_regressor()
problem.surrogate.train_step = 10
problem.surrogate.score_threshold = 0.0
problem.surrogate.distance_threshold = 1

# sweep analysis (for training)
gen = LHSGenerator(parameters=problem.parameters)
gen.init(problem.surrogate.train_step)
algorithm_sweep = SweepAlgorithm(problem, generator=gen)
algorithm_sweep.run()

# set the optimization method
algorithm = NLopt(problem)
algorithm.options['verbose_level'] = 0
algorithm.options['algorithm'] = GN_DIRECT_L_RAND
algorithm.options['xtol_abs'] = 1e-6
algorithm.options['xtol_rel'] = 1e-3
algorithm.options['ftol_rel'] = 1e-3
algorithm.options['ftol_abs'] = 1e-6
algorithm.options['n_iterations'] = 100
# perform the optimization
algorithm.run()

results = Results(problem)

opt = results.find_optimum('F_1')

print('The exact value of the optimization is at x_1 = 0.757, F_1 = -6.021')
print('Optimal solution (DIRECT_L_RAND) x_1 = {}, F_1 = {}'.format(opt.vector[0], opt.costs[0]))

print("surrogate.predict_counter: {}".format(problem.surrogate.predict_counter))
print("surrogate.eval_counter: {}".format(problem.surrogate.eval_counter))
