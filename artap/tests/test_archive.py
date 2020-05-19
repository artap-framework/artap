from artap.archive import Archive
from artap.individual import Individual

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
