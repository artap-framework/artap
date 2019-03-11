import unittest

from pygments.lexer import words

from artap.problem import Problem
from artap.algorithm_genetic import NSGA_II
from artap.results import Results
import sys
sys.path.insert(0, '~/agros2d/resources/python/')

sys.path.append('/home/tamas/agros2d/resources/python/')
print(sys.path)
from agros_script import run_fem
from optimization_functions import *

class TrOptimizer(Problem):
    """Test the convergence in a one objective example with a simple 2 variable Ackley N2 formula"""

    def __init__(self, name):
        parameters = {'r_c': {'initial_value': 2.5, 'bounds': [400., 700.], 'precision': 1.},
                      'b_c': {'initial_value': 1.65, 'bounds': [1.5, 1.7], 'precision': 1e-1},
                      'j_in': {'initial_value': 3.0, 'bounds': [1.5, 3.0], 'precision': 1e-1},
                      'j_ou': {'initial_value': 3.0, 'bounds': [1.5, 3.0], 'precision': 1e-1},
                      'j_reg': {'initial_value': 3.5, 'bounds': [2., 3.5], 'precision': 1e-1},
                      'h_in': {'initial_value': 1400., 'bounds': [1000., 2000.], 'precision': 5.},
                      'm_gap': {'initial_value': 37., 'bounds': [37., 64.], 'precision': 1.},
                      }
        costs = ['F_1']

        super().__init__(name, parameters, costs)
        self.options['save_level'] = "population"
        self.options['max_processes'] = 10

    def eval(self, r_c, b_c, j_in, j_ou, j_reg, h_in, m_gap):

        indep = ind = independent_variables(r_c=260.4, b_c=1.7,
                                            j_in=1.7, j_ou=1.5, j_reg=3.5, h_in=1460, m_gap=46.)

        # define parameters
        p = Parameters()
        p.power = 31500.
        p.freq = 50.
        p.ph_num = 3.
        p.drop_tol = 0.05
        p.drop = 14.5  # expected
        p.gap = 37.
        p.gap_core = 20.
        p.ei = 150.
        p.phase_distance = 71. / 2.
        p.ff_c = 0.9
        p.cc = 3.5
        p.u_in_line = 33.  # line voltage in the inner winding
        p.u_in = 19.05
        p.u_out = 132.
        p.ff_in = 0.6
        p.ff_ou = 0.60
        p.win_c = 10.
        p.wout_c = 8.5
        p.reg_range = 0.10
        p.ff_reg = 0.65
        p.alpha = 0.97
        p.beta = 0.85

        p.ll_c = 2000.
        p.nll_c = 6000.

        p.con_fact_in = 1.
        p.con_fact_ou = 1.73
        p.u_out = 132.  # phase voltage on the outer terminal [kV]
        p.u_out_line = 132.

        ####
        p.in_ins_ax = 3.5
        p.in_ins_rad = 0.45
        p.in_ins_s = 0.17  # ctx
        p.ou_ins_ax = 4.8
        p.ou_ins_rad = 0.5
        p.ou_ins_s = 0.3  # triple twins

        dep = calc_dependent_variables(ind, p)


        return run_fem(p, dep, indep)


class TestTrOptimizer(unittest.TestCase):
    """ Tests that the NSGA II algorithm can find the global optimum of a function."""

    def test_local_problem(self):
        problem = TrOptimizer("LocalPythonProblem")
        algorithm = NSGA_II(problem)
        algorithm.options['max_population_number'] = 15
        algorithm.options['max_population_size'] = 100
        algorithm.options['calculate_gradients'] = True
        algorithm.run()

        b = Results(problem)
        optimum = b.find_minimum('F_1')  # Takes last cost function
        #self.assertAlmostEqual(optimum, -200, 0)


if __name__ == '__main__':
    unittest.main()
