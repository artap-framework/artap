from artap.algorithm_swarm import SMPSO, OMOPSO, PSOGA
from artap.problem import Problem
from artap.results import Results
from pylab import cos, sin, exp, plot, show, e


class MishrasBirdFunction(Problem):
    """
      f(x,y)=sin(y)e^{[(1- cos x)^{2}]}+cos(x)e^{[(1- sin y)^{2}]} + (x-y)^{2}
      subjected to: (x+5)^{2} + (y+5)^{2}<25
    """

    def set(self):
        self.name = 'Mishra Bird Function'

        self.parameters = [{'name': 'x', 'bounds': [-10, 0]},
                           {'name': 'y', 'bounds': [-6.5, 0]}]

        self.costs = [{'name': 'f_1'}]

    def evaluate(self, individual):
        x = individual.vector[0]
        y = individual.vector[1]

        constraint = (x + 5) ** 2 + (y + 5) ** 2
        f_1 = sin(y) * exp(1 - cos(x) ** 2) + cos(x) * exp(1 - sin(y) ** 2) + (x - y) ** 2
        if constraint > 25:
            f_1 = 0
        return [f_1]


problem = MishrasBirdFunction()
# algorithm = SMPSO(problem)
# algorithm = OMOPSO(problem)
algorithm = PSOGA(problem)

algorithm.options['max_population_number'] = 20
algorithm.options['max_population_size'] = 20
algorithm.run()

results = Results(problem)
solution = results.find_optimum()

pareto = results.pareto_values()

plot(pareto)
show()


