from artap.operators import RandomGeneration, SimpleMutation, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelection, ParetoDominance
from artap.individual import Individual
from artap.results import GraphicalResults

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

    def test_dominates(self):
        dominance = ParetoDominance()
        i1 = Individual([0, 0])
        i1.costs = [0, 1]
        i2 = Individual([2, 2])
        i2.costs = [2, 2]
        result = dominance.compare(i1, i2)
        self.assertEqual(result, 1)

        result = dominance.compare(i2, i1)
        self.assertEqual(result, 2)

    def test_pareto(self):
        individuals = []
        for i in range(3):
            for j in range(3):
                individual = Individual([0, 1])
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

        selector = TournamentSelection(self.parameters)
        selector.non_dominated_sort(individuals)

        for individual in individuals:
            self.assertEqual(individual.costs[0] + individual.costs[1], individual.front_number)


if __name__ == '__main__':
    unittest.main()
