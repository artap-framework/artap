from archive import Archive
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