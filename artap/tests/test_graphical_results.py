import os
import unittest
import tempfile
from shutil import copyfile, rmtree
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults

from skimage.io import imread
from skimage.measure import compare_mse as mse

class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        copyfile("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "data.sqlite",
                 self.working_dir + os.sep + "data.sqlite")
        database_file = self.working_dir + os.sep + "data.sqlite"
        data_store = SqliteDataStore(database_file=database_file)
        problem = ProblemDataStore(data_store, working_dir=self.working_dir)

        self.results = GraphicalResults(problem)

    def tearDown(self):
        rmtree(self.working_dir)
        pass

    def test_scatter(self):
        self.results.plot_scatter('F_1', 'F_2', extension="png")

        original = imread("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "scatter.png")
        picture = imread(self.working_dir + os.sep + "scatter.png")

        mssim = mse(original, picture)
        self.assertLess(mssim, 10)

    def test_individuals(self):
        self.results.plot_individuals('F_1', extension="png")

        original = imread("." + os.sep + "workspace" + os.sep + "common_data" + os.sep + "individuals.png")
        picture = imread(self.working_dir + os.sep + "individuals.png")

        mssim = mse(original, picture)
        self.assertLess(mssim, 10)

if __name__ == '__main__':
    unittest.main()
