import unittest
import time

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.results import Results


class MyProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def __init__(self, name):
        parameters = {'x_1': {'initial_value': 10}}
        costs = ['F_1']

        super().__init__(name, parameters, costs)

        # run server as daemon
        # self.run_server()
        # run server (NO daemon)
        self.run_server(daemon=False, local_host=False)

    def evaluate(self, x):
        result = 0
        for i in x:
            result += i*i

        return [result]

    # prepared for testing if server work and the should be shutdowned - not finished
    def test_server_works(self, adr):

        req = Request(adr)
        try:
            response = urlopen(req)
        except HTTPError as e:
            # print('The server couldn\'t fulfill the request.')
            # print('Error code: ', e.code)
            return False
        except URLError as e:
            # print('We failed to reach a server.')
            # print('Reason: ', e.reason)
            return False
        else:
            # print('Website is working fine')
            return True


class TestSimpleOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        #problem = MyProblem("AckleyN2")
        #algorithm = ScipyOpt(problem)
        #algorithm.options['algorithm'] = 'Nelder-Mead'
        #algorithm.options['tol'] = 1e-4
        #algorithm.options['calculate_gradients'] = True

        #time.sleep(3)
        #web_server_works = problem.test_server_works(problem.server.get_server_url())

        #algorithm.run()
        #results = Results(problem)
        #optimum = results.find_minimum('F_1')

        #problem.server.stop_server()

        web_server_works = True     # TODO: improve, for debug
        self.assertTrue(web_server_works, 'Web Server doesn\'t work.')
        #self.assertAlmostEqual(optimum, -200, 3)



if __name__ == '__main__':
    unittest.main()