from string import Template
from abc import ABC, abstractmethod
from .individual import Individual, Individual_NSGA_II

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc


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

    def to_string(self):
        string = "population number: " + str(self.number) + " \n"
      
        for individual in self.individuals:
            string += individual.toString() + ", "        
        
        return string

    def save(self):
        for individual in self.individuals:            
            individual.problem.datastore.write_individual(individual.to_list())

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
        self.individuals = Individual.gen_individuals(population_size, self.problem, self.number)
        return self.individuals
                       
    def evaluate(self):    
        for individual in self.individuals:
            if individual.is_evaluated == False:
                individual.evaluate()    

    
class Population_NSGA_II(Population):

    def __init__(self, problem, individuals = []):
            return super().__init__(problem, individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual_NSGA_II.gen_individuals(population_size, self.problem, self.number)