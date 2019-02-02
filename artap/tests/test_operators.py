from artap.operators import SimulatedBinaryCrossover, SimpleCrossover
from artap.individual import Individual

import unittest


class TestCrossover(unittest.TestCase):
    """ Tests crossover."""

    def setUp(self):
        self.parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                          'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}

        self.i1 = Individual([1, 2, 2])
        self.i2 = Individual([3, 2, 1])

    def test_sbx(self):
        sbx = SimulatedBinaryCrossover(10)
        offsprings = sbx.cross(self.parameters, self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)

    def test_simple_crossover(self):
        sbx = SimpleCrossover()
        offsprings = sbx.cross(self.parameters, self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)


if __name__ == '__main__':
    unittest.main()
