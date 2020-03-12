import unittest
import time
import random
import threading
import rpyc

from artap.algorithm_sweep import SweepAlgorithm
from artap.problem import Problem
from artap.operators import LHSGeneration


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
        problem = SleepProblem()
        generator = LHSGeneration(problem.parameters)
        generator.init(4)

        algorithm = SweepAlgorithm(self.problem, generator=generator)
        algorithm.options['verbose_level'] = 0
        algorithm.options['max_processes'] = 3
        algorithm.options['n_iterations'] = 5
        algorithm.run()

    def test_run(self):
        self.problem = SleepProblem()

        # execute algorithm in different thread
        thread = threading.Thread(target=self.run_test, args=())
        thread.daemon = True
        thread.start()

        conn = rpyc.classic.connect("localhost", self.problem.monitor_service.port)
        while thread.is_alive():
            # print(len(conn.root.populations()))
            populations = conn.root.populations()
            if len(populations) == 1:
                for individual in populations[0].individuals:
                    print("individual = {}".format(individual))

            time.sleep(0.1)

        populations = conn.root.populations()
        self.assertEqual(len(populations[0].individuals), 4)


if __name__ == '__main__':
    unittest.main()
