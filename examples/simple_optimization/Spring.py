import matplotlib.pyplot as plt

from artap.algorithm_swarm import SMPSO, OMOPSO
from artap.problem import Problem
from artap.results import Results
from pylab import cos, pi, plot, show


class SpringDamperSMPSO(Problem):
    def set(self):
        self.name = 'Spring Damper'

        self.parameters = [{'name': 'x', 'initial_value': 0, 'bounds': [0, 1], 'parameter_type': 'integer'},
                           {'name': 'v', 'initial_value': 1.2, 'bounds': [0, 1.5], 'parameter_type': 'integer'}]

        self.costs = [{'name': 'f_1'}]

    def evaluate(self, individual):
        x = individual.vector[0]
        v = individual.vector[1]

        k = 124e3
        m = 64
        c = 3
        g = 9.8
        omega = 1.0
        A = 5
        # t = np.arange(0.0, 2.0, 0.001)
        # t = np.array(np.round(1, 100))

        f_1 = -(k * x / m) - (c * v) - g + (A * cos(2 * pi * omega))

        return [f_1]


problem = SpringDamperSMPSO()
algorithm = SMPSO(problem)
# algorithm = OMOPSO(problem)

algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 100
s = algorithm.run()

results = Results(problem)
solution = results.pareto_values()
# solution = results.find_optimum()

plot(solution, 'o')
show()
