import time
import numpy as np
from artap.algorithm_monte_carlo import Monte_Carlo
from artap.results import Results
from artap.benchmark_functions import BenchmarkFunction, Sphere, Ackley


class single_Problem(BenchmarkFunction):
    def set(self, **kwargs):
        """Time-dependent 1D QM wave function of a single particle - squared."""
        self.set_dimension(**kwargs)
        self.parameters = self.generate_paramlist(self.dimension, lb=-5.12, ub=5.12)

        self.global_optimum = 0.
        self.global_optimum_coords = [0.0 for x in range(self.dimension)]

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, z):
        x = z.vector
        output = np.exp(-x[0] ** 2) / (np.pi ** 0.5)
        return [output]


def test_local_problem1():
    problem = Sphere(**{'dimension': 1})
    n = 10
    algorithm = Monte_Carlo(problem, n)
    adaptive_result = np.zeros(n)
    adaptive_err = np.zeros(n)
    adaptive_eva = np.zeros(n)
    start = time.time()
    print("Running monte carlo for sphere function ...")
    for i in range(n):  # repeat the integrator for n times
        adaptive_result[i], adaptive_err[i], adaptive_eva[i] = algorithm.run()
        print(
            "Run {0}".format(
                i + 1),
            ": Result: ",
            adaptive_result[i],
            ", standard error: ",
            adaptive_err[i],
            "function evaluation:",
            adaptive_eva[i])
    end = time.time()
    mean = np.mean(adaptive_result)  # take the mean of n integration values
    # find the standard error of the mean
    error = np.std(adaptive_result) / np.sqrt(n)
    print("Mean of results:", mean, ", with error of the mean: ", error,
          " and averaged standard error: ", np.mean(adaptive_err))
    print(
        "Mean of function evaluations: ",
        np.mean(adaptive_eva),
        " with standard error of the mean: ",
        np.std(adaptive_eva) /
        np.sqrt(n))
    print("Average time usage: ", (end - start) / n, " seconds.")


def test_local_problem2():
    problem = Ackley(**{'dimension': 1})
    n = 10
    algorithm = Monte_Carlo(problem, n)
    adaptive_result = np.zeros(n)
    adaptive_err = np.zeros(n)
    adaptive_eva = np.zeros(n)
    start = time.time()
    print("Running monte carlo for sphere function ...")
    for i in range(n):  # repeat the integrator for n times
        adaptive_result[i], adaptive_err[i], adaptive_eva[i] = algorithm.run()
        print(
            "Run {0}".format(
                i + 1),
            ": Result: ",
            adaptive_result[i],
            ", standard error: ",
            adaptive_err[i],
            "function evaluation:",
            adaptive_eva[i])
    end = time.time()
    mean = np.mean(adaptive_result)  # take the mean of n integration values
    # find the standard error of the mean
    error = np.std(adaptive_result) / np.sqrt(n)
    print("Mean of results:", mean, ", with error of the mean: ", error,
          " and averaged standard error: ", np.mean(adaptive_err))
    print(
        "Mean of function evaluations: ",
        np.mean(adaptive_eva),
        " with standard error of the mean: ",
        np.std(adaptive_eva) /
        np.sqrt(n))
    print("Average time usage: ", (end - start) / n, " seconds.")


def test_local_problem3():
    problem = single_Problem(**{'dimension': 1})
    n = 10
    algorithm = Monte_Carlo(problem, n)
    adaptive_result = np.zeros(n)
    adaptive_err = np.zeros(n)
    adaptive_eva = np.zeros(n)
    start = time.time()
    print("Running monte carlo for problem function ...")
    for i in range(n):  # repeat the integrator for n times
        adaptive_result[i], adaptive_err[i], adaptive_eva[i] = algorithm.run()
        print(
            "Run {0}".format(
                i + 1),
            ": Result: ",
            adaptive_result[i],
            ", standard error: ",
            adaptive_err[i],
            "function evaluation:",
            adaptive_eva[i])
    end = time.time()
    mean = np.mean(adaptive_result)  # take the mean of n integration values
    # find the standard error of the mean
    error = np.std(adaptive_result) / np.sqrt(n)
    print("Mean of results:", mean, ", with error of the mean: ", error,
          " and averaged standard error: ", np.mean(adaptive_err))
    print(
        "Mean of function evaluations: ",
        np.mean(adaptive_eva),
        " with standard error of the mean: ",
        np.std(adaptive_eva) /
        np.sqrt(n))
    print("Average time usage: ", (end - start) / n, " seconds.")


if __name__ == '__main__':
    # test_local_problem1()
    test_local_problem2()
    # test_local_problem3()
