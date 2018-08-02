import sqlite3
from string import Template
from abc import ABC, abstractmethod
from .datastore import DataStore
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
from random import random

class Individual:           # TODO: Add: precisions, bounds
    """
       Collects information about one point in design space.
    """   
    number = 0    
    
    def __init__(self, x, problem, population_id = 0):        
        self.vector = x
        self.problem = problem
        self.length = len(self.vector)
        self.costs = []                
        
        self.number = Individual.number
        Individual.number += 1    
        
        self.population_id = population_id
        self.is_evaluated = False

    def toString(self):
        string = "["
        for number in self.vector:
            string += str(number) + ", "
        string = string[:len(string)-1]
        string += "]"
        string += "; costs:["
        for number in self.costs:
            string += str(number) + ", "        
        string += "]\n"
        return string

    
    def toDatabase(self):  
        id = self.number        
        cmd_exec_tmp = Template("INSERT INTO $table (id, population_id, ")  # TODO: rewrite using string templates
        cmd_exec = cmd_exec_tmp.substitute(table = "data")        
        
        if type(self.costs) != list:
            costs = [self.costs]
        else:
            costs = self.costs
        
        for parameter_name in self.problem.parameters.keys():
            cmd_exec += parameter_name + ","
        
        for cost_name in self.problem.costs.keys():
            cmd_exec += cost_name + ","

        cmd_exec = cmd_exec[:-1]  # delete last comma
        cmd_exec += ") VALUES (?, ?, "

        for i in range(len(self.vector) + len(costs) - 1):
            cmd_exec += " ?,"
        cmd_exec += " ?);"           
               
        params = [id, self.population_id]
        
        for i in range(len(self.vector)):
            params.append(self.vector[i])
        
        for cost in self.costs:
            params.append(cost)

        self.problem.datastore.write_individual(cmd_exec, params)    
                
    def evaluate(self):        
        # problem cost function evaluate     
        costs = self.problem.eval(self.vector)            

        if type(costs) != list:
            self.costs = [costs]
        else:
            self.costs = costs
        
        self.is_evaluated = True        
        return costs


    def set_id(self):
        self.number = Individual.number
        Individual.number += 1