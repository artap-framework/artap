from abc import ABC, abstractmethod

from .datastore import SqliteDataStore
from .individual import Individual


"""
 Module is dedicated to describe optimization problem. 
"""

class Problem(ABC):
    """ Is a main class wich collects information about optimization task """    
           
    def __init__(self, name, parameters, costs, datastore = None, working_dir = None):
        self.name = name

        self.working_dir = working_dir
        self.parameters = parameters
        self.costs = {cost:0 for cost in costs}

        if datastore is None:
            self.datastore = SqliteDataStore(self, working_dir = working_dir)
            self.datastore.create_structure_individual(self.parameters, self.costs)
        else:
            self.datastore = datastore
        
        self.id = self.datastore.get_id()
        self.populations = []
        
    def add_population(self, population):                
        self.populations.append(population)
        
    def evaluate_individual(self, x, population = 0):
        individ = Individual(x, self, population)        
        individ.evaluate()
        self.datastore.write_individual(individ.to_list())
        self.populations[population].individuals.append(individ)
        
        if len(individ.costs) == 1:
            return individ.costs[0]
        else:
            return individ.costs
                       
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def get_initial_values(self):
        values = []
        for parameter in self.parameters.items():
            if 'initial_value' in parameter[1]:
                values.append(parameter[1]['initial_value'])    
            else:
                values.append(0)

        return values

    @abstractmethod
    def eval(self):
        pass

class ProblemDataStore(Problem):
    def __init__(self, datastore):
        self.datastore = datastore
        self.datastore.read_problem(self)

    def eval(self):
        assert 0