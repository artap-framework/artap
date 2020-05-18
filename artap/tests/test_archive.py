from archive import Archive

import unittest


class TestArchive(unittest.TestCase):

    def setUp(self):
        self.archive = Archive()

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.archive)