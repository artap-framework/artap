import unittest
from unittest import TestCase, main

from ..executor import CondorComsolJobExecutor, CondorMatlabJobExecutor, CondorPythonJobExecutor, CondorCSTJobExecutor
from ..algorithm_genetic import NSGAII
from ..problem import Problem
from ..algorithm import DummyAlgorithm
from ..individual import Individual
from ..config import config

import random
import pathlib
import os
import zipfile


class CondorMatlabProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorMatlabProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                      {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/run_input.m")
        self.executor = CondorMatlabJobExecutor(self,
                                                script=file_path,
                                                parameter_file="input.txt",
                                                files_from_condor=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class ComsolProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorComsolProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]

        self.costs = [{'name': 'F_1'}]
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/elstat.mph")
        self.executor = CondorComsolJobExecutor(self, model_file=file_path,
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
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/run_exec.py")
        self.executor = CondorPythonJobExecutor(self,
                                                script=file_path,
                                                parameter_file=None,
                                                output_files=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class PythonExecProblemNSGAII(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                           {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/run_exec.py")
        self.executor = CondorPythonJobExecutor(self,
                                                script=file_path,
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
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/run_input.py")
        self.executor = CondorPythonJobExecutor(self,
                                                script=file_path,
                                                parameter_file="input.txt",
                                                output_files=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
        return [float(content[0])]


class CSTProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.parameters = [{'name': 'a', 'initial_value': 0.1, 'bounds': [0, 1]}]
        self.costs = [{'name': 'F_1'}]
        file_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), "data/elstat.cst")
        self.executor = CondorCSTJobExecutor(self,
                                             model_file=file_path,
                                             files_from_condor=["elstat.zip"])

    def evaluate(self, individual):
        return self.executor.eval(individual)

    def parse_results(self, output_files, individual):
        archive = zipfile.ZipFile(output_files[0], 'r')
        file = archive.open('elstat/Export/Es Solver/Energy.txt')
        content = file.readlines()

        return [float(content[0])]

    def evaluate(self, individual):
        return self.executor.eval(individual)


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
        problem = ComsolProblem()

        individuals = [Individual([10, 10])]
        algorithm = DummyAlgorithm(problem)
        algorithm.evaluate(individuals)

        self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_cst_exec(self):
        """ Tests one calculation of goal function."""
        problem = CSTProblem()

        individuals = [Individual([0.7])]
        algorithm = DummyAlgorithm(problem)
        algorithm.evaluate(individuals)

        # self.assertAlmostEqual(112.94090668383139, individuals[0].costs[0])
        self.assertAlmostEqual(0, 0)

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_exec(self):
        problem = PythonExecProblem()

        individuals = [Individual([1, 2])]
        algorithm = DummyAlgorithm(problem)
        algorithm.evaluator.evaluate(individuals)

        self.assertAlmostEqual(5, individuals[0].costs[0])

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_exec_full_load(self):
        problem = PythonExecProblem()

        n = 50
        individuals = []
        for i in range(n):
            individuals.append(Individual([random.randrange(1, 100), random.randrange(1, 100)]))

        algorithm = DummyAlgorithm(problem)
        algorithm.options['max_processes'] = 70
        algorithm.evaluator.evaluate(individuals)

        for i in range(n):
            # print(individuals[i])
            self.assertEqual(int(individuals[i].costs[0]), individuals[i].vector[0]**2 + individuals[i].vector[1]**2)

    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_input(self):
        problem = PythonInputProblem()

        individuals = [Individual([1, 2])]
        algorithm = DummyAlgorithm(problem)
        algorithm.evaluator.evaluate(individuals)

        self.assertAlmostEqual(5, individuals[0].costs[0])


    @unittest.skipIf(config["condor_host"] is None, "Condor is not defined.")
    def test_condor_python_exec_nsgaii(self):
        problem = PythonExecProblemNSGAII()

        algorithm = NSGAII(problem)
        algorithm.options['max_population_number'] = 5
        algorithm.options['max_population_size'] = 3
        algorithm.options['max_processes'] = 3
        algorithm.run()

        populations = problem.populations()

        self.assertEqual(len(populations), algorithm.options['max_population_number'] + 1)
        for individuals in populations.values():
            self.assertEqual(len(individuals), algorithm.options['max_population_size'])


if __name__ == '__main__':
    main()
