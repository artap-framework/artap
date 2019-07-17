from artap.problem import Problem
from artap.algorithm_genetic import NSGAII, EpsMOEA
from artap.results import Results, GraphicalResults

import matplotlib.pyplot as plt


class BiObjectiveTestProblem(Problem):
    """
    From GDE3: The third Evolution Step of Generalized Dierential Evolution
    Saku Kukkonen, Jouni Lampinen

    Minimize f1 = x1
    Minimize f2 = (1+x2) / x1

    subject to
            x1 e [0.1, 1]
            x2 e [0, 5]

    The Pareto front is a hyperbola-
    """

    def set(self):
        self.name = 'Biobjective Test Problem'
        self.parameters = [{'name':'x_1', 'initial_value': .5, 'bounds': [0.1, 1.]},
                           {'name':'x_2', 'initial_value': .5, 'bounds': [0.0, 5.0]}]

        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}, {'name': 'F_2', 'criteria': 'minimize'}]



    def evaluate(self, individual):
        x = individual.vector
        f1 = x[0]
        f2 = (1+x[1])/x[0]
        return [f1, f2]

#def test_problem():

problem = BiObjectiveTestProblem()
algorithm = NSGAII(problem)
algorithm.options['max_population_number'] = 100
algorithm.options['max_population_size'] = 100
algorithm.run()

b = Results(problem)

b = Results(problem)
solution = b.pareto_values()

print(solution)


plt.scatter([s[0] for s in solution],
            [s[1] for s in solution])
plt.xlim([0, 1.05])
plt.ylim([0, 10.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.show()

#b.find_pareto('F_1','F_2')
#solutions = problem.data_store.populations[5]
#for solution in solutions.individuals:
#        print(solution.vector)


#test_problem()