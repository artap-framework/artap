from artap.operators import SimpleMutation, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelection, ParetoDominance
from artap.individual import Individual
from artap.algorithm_genetic import GeneticIndividual

import unittest


class TestCrossover(unittest.TestCase):
    """ Tests crossover."""

    def setUp(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [0, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [0, 3]}]

        self.signs = [1, 1]

        self.i1 = Individual([1, 2, 2])
        self.i2 = Individual([3, 2, 1])

    def test_simple_mutation(self):
        sbx = SimpleMutation(self.parameters, 0.7)
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
        i1 = GeneticIndividual([0, 0])
        i1.costs = [1, 1]

        i1.transform_data(self.signs)

        i2 = GeneticIndividual([2, 2])
        i2.costs = [2, 2]

        i2.transform_data(self.signs)

        result = dominance.compare(i1.signed_costs, i2.signed_costs)
        self.assertEqual(result, 1)

        result = dominance.compare(i2.signed_costs, i1.signed_costs)
        self.assertEqual(result, 2)

    def test_pareto(self):
        individuals = []
        for i in range(3):
            for j in range(3):
                individual = GeneticIndividual([0, 1])
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

        _ = [ind.transform_data(self.signs) for ind in individuals]

        selector = TournamentSelection(self.parameters)
        selector.sorting(individuals)

        for individual in individuals:
            # print(individual.costs, individual.front_number)
            self.assertEqual(individual.costs[0] + individual.costs[1], individual.front_number)


if __name__ == '__main__':
    unittest.main()
