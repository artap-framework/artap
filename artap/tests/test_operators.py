from artap.operators import SimpleMutator, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelector, ParetoDominance
from artap.individual import Individual

import unittest


class TestCrossover(unittest.TestCase):
    """ Tests crossover."""

    def setUp(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]

        self.signs = [1, 1]
        self.signs2 = [1, 1, 1]

        self.i1 = Individual([1, 2, 2])
        self.i2 = Individual([3, 2, 1])

        self.features = {'dominate': set(),
                         'crowding_distance': 0,
                         'domination_counter': 0,
                         'front_number': None}

    def test_simple_mutation(self):
        sbx = SimpleMutator(self.parameters, 0.7)
        individual = sbx.mutate(self.i1)
        self.assertTrue(
            self.parameters[0]['bounds'][0] <= individual.vector[0] <= self.parameters[0]['bounds'][1] and
            self.parameters[1]['bounds'][0] <= individual.vector[1] <= self.parameters[1]['bounds'][1])

    def test_sbx(self):
        sbx = SimulatedBinaryCrossover(self.parameters, 10)
        offsprings = sbx.cross(self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)

    def test_simple_crossover(self):
        sbx = SimpleCrossover(self.parameters, 0.9)
        offsprings = sbx.cross(self.i1, self.i2)
        self.assertEqual(len(offsprings), 2)

    def test_dominates(self):
        dominance = ParetoDominance()
        i1 = Individual([0, 0])
        i1.costs = [1, 1]
        i1.features = self.features.copy()
        i1.calc_signed_costs(self.signs)

        i2 = Individual([2, 2])
        i2.costs = [2, 2]
        i2.features = self.features.copy()
        i2.calc_signed_costs(self.signs)

        # test weak-strong dominance
        i3 = Individual([0, 0, 0])
        i3.costs = [1, 0, 2]
        i3.features = self.features.copy()
        i3.calc_signed_costs(self.signs2)

        i4 = Individual([1, 1, 1])
        i4.costs = [1, 1, 1]
        i4.features = self.features.copy()
        i4.calc_signed_costs(self.signs2)

        result = dominance.compare(i1.signs, i2.signs)
        self.assertEqual(result, 1)

        result = dominance.compare(i2.signs, i1.signs)
        self.assertEqual(result, 2)

        result = dominance.compare(i3.signs, i4.signs)
        self.assertEqual(result, 0)

    def test_pareto(self):
        individuals = []
        for i in range(3):
            for j in range(3):
                individual = Individual([0, 1])
                individual.signs = [1, 1]
                individual.features = self.features.copy()
                individuals.append(individual)

        individuals[0].costs = [0, 1]
        individuals[1].costs = [1, 0]
        individuals[2].costs = [0, 2]
        individuals[3].costs = [1, 1]
        individuals[4].costs = [2, 0]
        individuals[5].costs = [0, 3]
        individuals[6].costs = [1, 2]
        individuals[7].costs = [2, 1]
        individuals[8].costs = [3, 0]

        selector = TournamentSelector(self.parameters)
        selector.sorting(individuals)

        for individual in individuals:
            print(individual.costs, individual.features['front_number'])
            # self.assertEqual(individual.signed_costs()[0] + individual.signed_costs()[1], individual.features['front_number'])


if __name__ == '__main__':
    unittest.main()
