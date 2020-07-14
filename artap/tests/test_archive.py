from ..archive import Archive
from ..individual import Individual
from ..operators import crowding_distance

import unittest


class TestArchive(unittest.TestCase):

    def setUp(self):
        self.archive = Archive()

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.archive)

    def test_should_adding_one_solution_work_properly(self):
        x = Individual([2, 2])
        x.costs = [-1.0, 5.0, 9.0]
        x.costs_signed = [-1.0, 5.0, 9.0, 0]

        self.archive.add(x)
        self.assertEqual(1, self.archive.size())
        self.assertEqual(x, self.archive._contents[0])

    def test_should_adding_two_solutions_work_properly_if_one_is_dominated(self):
        dominated_solution = Individual([1, 2])
        dominated_solution.costs = [2.0, 2.0, 0]
        dominated_solution.costs_signed = [2.0, 2.0, 0]

        dominant_solution = Individual([1, 1])
        dominant_solution.costs = [1.0, 1.0, 0]
        dominant_solution.costs_signed = [1.0, 1.0, 0]

        self.archive.add(dominated_solution)
        self.archive.add(dominant_solution)

        self.assertEqual(1, self.archive.size())
        self.assertEqual(dominant_solution, self.archive._contents[0])

    def test_should_adding_two_solutions_work_properly_if_both_are_non_dominated(self):
        x = Individual([1, 2])
        x.costs = [1.0, 0.0, 0]
        x.costs_signed = [1.0, 0.0, 0]

        y = Individual([1, 1])
        y.costs = [0.0, 1.0, 0]
        y.costs_signed = [0.0, 1.0, 0]

        self.archive.add(x)
        self.archive.add(y)

        self.assertEqual(2, self.archive.size())
        self.assertTrue(x in self.archive._contents and
                        y in self.archive._contents)

    def test_should_adding_four_solutions_work_properly_if_one_dominates_the_others(self):
        x = Individual([1, 2])
        x.costs = [1.0, 1.0]
        x.costs_signed = [1.0, 1.0, 0]

        y = Individual([1, 2])
        y.costs = [0.0, 2.0]
        y.costs_signed = [0.0, 2.0, 0]

        z = Individual([1, 2])
        z.costs = [0.5, 1.5]
        z.costs_signed = [0.5, 1.5, 0]

        v = Individual([1, 2])
        v.costs = [0.0, 0.0]
        v.costs_signed = [0.0, 0.0, 0]

        self.archive.add(x)
        self.archive.add(y)
        self.archive.add(z)
        self.archive.add(v)

        self.assertEqual(1, self.archive.size())
        self.assertEqual(v, self.archive._contents[0])

    def test_should_adding_three_solutions_work_properly_if_two_of_them_are_equal(self):
        x = Individual([1, 2])
        x.costs = [1.0, 1.0]
        x.costs_signed = [1.0, 1.0, 0.0]

        y = Individual([1, 2])
        y.costs = [0.0, 2.0]
        y.costs_signed = [0.0, 2.0, 0.0]

        z = Individual([1, 2])
        z.costs = [1.0, 1.0]
        z.costs_signed = [1.0, 1.0, 0.0]

        self.archive.add(x)
        self.archive.add(y)

        result = self.archive.add(z)

        self.assertEqual(2, self.archive.size())
        self.assertFalse(result)
        self.assertTrue(x in self.archive._contents
                        or y in self.archive._contents)

    def test_crowding_distance_truncate(self):
        # the cost values for the test function, 16 non-dominated solution, half - of- them should be rejected by their
        # crowding distance

        test_costs = [[12, 0],
                      [11.5, 0.5],
                      [11, 1],
                      [10.8, 1.2],
                      [10.5, 1.5],
                      [10.3, 1.8],
                      [9.5, 2],
                      [9, 2.5],
                      [7, 3],
                      [5, 4],
                      [2.5, 6],
                      [2, 10],
                      [1.5, 11],
                      [1, 11.5],
                      [0.8, 11.7],
                      [0, 12]]

        for cost in test_costs:
            x = Individual(cost)
            x.costs = cost
            cost.append(0.)
            x.costs_signed = cost
            x.features = {'crowding_distance': 0}

            res = self.archive.add(x)

        crowding_distance(self.archive._contents)

        # test the algorithm adds every non-dominated solutions to the list
        self.assertEqual(self.archive.size(), len(test_costs))

        # ordering and truncate the elements according to their crowding distance,
        # length of the list should be the given number
        self.archive.truncate(8, 'crowding_distance')
        # if ordered by crowding distance the following items should be contained by the new list
        # the two endpoints
        x1 = Individual([0, 12])
        x1.costs = [0, 12]
        x1.costs_signed = [0, 12, 0.]

        x2 = Individual([12, 0])
        x2.costs = [12, 0]
        x2.costs_signed = [12, 0, 0.]

        self.assertIn(x1, self.archive._contents)
        self.assertIn(x2, self.archive._contents)

        x3 = Individual([1.5, 11])
        x3.costs = [1.5, 11]
        x3.costs_signed = [1.5, 11., 0.]

        self.assertIn(x3, self.archive._contents)
