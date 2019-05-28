"""
import os
import unittest
import tempfile
from shutil import copyfile, rmtree
from artap.problem import ProblemSqliteDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults

from skimage.io import imread
from skimage.measure import compare_mse as mse


class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        copyfile("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite",
                 self.working_dir + os.sep + "data.sqlite")
        database_name = self.working_dir + os.sep + "data.sqlite"
        problem = ProblemSqliteDataStore(database_name=database_name)

        self.results = GraphicalResults(problem)

    def tearDown(self):
        rmtree(self.working_dir)
        pass

    def test_scatter(self):
        self.results.plot_scatter('F_1', 'F_2', filename=self.working_dir + os.sep + "scatter.png")

        original = imread("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "scatter.png")
        picture = imread(self.working_dir + os.sep + "scatter.png")

        mmse = mse(original, picture)
        self.assertLess(mmse, 100)

    def test_individuals(self):
        self.results.plot_individuals('F_1', filename=self.working_dir + os.sep + "individuals.png")

        original = imread("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "individuals.png")
        picture = imread(self.working_dir + os.sep + "individuals.png")

        mmse = mse(original, picture)
        self.assertLess(mmse, 100)


if __name__ == '__main__':
    unittest.main()
"""