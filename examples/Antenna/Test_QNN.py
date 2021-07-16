import matplotlib.pyplot as plt
import numpy as np
from artap.algorithm_genetic import NSGAII
import pandas as pd
from artap.algorithm_swarm import PSOGA, SMPSO, OMOPSO
from artap.problem import Problem
from artap.NNQuantized import QNN_model
from artap.results import Results
from scipy.signal import argrelextrema
from artap.datastore import SqliteDataStore


class TestQNNProblem(Problem):

    def set(self):
        self.parameters = [{'name': 'epochs', 'bounds': [1, 100], 'parameter_type':'int', 'initial_value': 100},
                           {'name': 'lr', 'bounds': [0, 0.1], 'parameter_type': 'float', 'initial_value': 0.001}]
        self.costs = []

    def evaluate(self, individual):

        # TODO: Ask about the goal function
        pass


qnn = TestQNNProblem()
qnn.model = QNN_model(qnn)
qnn.model.build_model(qnn)
qnn.model.train(qnn)

