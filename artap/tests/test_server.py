import unittest
import time
import random
import threading
import rpyc

from artap.algorithm_sweep import SweepAlgorithm
from artap.problem import Problem
from artap.operators import LHSGeneration
from artap.monitor import MONITOR_PORT


class SleepProblem(Problem):
    def set(self, **kwargs):
        self.name = 'Sleep Problem'
        self.parameters = [{'name': 'x', 'bounds': [-5., 5.]}]

        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, x):
        time.sleep(random.randrange(1, 3))

        return [x.vector[0]**2]


class TestServer(unittest.TestCase):
    def run_test(self):
        generator = LHSGeneration(self.problem.parameters)
        generator.init(5)

        algorithm = SweepAlgorithm(self.problem, generator=generator)
        algorithm.options['verbose_level'] = 0
        algorithm.options['max_processes'] = 3
        algorithm.options['n_iterations'] = 5
        algorithm.run()

    def test_run(self):
        self.problem = SleepProblem()

        # execute algorithm in different thread
        thread = threading.Thread(target=self.run_test, args=())
        thread.start()

        # connect to server
        conn = rpyc.classic.connect("localhost", self.problem.monitor_service.port)
        while thread.is_alive():
            # print(len(conn.root.populations()))
            populations = conn.root.populations()
            if len(populations) == 1:
                for individual in populations[0].individuals:
                    # print("individual = {}".format(individual))
                    pass

            time.sleep(0.1)

        populations = conn.root.populations()
        self.assertEqual(len(populations[0].individuals), 4)


class TestServer(unittest.TestCase):
    def run_test(self, n):
        problem = SleepProblem()
        problem.name = "SleepProblem{}".format(n)
        generator = LHSGeneration(problem.parameters)
        generator.init(1)

        algorithm = SweepAlgorithm(problem, generator=generator)
        algorithm.options['verbose_level'] = 0
        algorithm.options['max_processes'] = 1
        algorithm.options['n_iterations'] = 1
        algorithm.run()

    def test_run(self):
        ok = False

        n = 4
        for i in range(n):
            # execute algorithm in different thread
            thread = threading.Thread(target=self.run_test, args=(i, ))
            thread.start()
            time.sleep(0.2)

        port = MONITOR_PORT
        # connect to server
        i = 0
        while i < n:
            try:
                conn = rpyc.classic.connect("localhost", port)
                # print("Connected to {} at port {}".format(conn.root.problem.name, port))
                i = i + 1
            except Exception as e:
                # print(e)
                pass

            port = port + 1

            # emergency exit
            if port > MONITOR_PORT + n + 100:
                break

        self.assertTrue(i == n)


if __name__ == '__main__':
    unittest.main()
