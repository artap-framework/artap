from artap.operators import SimulatedBinaryCrossover
from artap.individual import Individual

import unittest


class TestSensitivity(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_local_problem(self):
        parameters = {'x_1': {'initial_value': 2.5, 'bounds': [0, 5], 'precision': 1e-1},
                      'x_2': {'initial_value': 1.5, 'bounds': [0, 3], 'precision': 1e-1}}
        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 2, 1])
        parents = [i1, i2]
        sbx = SimulatedBinaryCrossover(parameters, 10)
        offsprings = sbx.run(parents)
        self.assertEqual(len(offsprings), 2)


if __name__ == '__main__':
    unittest.main()
