import os
from unittest import TestCase, main

from artap.executor import CondorJobExecutor
from artap.problem import Problem
from artap.population import Population
from artap.algorithm import DummyAlgorithm


class CondorMatlabProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'a': {'initial_value': 10, 'bounds': [0, 20]},
                      'b': {'initial_value': 10, 'bounds': [5, 15]}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "workspace" + os.sep + "condor_matlab" + os.sep)

        self.executor = CondorJobExecutor(self,
                                          command="run.sh",
                                          model_file="run_input.m",
                                          input_file="input.txt",
                                          output_file="output.txt",
                                          supplementary_files=["run.sh"])

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        return [float(content)]


class CondorComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        parameters = {'a': {'initial_value': 10, 'bounds': [0, 20]},
                      'b': {'initial_value': 10, 'bounds': [5, 15]}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "workspace" + os.sep + "condor_comsol" + os.sep)

        self.executor = CondorJobExecutor(self,
                                          command="run.sh",
                                          model_file="elstat.mph",
                                          output_file="out.txt",
                                          supplementary_files=["run.sh"])

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        lines = content.split("\n")
        line_with_results = lines[5]  # 5th line contains results
        result = float(line_with_results)
        return [result]


class TestPythonExecProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10},
                      'x_2': {'initial_value': 10}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "workspace" + os.sep + "condor_python_exec" + os.sep)

        self.executor = CondorJobExecutor(self,
                                          command="/usr/bin/python3",
                                          model_file="run_exec.py",
                                          output_file="output.txt")

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        return [float(content)]


class TestPythonInputProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10},
                      'x_2': {'initial_value': 10}}
        costs = ['F1']

        super().__init__(name, parameters, costs,
                         working_dir="." + os.sep + "workspace" + os.sep + "condor_python_input" + os.sep)

        self.executor = CondorJobExecutor(self,
                                          command="/usr/bin/python3",
                                          model_file="run_input.py",
                                          input_file="input.txt", # file is created in eval with specific parameters
                                          output_file="output.txt")

    def evaluate(self, x):
        return self.executor.eval(x)

    def parse_results(self, content):
        return [float(content)]


class TestCondor(TestCase):
    """ Tests simple optimization problem where calculation of
        goal function is submitted as a job on HtCondor.
    """
    def test_condor_matlab_input(self):
        """ Tests one calculation of goal function."""
        problem = CondorMatlabProblem("CondorMatlabProblem")

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        population.individuals = evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5.0, population.individuals[0].costs[0])

    def test_condor_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = CondorComsolProblem("CondorComsolProblem")

        table = [[10, 10], [11, 11]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        population.individuals = evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])
        self.assertAlmostEqual(124.23499735221547, population.individuals[1].costs[0])

    def test_condor_python_exec(self):
        problem = TestPythonExecProblem("CondorPythonExecProblem")

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        population.individuals = evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5.0, population.individuals[0].costs[0])

    def test_condor_python_input(self):
        problem = TestPythonInputProblem("CondorPythonInputProblem")

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        population.individuals = evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5.0, population.individuals[0].costs[0])


if __name__ == '__main__':
    main()
