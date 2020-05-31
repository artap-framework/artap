import unittest
from artap.benchmark_functions import Ackley
from artap.algorithm_swarm import SwarmAlgorithm
from artap.problem import Problem


class TestSwarm(unittest.TestCase):

    def setUp(self):
        problem = Problem()
        self.Swarm = SwarmAlgorithm(problem)

    def test_should_constructor_create_a_valid_object(self):
        self.assertIsNotNone(self.Swarm)

    def test_constrictionfactor(self):
        # results should be 1.
        self.assertEqual(self.Swarm.khi(1., 1.), 1.)

        # result should be -0.2087
        self.assertAlmostEqual(self.Swarm.khi(3., 4.), -0.2087, 4)

    def test_speed_max_should_reduce_speed(self):
        self.assertAlmostEqual(self.Swarm.speed_constriction(1., 1., 0.), 0.5)

    def test_speed_max_should_increase_speed(self):
        self.assertEqual(self.Swarm.speed_constriction(-1., 0., -1.), -0.5)

    def test_speed_do_not_change(self):
        self.assertEqual(self.Swarm.speed_constriction(0.1, 0., -1.), 0.1)


