import os
import pylab as plt
import numpy
from artap.executor import LocalComsolExecutor
from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.algorithm_genetic import NSGAII
from artap.datastore import JsonDataStore
from artap.datastore import FileDataStore
from artap.results import Results

class ComsolProblem(Problem):
    def set(self):
        self.name = "ComsolProblem"
        tol = 5e-4
        self.parameters = [{'name': 'b1', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b2', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b3', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b4', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b5', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b6', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b7', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b8', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b9', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b10', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b11', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b12', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b13', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b14', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b15', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b16', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b17', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b18', 'initial_value': 0, 'bounds': [0, 3e-3 - tol]},
                           {'name': 'b19', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b20', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b21', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b22', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b23', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b24', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b25', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b26', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b27', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'b28', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f1', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f2', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f3', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f4', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f5', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f6', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f7', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f8', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f9', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f10', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f11', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f12', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f13', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f14', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f15', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f16', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f17', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f18', 'initial_value': 0, 'bounds': [0, 2.5e-3 - tol]},
                           {'name': 'f19', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f20', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f21', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f22', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f23', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f24', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f25', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f26', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f27', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]},
                           {'name': 'f28', 'initial_value': 0, 'bounds': [0, 2e-3 - tol]}]

        self.costs = [{'name': 'f1', 'criteria': 'minimize'},
                      {'name': 'f2', 'criteria': 'minimize'}]
        self.output_files = ["OUT.txt"]
        self.executor = CondorComsolJobExecutor(self, model_file="clutch.mph",
                                                files_from_condor=["OUT.txt"])

    def parse_results(self, output_files, individual):
        output_file = output_files[0]
        path = output_file
        with open(path) as file:
            content = file.read()
        f1 = float(content.split()[-2])
        f2 = float(content.split()[-1])
        return [f1, f2]

    def evaluate(self, individual):
        results = self.executor.eval(individual)
        f1 = results[0]
        f2 = results[1]
        return [f1, f2]  # method evaluate must return list

def solve():
    problem = ComsolProblem()  # Creating problem
    database_name = "." + os.sep + "data"
    problem.data_store = JsonDataStore(problem, database_name=database_name, mode="write")
    problem.options['save_data_files'] = True

    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 50
    algorithm.options['max_population_size'] = 50
    algorithm.options['max_processes'] = 10
    algorithm.run()


def process_results():
    problem = ComsolProblem()
    database_name = "." + os.sep + "data"
    problem.data_store = JsonDataStore(problem, database_name=database_name, mode="read")
    problem.data_store.problem.populations = problem.data_store.problem.populations[0:-1]
    b = Results(problem.data_store.problem)
    # Plot Results

    F_cost = []
    V_cost = []
    for j in range(0, 50):
        for i in range(0, 50):
            F = problem.data_store.problem.populations[j].individuals[i].costs[0]
            V = problem.data_store.problem.populations[j].individuals[i].costs[1]
            F_cost.append(F)
            V_cost.append(V)

    pvalues = b.pareto_values()
    f_all = [i[0] for i in pvalues]
    v_all = [i[1] for i in pvalues]

    plt.scatter(F_cost, V_cost, alpha=0.3)
    plt.scatter(f_all, v_all)

    plt.grid()
    plt.xlabel('Force [N]')
    plt.ylabel('Volume [m3]')
    plt.savefig('Pareto_new.pdf')
    plt.show()

    maxF = numpy.amin(F_cost)
    minV = numpy.amin(V_cost)
    print('Max Force: ', maxF, '; Min Volume: ', minV, '\n')

solve()
process_results()
