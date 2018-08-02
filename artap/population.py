from string import Template
from abc import ABC, abstractmethod
from .individual import Individual

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
from random import random

class Population:
    
    size = 0
    number = 0

    def __init__(self, problem, individuals = []):
        self.length = len(individuals)   
        self.problem = problem     
        self.number = Population.number
        
        
        self.individuals = individuals
        for individual in self.individuals:
            individual.population_id = self.number
            individual.set_id()

        Population.number += 1

    def toString(self):
        string = "population number: " + str(self.number) + " \n"
      
        for individual in self.individuals:
            string += individual.toString() + ", "        
        
        return string

    def save(self):
        for individual in self.individuals:            
            individual.toDatabase()

    def print(self):
        print(self.toString())

    def plot(self):
        #TODO: Move settings outside
        rc('text', usetex=True)                
        rc('font', family='serif')

        figure_name = "pareto_" + str(self.number) + ".pdf"
        if len(self.individuals) > 1:
            figure = Figure()
            FigureCanvas(figure)
            figure.add_subplot(111)        
            ax = figure.axes[0]
            colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']
            for individual in self.individuals:            
                    #TODO: Make for more objective values
                    ax.plot(individual.costs[0], individual.costs[1], 'o')
                    if hasattr(individual, 'front_number'):
                        if individual.front_number != 0:
                            scale = 100 / (individual.front_number / 4.)
                            ax.scatter(individual.costs[0], individual.costs[1], 
                            scale, c = colors[(individual.front_number - 1) % 6])
            
            ax.set_xlabel('$x$')
            ax.set_ylabel('$y$')
            ax.grid()            
            figure.savefig(figure_name)
        
    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = []
        
        for i in range(population_size):    
            self.individuals.append(Individual(self.gen_vector(vector_length, parameters), self.problem))
        
        
    def evaluate(self):    
        for individual in self.individuals:
            if individual.is_evaluated == False:
                individual.evaluate()

    
    def gen_vector(self, vector_length, parameters: dict):    
            
        vector = []
        for parameter in parameters.items():
                    
            if not('bounds' in parameter[1]):
                bounds = None
            else:
                bounds = parameter[1]['bounds']

            if not('precision' in parameter[1]):
                precision = None
            else:
                precision = parameter[1]['precision']
            
            if (precision == None) and (bounds == None):
                vector.append(self.gen_number())
                continue
            
            if (precision == None):
                vector.append(self.gen_number(bounds=bounds))
                continue

            if (bounds == None):
                vector.append(self.gen_number(precision=precision))
                continue

            vector.append(self.gen_number(bounds, precision))

        return vector

    def gen_number(self, bounds = [], precision = 0):

        if bounds == []:
            bounds = [0, 1]
        
        if precision == 0:
            precision = 1e-12
            
        number = random() * (bounds[1] - bounds[0]) + bounds[0] 
        number = round(number / precision) * precision 

        return number

    