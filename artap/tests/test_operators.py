from artap.operators import SimpleMutator, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelector, ParetoDominance, nondominated_truncate
from artap.individual import Individual
from artap.benchmark_pareto import BiObjectiveTestProblem
from math import inf
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

        for individual in individuals:
            individual.calc_signed_costs(self.signs2)

        selector = TournamentSelector(self.parameters)
        selector.fast_nondominated_sorting(individuals)

        for individual in individuals:
            # print(individual.costs, individual.features['front_number'])
            self.assertEqual(individual.signs[0] + individual.signs[1], individual.features['front_number'])


class TestFastNonDominatedSorting(unittest.TestCase):

    def setUp(self):
        test2d = BiObjectiveTestProblem()
        self.selector = TournamentSelector(test2d.parameters)

    def test_should_constructor_create_a_valid_object(self):
        self.assertIsNotNone(self.selector)

    def test_should_compute_crowding_distance_if_the_population_contains_one_solution(self):
        x = Individual([0, 0])
        x.costs = [2, 3]
        population = [x]

        self.selector.fast_nondominated_sorting(population)
        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])

    def test_should_compute_crowding_distance_if_the_population_contains_two_individuals(self):
        x = Individual([0, 0])
        x.costs = [2, 3]
        x.signs = [2, 3, 0]
        y = Individual([1, 1, 0])  # last index means that the solution is computed correctly
        y.costs = [1, 1]
        y.signs = [1, 1, 0]

        population = [x, y]

        self.selector.fast_nondominated_sorting(population)
        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[1].features['crowding_distance'])

    def test_should_compute_ranking_work_properly_case1(self):
        """ The list contains two solutions and y is dominated by x."""
        x = Individual([2, 2])
        x.costs = [2, 3]
        x.signs = [2, 3, 0]
        y = Individual([2, 2, 0])  # last index means that the solution is computed correctly
        y.costs = [3, 6]
        y.signs = [3, 6, 0]

        population = [x, y]
        self.selector.fast_nondominated_sorting(population)
        nondominated_truncate(population,2)
        self.assertEqual(population[0].features['front_number'], 1)
        self.assertEqual(population[1].features['front_number'], 2)

    def test_should_sort_the_population_with_three_dominated_solutions_return_three_subfronts(self):

        x = Individual([2, 2])
        x.costs = [2, 3]
        x.signs = [2, 3, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [3, 6]
        y.signs = [3, 6, 0]

        z = Individual([2, 2, 0])  # last index means that the solution is computed correctly
        z.costs = [4, 8]
        z.signs = [4, 8, 0]

        population = [x, y, z]
        self.selector.fast_nondominated_sorting(population)
        nondominated_truncate(population, 3)
        self.assertEqual(population[0].features['front_number'], 1)
        self.assertEqual(population[1].features['front_number'], 2)
        self.assertEqual(population[2].features['front_number'], 3)

        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[1].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[2].features['crowding_distance'])

    def test_should_ranking_of_a_population_with_five_solutions_work_properly(self):

        x = Individual([2, 2])
        y = Individual([2, 2])
        z = Individual([2, 2])
        v = Individual([2, 2])
        w = Individual([2, 2])

        x.signs = [1.0, 0.0, 0.0] # third value: 0 means its calculated
        y.signs = [0.5, 0.5, 0.0]
        z.signs = [0.0, 1.0, 0.0]

        v.signs = [0.6, 0.6, 0.0]
        w.signs = [0.7, 0.5, 0.0]

        population = [x, y, z, v, w]

        self.selector.fast_nondominated_sorting(population)
        population = nondominated_truncate(population, 5)

        # [z, x, y]
        self.assertEqual(population[0].features['front_number'], 1)
        self.assertEqual(population[1].features['front_number'], 1)
        self.assertEqual(population[2].features['front_number'], 1)

        self.assertEqual(population[3].features['front_number'], 2)
        self.assertEqual(population[4].features['front_number'], 2)

        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[1].features['crowding_distance'])
        self.assertAlmostEqual(2.0, population[2].features['crowding_distance'])

if __name__ == '__main__':
    unittest.main()
