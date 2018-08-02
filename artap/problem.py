import sqlite3
from string import Template
from abc import ABC, abstractmethod

from .datastore import DataStore
from .population import Population

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
from random import random

"""
 Module is dedicated to describe optimization problem. 
"""

class Problem(ABC):
    """ Is a main class wich collects information about optimization task """    
           
    def __init__(self, name, parameters, costs):                                        
        self.name = name
        self.path_to_source_files = ""
        self.source_files = []
        self.path_to_results = ""                    
        self.parameters = parameters        
        self.parameters_values = []
        for parameter in parameters.items():
            if 'initial_value' in parameter[1]:
                self.parameters_values.append(parameter[1]['initial_value'])    
            else:
                self.parameters_values.append(0)
        
        self.costs = {cost:0 for cost in costs}
        self.table_name = self.name
        self.datastore = DataStore(self.name)                
        self.create_table_individual()
        
        self.populations = []
        
    def add_population(self, population):                
        self.populations.append(population)
                
    def create_table_individual(self):
        self.datastore.create_table_individual(self.table_name, self.parameters, self.costs)    
        
    def evaluate_individual(self, x, population = 0):
        individ = Individual(x, self, population)        
        individ.evaluate()        
        self.populations[population].individuals.append(individ)
        
        if len(individ.costs) == 1:
            return individ.costs[0]
        else:
            return individ.costs

    def read_from_database(self):        
        self.data = self.datastore.read_all("data")
                       
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    @abstractmethod
    def eval(self):
        pass

    def plot_data(self):
        vector = []
        cost = []
        vector_length = len(self.parameters)
        self.read_from_database()

        for i in range(len(self.data)):
            vector.append(self.data[i][2:2 + vector_length])
            cost.append(self.data[i][2 + vector_length])

        import pylab as pl
        
        for j in range(vector_length):
            y = []
            for i in range(len(vector)):
                y.append(vector[i][j])
            pl.figure(j)        
            pl.plot(y)
            pl.grid() 
        
        pl.figure('Cost function')
        pl.plot(cost)
        
        pl.show()