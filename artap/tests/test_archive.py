from artap.operators import SimpleMutator, SimulatedBinaryCrossover, SimpleCrossover, \
    TournamentSelector, ParetoDominance, nondominated_truncate, crowding_distance, PmMutator
from artap.individual import Individual
from artap.benchmark_pareto import BiObjectiveTestProblem
from math import inf
import unittest