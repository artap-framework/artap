import unittest
from ..benchmark_functions import Ackley
from ..algorithm_swarm import SwarmAlgorithm, OMOPSO
from ..problem import Problem
from ..individual import Individual
from ..archive import Archive


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


class TestOMOPSOTOOLS(unittest.TestCase):
    def setUp(self):
        problem = TestProblem()
        self.omopso = OMOPSO(problem)
        self.omopso.non_uniform_mutator.probability = 1.0
        self.omopso.uniform_mutator.probability = 1.0

    def test_turbulence_should_change_vector(self):
        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [z]

        self.omopso.turbulence(population)

        # the new population vector should be differ from the original one
        self.assertNotEqual(population[0].vector, [1, 2])

        # it should preserve the features
        self.assertEqual(population[0].features, z.features)

    def test_init_velocity(self):
        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        z.features = {'velocity': [], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [z]

        self.omopso.init_pvelocity(population)
        self.assertEqual(z.features['velocity'], [0, 0])

    def test_global_best(self):
        x = Individual([1, 2])
        x.costs = [2.0, 1.0]
        x.costs_signed = [2.0, 1.0, 0]
        x.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2], 'crowding_distance':[50]}

        self.omopso.leaders.add(x)
        y = self.omopso.select_leader()

        self.assertEqual(x, y)

        z = Individual([3, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]
        z.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2], 'crowding_distance':[100]}

        self.omopso.leaders.add(z)
        y = self.omopso.select_leader()

        # the leader has the bigger crowding distance
        self.assertEqual(z, y)

    def test_velocity(self):
        # if every parameter set to one and we are not on the borders, we shuold got back the velocity
        # mocking the random numbers
        self.omopso.c1_min = 1.
        self.omopso.c1_max = 1.
        self.omopso.c2_min = 1.
        self.omopso.c2_max = 1.0
        self.omopso.r1_min = 1.0
        self.omopso.r1_max = 1.0
        self.omopso.r2_min = 1.0
        self.omopso.r2_max = 1.0
        self.omopso.min_weight = 1.0
        self.omopso.max_weight = 1.0

        x = Individual([1, 2])
        x.costs = [2.0, 1.0]
        x.costs_signed = [2.0, 1.0, 0]

        x.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        # add x elements to the leaders and to the population
        self.omopso.leaders.add(x)
        population = [x]
        self.omopso.update_velocity(population)

        self.assertEqual([1, 2], population[0].features['velocity'])

    def test_position_update(self):
        x = Individual([1, 2])
        x.costs = [2.0, 1.0]
        x.costs_signed = [2.0, 1.0, 0]

        x.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [x]

        self.omopso.update_position(population)

        self.assertEqual(population[0].vector, [2, 4])

    def test_position_update_particle_turn_back_from_the_border(self):
        x = Individual([10, 20])
        x.costs = [10.0, 20.0]
        x.costs_signed = [10.0, 20.0, 0]

        x.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}

        population = [x]

        self.omopso.update_position(population)

        self.assertEqual(population[0].vector, [10, 20])  # preserve the position
        self.assertEqual(population[0].features['velocity'], [-1, -2])  # particle should turn back

    def test_update_global_best(self):
        population = []
        for i in range(0, 10):
            x = Individual([i, 20 - i])
            x.costs = [i, 20.0 - i]
            x.costs_signed = [i, 20.0 - i, 0]

            x.features = {'velocity': [1, 2], 'best_cost': [0., 0., 0.], 'best_vector': [1, 2]}
            population.append(x)

        self.assertIsInstance(self.omopso.archive, Archive)  # archhive is an empty class here

        self.omopso.options['max_population_size'] = 5
        self.omopso.update_global_best(population)

        self.assertEqual(self.omopso.archive.size(), 10)  # archive should contain everybody
        self.assertEqual(self.omopso.leaders.size(), 5)  # shuold be truncated to 5
