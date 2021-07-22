import matplotlib.pyplot as plt
import numpy as np
from artap.algorithm_genetic import NSGAII
import pandas as pd
from artap.algorithm_swarm import PSOGA, SMPSO, OMOPSO
from artap.problem import Problem
from artap.NNQuantized import QNN_model
from math import sin
from artap.results import Results
from scipy.signal import argrelextrema
from artap.datastore import SqliteDataStore


class TestQNNProblem(Problem):

    def set(self):
        # self.parameters = [{'name': 'x_1', 'initial_value': 0.1, 'bounds': [0.0, 1.0]}]
        # self.costs = [{'name': 'F_1'}]
        pass

    def evaluate(self, individual):

        # TODO: Ask about the goal function
        # obtained from the examples/surrogate/simple_surrogate.py
        # x = individual.vector
        #
        # # the goal function
        # F1 = (6 * x[0] - 2) ** 2 * sin(12 * x[0] - 4)
        #
        # return [F1]
        pass


qnn = TestQNNProblem()
qnn.model = QNN_model(qnn)
# qnn.model.build_model(qnn)
qnn.model.train(qnn)

