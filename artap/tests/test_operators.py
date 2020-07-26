from ..operators import SimpleMutator, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelector, ParetoDominance, nondominated_truncate, crowding_distance, PmMutator, EpsilonDominance, \
    UniformMutator, NonUniformMutation, FireflyStep
from ..individual import Individual
from ..benchmark_pareto import BiObjectiveTestProblem
from ..problem import Problem
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

        self.features = {}
        self.features['dominate'] = set()
        self.features['crowding_distance'] = 0
        self.features['domination_counter'] = 0
        self.features['front_number'] = 0
        self.features['precision'] = 7
        self.features['feasible'] = 0.0

    def test_simple_mutation(self):
        sm = SimpleMutator(self.parameters, 0.7)
        individual = sm.mutate(self.i1)
        self.assertTrue(
            self.parameters[0]['bounds'][0] <= individual.vector[0] <= self.parameters[0]['bounds'][1] and
            self.parameters[1]['bounds'][0] <= individual.vector[1] <= self.parameters[1]['bounds'][1])

    def test_sbx(self):
        sbx = SimulatedBinaryCrossover(self.parameters, 1.0)
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

        result = dominance.compare(i1.costs_signed, i2.costs_signed)
        self.assertEqual(result, 1)

        result = dominance.compare(i2.costs_signed, i1.costs_signed)
        self.assertEqual(result, 2)

        result = dominance.compare(i3.costs_signed, i4.costs_signed)
        self.assertEqual(result, 0)

    def test_pareto(self):
        individuals = []
        n = 10
        for i in range(n):
            for j in range(i + 2):
                individual = Individual([j, i + 1 - j])
                individual.costs = [j, i + 1 - j]
                individual.features = self.features.copy()
                individuals.append(individual)

        for individual in individuals:
            individual.calc_signed_costs(self.signs2)

        selector = TournamentSelector(self.parameters)
        selector.fast_nondominated_sorting(individuals)

        for individual in individuals:
            self.assertEqual(individual.costs_signed[0] + individual.costs_signed[1],
                             individual.features['front_number'])


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
        x.costs_signed = [2, 3, 0]
        y = Individual([1, 1, 0])  # last index means that the solution is computed correctly
        y.costs = [1, 1]
        y.costs_signed = [1, 1, 0]

        population = [x, y]

        self.selector.fast_nondominated_sorting(population)
        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[1].features['crowding_distance'])

    def test_should_compute_ranking_work_properly_case1(self):
        """ The list contains two solutions and y is dominated by x."""
        x = Individual([2, 2])
        x.costs = [2, 3]
        x.costs_signed = [2, 3, 0]
        y = Individual([2, 2, 0])  # last index means that the solution is computed correctly
        y.costs = [3, 6]
        y.costs_signed = [3, 6, 0]

        population = [x, y]
        self.selector.fast_nondominated_sorting(population)
        nondominated_truncate(population, 2)
        self.assertEqual(population[0].features['front_number'], 1)
        self.assertEqual(population[1].features['front_number'], 2)

    def test_should_sort_the_population_with_three_dominated_solutions_return_three_subfronts(self):
        x = Individual([2, 2])
        x.costs = [2, 3]
        x.costs_signed = [2, 3, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [3, 6]
        y.costs_signed = [3, 6, 0]

        z = Individual([2, 2, 0])  # last index means that the solution is computed correctly
        z.costs = [4, 8]
        z.costs_signed = [4, 8, 0]

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
        x = Individual([1.0, 0.0])
        y = Individual([0.5, 0.5])
        z = Individual([0, 1.0])
        v = Individual([0.6, 0.6])
        w = Individual([0.7, 0.5])

        x.costs_signed = [1.0, 0.0, 0.0]  # third value: 0 means its calculated
        y.costs_signed = [0.5, 0.5, 0.0]
        z.costs_signed = [0.0, 1.0, 0.0]

        v.costs_signed = [0.6, 0.6, 0.0]
        w.costs_signed = [0.7, 0.5, 0.0]

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

        self.assertAlmostEqual(inf, population[3].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[4].features['crowding_distance'])

    def test_should_the_crowding_distance_of_four_solutions_correctly_assigned(self):
        x = Individual([0, 1])
        y = Individual([1, 0])
        z = Individual([0.5, 0.5])
        v = Individual([0.75, 0.75])

        x.costs_signed = [0.0, 1.0, 0.0]  # third value: 0 means its calculated
        y.costs_signed = [1.0, 0.0, 0.0]
        z.costs_signed = [0.5, 0.5, 0.0]
        v.costs_signed = [0.75, 0.75, 0.0]

        population = [x, y, v, z]  # the expected results after sorting is : [x, y, z, v]

        for p in population:
            p.features['front_number'] = 1

        crowding_distance(population)
        population = nondominated_truncate(population, 4)

        self.assertAlmostEqual(inf, population[0].features['crowding_distance'])
        self.assertAlmostEqual(inf, population[1].features['crowding_distance'])
        self.assertAlmostEqual(1.5, population[2].features['crowding_distance'])
        self.assertAlmostEqual(1.0, population[3].features['crowding_distance'])


class SBXCrossoverTestCases(unittest.TestCase):

    def test_should_constructor_assign_the_correct_probability_value(self):
        crossover_probability = 0.8
        distribution_index = 15
        test2d = BiObjectiveTestProblem()
        SBXCrossover = SimulatedBinaryCrossover(test2d.parameters, crossover_probability, distribution_index)

        self.assertEqual(crossover_probability, SBXCrossover.probability)
        self.assertEqual(distribution_index, SBXCrossover.distribution_index)

    def test_should_constructor_raise_an_exception_if_the_probability_is_greater_than_one(self):
        with self.assertRaises(Exception):
            test2d = BiObjectiveTestProblem()
            SimulatedBinaryCrossover(test2d.parameters, 1.5, 20)

        with self.assertRaises(Exception):
            test2d = BiObjectiveTestProblem()
            SimulatedBinaryCrossover(test2d.parameters, 0.5, -1)


class DominanceComparator(unittest.TestCase):

    def test_should_dominance_comparator_return_zero_if_the_two_solutions_have_one_objective_with_the_same_value(self):
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [2.]
        x.costs_signed = [2., 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [2.]
        y.costs_signed = [2., 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(0, result)

    def test_should_dominance_comparator_return_two_if_the_two_solutions_have_one_objective_and_the_second_one_is_lower(
            self):
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [2.]
        x.costs_signed = [2., 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [1.]
        y.costs_signed = [1., 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(2, result)

    def test_should_dominance_comparator_return_one_if_the_two_solutions_have_one_objective_and_the_first_one_is_lower(
            self):
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [1.]
        x.costs_signed = [1., 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [2.]
        y.costs_signed = [2., 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(1, result)

    def test_should_dominance_comparator_work_properly_case_a(self):
        """ Case A: solution1 has objectives [-1.0, 5.0, 9.0] and solution2 has [2.0, 6.0, 15.0]
        """

        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [2.0, 6.0, 15.0]
        y.costs_signed = [2.0, 6.0, 15.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(1, result)

    def test_should_dominance_comparator_work_properly_case_b(self):
        """ Case B: solution1 has objectives [-1.0, 5.0, 9.0] and solution2 has [-1.0, 5.0, 10.0]
        """

        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.0, 10.0]
        y.costs_signed = [-1.0, 5.0, 10.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(1, result)

    def test_should_dominance_comparator_work_properly_case_c(self):
        """ Case C: solution1 has objectives [-1.0, 5.0, 9.0] and solution2 has [-2.0, 5.0, 9.0]
        """
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-2.0, 5.0, 9.0]
        y.costs_signed = [-2.0, 5.0, 9.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(2, result)

    def test_should_dominance_comparator_work_properly_case_d(self):
        """ Case d: solution1 has objectives [-1.0, 5.0, 9.0] and solution2 has [-1.0, 5.0, 8.0]
        """
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.0, 8.0]
        y.costs_signed = [-1.0, 5.0, 8.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(2, result)

    def test_should_dominance_comparator_work_properly_with_constrains_case_1(self):
        """ Case 1: solution2 has a higher degree of constraint violation than solution 1
        """
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 6.0, 11.0]
        x.costs_signed = [-1.0, 6.0, 11.0, -0.1]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.0, 10.0]
        y.costs_signed = [-1.0, 5.0, 10.0, -0.3]

        result = dominance.compare(x.costs_signed, y.costs_signed)
        self.assertEqual(1, result)

    def test_should_dominance_comparator_work_properly_with_constrains_case_2(self):
        """ Case 2: solution1 has a higher degree of constraint violation than solution 1
        """
        dominance = ParetoDominance()
        x = Individual([2, 2])
        x.costs = [-1.0, 6.0, 9.0]
        x.costs_signed = [-1.0, 6.0, 9.0, -0.5]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 6.0, 10.0]
        y.costs_signed = [-1.0, 6.0, 10.0, -0.1]

        result = dominance.compare(x.costs_signed, y.costs_signed)
        self.assertEqual(2, result)


class EpsDominanceComparator(unittest.TestCase):

    def test_should_dominance_comparator_work_properly_case_d(self):
        """ Case 1: solution1 has objectives [-1.0, 5.0, 9.0] and solution2 has [-1.0, 5.0, 8.0]
        """

        # eps-dominance comparator should give back the same results as pareto-dominance if eps = 1e-5

        dominance = EpsilonDominance(epsilons=1e-2)
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.01, 8.0]
        y.costs_signed = [-1.0, 5.01, 8.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(2, result)

        # eps-dominance comparator should give different results if eps = 1

        dominance = EpsilonDominance(epsilons=1e-3)
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.01, 8.0]
        y.costs_signed = [-1.0, 5.01, 8.0, 0]

        result = dominance.compare(x.costs_signed, y.costs_signed)

        self.assertEqual(0, result)

    def test_should_dominance_comparator_work_properly_with_constrains_case_1(self):
        """ Case 1: solution2 has a higher degree of constraint violation than solution 1
        """
        dominance = EpsilonDominance(epsilons=1e-5)
        x = Individual([2, 2])
        x.costs = [-1.0, 6.0, 11.0]
        x.costs_signed = [-1.0, 6.0, 11.0, -0.1]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 5.0, 10.0]
        y.costs_signed = [-1.0, 5.0, 10.0, -0.3]

        result = dominance.compare(x.costs_signed, y.costs_signed)
        self.assertEqual(1, result)

    def test_should_dominance_comparator_work_properly_with_constrains_case_2(self):
        """ Case 2: solution1 has a higher degree of constraint violation than solution 1
        """
        dominance = EpsilonDominance(epsilons=1e-5)
        x = Individual([2, 2])
        x.costs = [-1.0, 6.0, 9.0]
        x.costs_signed = [-1.0, 6.0, 9.0, -0.5]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 6.0, 10.0]
        y.costs_signed = [-1.0, 6.0, 10.0, -0.1]

        result = dominance.compare(x.costs_signed, y.costs_signed)
        self.assertEqual(2, result)

    def test_should_dominance_comparator_work_properly_select_closer_to_boundary(self):
        """ Case 3: solution1 closer to the rounded value than solution 2
        """
        dominance = EpsilonDominance(epsilons=0.1)
        x = Individual([2, 2])
        x.costs = [-1.0, 6.0, 9.05]
        x.costs_signed = [-1.0, 6.0, 9.05, 0.0]

        y = Individual([2, 2])  # last index means that the solution is computed correctly
        y.costs = [-1.0, 6.0, 9.06]
        y.costs_signed = [-1.0, 6.0, 9.06, 0.0]

        result = dominance.compare(x.costs_signed, y.costs_signed)
        self.assertEqual(1, result)


class TestTournamentSelector(unittest.TestCase):

    def test_should_execute_work_properly_case1(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = Individual([3, 2])  # last index means that the solution is computed correctly
        y.costs = [1.0, 4.0]
        y.costs_signed = [1.0, 4.0, 0.0]


class TestProblem(Problem):

    def set(self):
        self.name = 'Test Problem'
        self.parameters = [{'name': '1', 'bounds': [2., 10.]},
                           {'name': '2', 'bounds': [2., 20.]},
                           ]

        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, individual):
        return [1, 1]


class TestUniformMutator(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()
        self.um = UniformMutator(problem.parameters, 0)

    def test_should_the_solution_remain_unchanged_if_the_probability_is_zero(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = self.um.mutate(x)
        self.assertEqual(y.vector, [3, 2])

    def test_should_change_if_the_probability_is_one(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        self.um.probability = 1.0
        y = self.um.mutate(x)
        self.assertNotEqual(y.vector, [3, 2])


class TestUniformMutator(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()
        self.um = PmMutator(problem.parameters, 0)

    def test_should_the_solution_remain_unchanged_if_the_probability_is_zero(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = self.um.mutate(x)
        self.assertEqual(y.vector, [3, 2])

    def test_should_change_if_the_probability_is_one(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        self.um.probability = 1.0
        y = self.um.mutate(x)
        self.assertNotEqual(y.vector, [3, 2])


class TestNonUniformMutator(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()
        self.um = NonUniformMutation(problem.parameters, 0, 100, 1)

    def test_should_the_solution_remain_unchanged_if_the_probability_is_zero(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = self.um.mutate(x)
        self.assertEqual(y.vector, [3, 2])

    def test_should_change_if_the_probability_is_one(self):
        x = Individual([3, 2])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        self.um.probability = 1.0
        y = self.um.mutate(x, 2)
        self.assertNotEqual(y.vector, [3, 2])


class TestFireflystep(unittest.TestCase):

    def setUp(self):
        problem = TestProblem()
        self.crossover = FireflyStep(problem.parameters, 0, 1.0, 0, 1)

    def test_should_not_change_the_vector_by_the_given_values_if_not_dominates(self):
        x = Individual([4, 3])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = Individual([3, 2])
        y.costs = [1.0, 2.0]
        y.costs_signed = [1.0, 1.0, 0.0]

        self.crossover.attraction_step(y, x, 1)
        self.assertEqual([3.0, 2.0], y.vector)

    def test_should_change_the_vector_by_the_given_values(self):
        x = Individual([4, 3])
        x.costs = [2.0, 3.0]
        x.costs_signed = [2.0, 3.0, 0.0]

        y = Individual([3, 2])
        y.costs = [1.0, 2.0]
        y.costs_signed = [1.0, 1.0, 0.0]

        self.crossover.attraction_step(x, y, 1)
        self.assertEqual([3.0, 2.0], x.vector)


if __name__ == '__main__':
    unittest.main()
