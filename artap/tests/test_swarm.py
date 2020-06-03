import unittest
from artap.benchmark_functions import Ackley
from artap.algorithm_swarm import SwarmAlgorithm, OMOPSO
from artap.problem import Problem
from artap.individual import Individual


class TestProblem(Problem):

    def set(self):
        self.name = 'Test Problem'
        self.parameters = [{'name': '1', 'bounds': [2., 10.]},
                           {'name': '2', 'bounds': [2., 20.]},
                           ]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        return [1, 1]


class TestSwarm(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()

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

    def test_particle_best_should_initialized_correctly(self):
        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [], 'best_cost': [], 'best_vector': []}  #

        population = [z]

        self.Swarm.init_pbest(population)

        self.assertEqual(z.features['best_cost'], z.costs_signed)
        self.assertEqual(z.features['best_vector'], z.vector)

    def test_particle_best_update_should_change_the_values(self):
        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [1, 2], 'best_cost': [2., 2., 0.], 'best_vector': [1, 2]}

        population = [z]

        self.Swarm.update_particle_best(population)

        self.assertEqual(z.features['best_cost'], z.costs_signed)
        self.assertEqual(z.features['best_vector'], z.vector)

    def test_particle_best_update_should_not_change_the_values(self):
        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [z]

        self.Swarm.update_particle_best(population)
        self.assertNotEqual(z.features['best_cost'], z.costs_signed)


class TestSwarm(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()
        self.omopso = OMOPSO(problem)
        self.omopso.mutator.probability = 1.0

    def test_turbulence_should_change_vector(self):

        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [z]
        self.omopso.turbulence(population)

        # the new population vector should be differ from the original one
        self.assertNotEqual(population[0].vector, [1,2])

        # it should preserve the features
        self.assertEqual(population[0].features, z.features)
