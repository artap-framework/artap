import os
from unittest import TestCase, main

from artap.executor import CondorComsolJobExecutor
from artap.problem import Problem, ProblemType
from artap.population import Population
from artap.algorithm import DummyAlgorithm


# class CondorMatlabProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#
#     def set(self):
#         self.name = "CondorMatlabProblem"
#         self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
#                       {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
#         self.costs = [{'name': 'F_1'}]
#         self.working_dir = "." + os.sep + "data" + os.sep
#         self.type = ProblemType.matlab
#         self.executor = CondorJobExecutor(self,
#                                           command="run.sh",
#                                           model_file="run_input.m",
#                                           input_file="input.txt",
#                                           output_file="output.txt",
#                                           supplementary_files=["run.sh"])
#
#     def evaluate(self, individual):
#         return self.executor.eval(individual.vector)    # ToDo: could be passed individual?
#
#     def parse_results(self, content):
#         return [float(content)]


class CondorComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]

        self.costs = [{'name': 'F_1'}]
        self.type = ProblemType.comsol
        self.executor = CondorComsolJobExecutor(self, model_file="./data/elstat.mph", output_files=["out.txt", "elstat.mph"],)

    def evaluate(self, individual):
        return self.executor.eval(individual.vector)

    def parse_results(self, output_files):
        with open(output_files[0]) as file:
            content = file.readlines()
        line_with_results = content[5]  # 5th line contains results
        result = float(line_with_results)
        return [result]


# class PythonExecProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#     def set(self):
#         self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
#                            {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
#         self.costs = [{'name': 'F_1'}]
#         self.working_dir = "." + os.sep + "data" + os.sep
#         self.type = ProblemType.python
#         self.executor = CondorJobExecutor(self,
#                                           command="/usr/bin/python",
#                                           model_file="run_exec.py",
#                                           output_file="output.txt")
#
#     def evaluate(self, individual):
#         return self.executor.eval(individual.vector)
#
#     def parse_results(self, content):
#         return [float(content)]
#
#
# class PythonInputProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#     def set(self):
#         self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
#                            {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
#         self.costs = [{'name': 'F_1'}]
#         self.working_dir = "." + os.sep + "data" + os.sep
#         self.type = ProblemType.python
#         self.executor = CondorJobExecutor(self,
#                                           command="/usr/bin/python",
#                                           model_file="run_input.py",
#                                           input_file="input.txt",  # file is created in eval with specific parameters
#                                           output_file="output.txt")
#
#     def evaluate(self, individual):
#         return self.executor.eval(individual.vector)
#
#     def parse_results(self, content):
#         return [float(content)]


class TestCondor(TestCase):
    """ Tests simple optimization problem where calculation of
        goal function is submitted as a job on HtCondor.
    """
    # def test_condor_matlab_input(self):
    #     """ Tests one calculation of goal function."""
    #     problem = CondorMatlabProblem()
    #
    #     table = [[1, 2]]
    #     population = Population()
    #     population.gen_population_from_table(table)
    #     evaluator = DummyAlgorithm(problem)
    #     evaluator.evaluate(population.individuals)

    #    self.assertAlmostEqual(5, population.individuals[0].costs[0])

    def test_condor_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = CondorComsolProblem()
        problem.options['save_data_files'] = True
        table = [[10, 10], [11, 11]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.options["max_processes"] = 1
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])
        self.assertAlmostEqual(124.23499735221547, population.individuals[1].costs[0])

    # def test_condor_python_exec(self):
    #     problem = PythonExecProblem()
    #
    #     table = [[1, 2]]
    #     population = Population()
    #     population.gen_population_from_table(table)
    #     evaluator = DummyAlgorithm(problem)
    #     evaluator.evaluate(population.individuals)
    #
    #     self.assertAlmostEqual(5, population.individuals[0].costs[0])
    #
    # def test_condor_python_input(self):
    #     problem = PythonInputProblem()
    #
    #     table = [[1, 2]]
    #     population = Population()
    #     population.gen_population_from_table(table)
    #     evaluator = DummyAlgorithm(problem)
    #     evaluator.evaluate(population.individuals)
    #
    #     self.assertAlmostEqual(5, population.individuals[0].costs[0])


if __name__ == '__main__':
    main()
