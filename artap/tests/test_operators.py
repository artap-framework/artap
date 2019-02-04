from artap.operators import RandomGeneration, SimpleMutation, SimulatedBinaryCrossover, SimpleCrossover
from artap.individual import Individual

import unittest


class TestCrossover(unittest.TestCase):
    """ Tests crossover."""

    def setUp(self):
        self.parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                           'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}

        self.i1 = Individual([1, 2, 2])
        self.i2 = Individual([3, 2, 1])

    def test_random_generator(self):
        gen = RandomGeneration(self.parameters)
        individuals = gen.generate(2)
        self.assertTrue(self.parameters['x_1']['bounds'][0] <= individuals[0].vector[0] <= self.parameters['x_1']['bounds'][1] and
                        self.parameters['x_2']['bounds'][0] <= individuals[0].vector[1] <= self.parameters['x_2']['bounds'][1] and
                        self.parameters['x_1']['bounds'][0] <= individuals[1].vector[0] <= self.parameters['x_1']['bounds'][1] and
                        self.parameters['x_2']['bounds'][0] <= individuals[1].vector[1] <= self.parameters['x_2']['bounds'][1])

    def test_simple_mutation(self):
        sbx = SimpleMutation(self.parameters, 0.7)
        individual = sbx.mutate(self.i1)
        self.assertTrue(
            self.parameters['x_1']['bounds'][0] <= individual.vector[0] <= self.parameters['x_1']['bounds'][1] and
            self.parameters['x_2']['bounds'][0] <= individual.vector[1] <= self.parameters['x_2']['bounds'][1])

    def test_sbx(self):
        sbx = SimulatedBinaryCrossover(self.parameters, 10)
        offsprings = sbx.cross(self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)

    def test_simple_crossover(self):
        sbx = SimpleCrossover(self.parameters, 0.9)
        offsprings = sbx.cross(self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)


if __name__ == '__main__':
    unittest.main()
