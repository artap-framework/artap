import matplotlib.pyplot as plt
import numpy as np
from artap.algorithm_genetic import NSGAII
import pandas as pd
from artap.algorithm_swarm import PSOGA, SMPSO, OMOPSO
from artap.problem import Problem
from artap.results import Results
from scipy.signal import argrelextrema
from artap.datastore import SqliteDataStore


class TestQNNProblem(Problem):

    def set(self):
        self.parameters = []
        self.costs = []

    def evaluate(self, individual):
        pass


antenna = TestQNNProblem()
