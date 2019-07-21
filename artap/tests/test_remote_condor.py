from unittest import TestCase, main

from artap.executor import CondorComsolJobExecutor, CondorMatlabJobExecutor, CondorPythonJobExecutor
from artap.problem import Problem, ProblemType
from artap.population import Population
from artap.algorithm import DummyAlgorithm


class CondorMatlabProblem(Problem):
    """ Describe simple one objective optimization problem. """

    def set(self):
        self.name = "CondorMatlabProblem"
        self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0, 20]},
                      {'name': 'b', 'initial_value': 10, 'bounds': [5, 15]}]
        self.costs = [{'name': 'F_1'}]
        self.type = ProblemType.matlab
        self.executor = CondorMatlabJobExecutor(self,
                                                script="./data/run_input.m",
                                                parameter_file="input.txt",
                                                files_from_condor=["output.txt"])

    def evaluate(self, individual):
        return self.executor.eval(individual)    # ToDo: could be passed individual?

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
        self.type = ProblemType.comsol
        self.executor = CondorComsolJobExecutor(self, model_file="./data/elstat.mph",
                                                files_from_condor=["out.txt", "elstat.mph"], )

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
        self.type = ProblemType.python
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
        self.type = ProblemType.python
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
    def test_condor_matlab_input(self):
        """ Tests one calculation of goal function."""
        problem = CondorMatlabProblem()

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5, population.individuals[0].costs[0])

    def test_condor_comsol_exec(self):
        """ Tests one calculation of goal function."""
        problem = CondorComsolProblem()
        problem.options['save_data_files'] = True
        table = [[10, 10], [11, 11]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(112.94090668383139, population.individuals[0].costs[0])
        self.assertAlmostEqual(124.23499735221547, population.individuals[1].costs[0])

    def test_condor_python_exec(self):
        problem = PythonExecProblem()

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5, population.individuals[0].costs[0])

    def test_condor_python_input(self):
        problem = PythonInputProblem()

        table = [[1, 2]]
        population = Population()
        population.gen_population_from_table(table)
        evaluator = DummyAlgorithm(problem)
        evaluator.evaluate(population.individuals)

        self.assertAlmostEqual(5, population.individuals[0].costs[0])


if __name__ == '__main__':
    main()
