import unittest
from unittest import TestCase, main

from artap.executor import CondorComsolJobExecutor, CondorMatlabJobExecutor, CondorPythonJobExecutor
from artap.problem import Problem
from artap.population import Population
from artap.algorithm import DummyAlgorithm
from artap.individual import Individual
from artap.config import config

import random


class CondorMatlabProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorMatlabProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                      {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        self.executor = CondorMatlabJobExecutor(self,
                                                script="./data/run_input.m",
                                                parameter_file="input.txt",
                                                files_from_condor=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class CondorComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]

        self.costs = [{'name': 'F_1'}]
        self.executor = CondorComsolJobExecutor(self, model_file="./data/elstat.mph",
                                                files_from_condor=["out.txt", "elstat.mph"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        line_with_results = content[5]  # 5th line contains results
        result = float(line_with_results)
        return [result]


class PythonExecProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        self.executor = CondorPythonJobExecutor(self,
                                                script="./data/run_exec.py",
                                                parameter_file=None,
                                                output_files=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class PythonInputProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        self.executor = CondorPythonJobExecutor(self,
                                                script="./data/run_input.py",
                                                parameter_file="input.txt",
                                                output_files=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class TestCondor(TestCase):
    """ Tests simple optimization problem where calculation of
        goal function is submitted as a job on HtCondor.
    """

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_matlab_input(self):
        """ Tests one calculation of goal function."""
        problem = CondorMatlabProblem()

        individuals = [Individual([1, 2])]
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(individuals)

        self.assertAlmostEqual(5, individuals[0].costs[0])

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = CondorComsolProblem()

        individuals = [Individual([10, 10]), Individual([11, 11])]
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(individuals)

        self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])
        self.assertAlmostEqual(124.23499735221547, individuals[1].costs[0])

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_exec(self):
        problem = PythonExecProblem()

        individuals = [Individual([1, 2])]
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(individuals)

        self.assertAlmostEqual(5, individuals[0].costs[0])

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_exec_full_load(self):
        problem = PythonExecProblem()

        n = 200
        individuals = []
        for i in range(n):
            individuals.append(Individual([random.randrange(1, 100), random.randrange(1, 100)]))

        algorithm = DummyAlgorithm(problem)
        algorithm.options['max_processes'] = 70
        algorithm.evaluate(individuals)

        for i in range(n):
            # print(individuals[i])
            self.assertEqual(int(individuals[i].costs[0]), individuals[i].vector[0]**2 + individuals[i].vector[1]**2)

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_input(self):
        problem = PythonInputProblem()

        individuals = [Individual([1, 2])]
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(individuals)

        self.assertAlmostEqual(5, individuals[0].costs[0])


if __name__ == '__main__':
    main()
