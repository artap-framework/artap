from artap.problem import Problem
import pylab as pl

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc


class Results:

    def __init__(self, problem):
        self.problem = problem


class GraphicalResults(Results):

    def __init(self, problem):
        super.__init__(problem)
        
        rc('text', usetex=True)                
        rc('font', family='serif')


    def plot_all_individuals(self):        
        figure = pl.figure(1)
        for population in self.problem.populations:
            for individual in population.individuals:
                pl.plot(individual.number, individual.parameters[0], 'x')
        
        pl.savefig("all_individuals.pdf")
       
    def plot_populations(self):        
        for population in self.problem.populations:
            figure_name = "pareto_" + str(population.number) + ".pdf"
            if len(population.individuals) > 1:
                figure = Figure()
                FigureCanvas(figure)
                figure.add_subplot(111)        
                ax = figure.axes[0]
                colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']
                
                for individual in population.individuals:                                    
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
                    