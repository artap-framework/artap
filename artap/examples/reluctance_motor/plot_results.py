import os
import unittest
from artap.problem import ProblemDataStore
from artap.datastore import SqliteDataStore
from artap.results import GraphicalResults
from artap.benchmark_functions import Rosenbrock

working_dir = "./"
database_file = working_dir + "data.sqlite"
data_store = SqliteDataStore(database_file=database_file)
problem = ProblemDataStore(data_store, working_dir=working_dir)

results = GraphicalResults(problem)
# results.plot_all_individuals()
results.plot_populations()
results.plot_gradients()
